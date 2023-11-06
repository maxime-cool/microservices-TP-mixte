from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound
import urllib3

import grpc
import sys
sys.path.append('booking')
import booking_pb2
import booking_pb2_grpc

urllib3.disable_warnings()

app = Flask(__name__)

# Defining the server entry point
PORT = 3203
HOST = 'user'

# open the database user
with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"

def get_booking_for_user(stub, userid):
    allbookings = stub.GetBookings(userid)
    return allbookings

def add_booking_byuser(stub, bookingRequest):
    reponse = stub.AddBooking(bookingRequest)
    return reponse

# an entry point for obtaining reservations from a user's name or ID 
@app.route("/user", methods=['GET'])
def check_user_booking():
    # get the query parameter of user_id
    user_id = request.args.get("user_id")
    date = request.args.get("date")
    movieid = request.args.get("movieid")
    data = {"date": date, "movieid": movieid}
    user = next((user for user in users if str(user['id']) == str(user_id)), None)
    if user:
        # Use Booking GRPC to check if the booking is ok for this user
        with grpc.insecure_channel('booking:3201') as channel:
            stub = booking_pb2_grpc.BookingStub(channel)
            bookingRequest = booking_pb2.AddBookingRequest(userid=user_id, date=date, movieid=movieid)
            response = add_booking_byuser(stub, bookingRequest)
        # If there is the response
        if(len(response.booking.dates) != 0):
            res = jsonify({"message": "Booking created successfully"})
        # If there is not the response, that means in grpc booking has already exists
        else:
            res = make_response(jsonify({"error": "Failed to create booking"}), 400)
    else:
        res = make_response(jsonify({"error": "user ID not found"}), 400)
    return res

# an entry point for retrieving film information for a user's reservations 
@app.route("/user/booking/movies", methods=['GET'])
def get_user_booking_movies():
    # get the query parameter of user_id
    user_id = request.args.get("user_id")
    # check user existence
    user = next((user for user in users if user['id'] == user_id), None)
    if user: # if user exists, firstly go to the booking serveur to get the information of booking
        res = []
        # Get all the booking infotmation from channel booking in grpc
        with grpc.insecure_channel('booking:3201') as channel:
            stub = booking_pb2_grpc.BookingStub(channel)
            userid = booking_pb2.UserID(userid = user_id)
            response = get_booking_for_user(stub, userid)
        # Check if there is the booking or not for the user
        if response.booking.userid == "" and len(response.booking.dates) == 0:
            return make_response(jsonify({"error": "user ID no bookings"}), 400)
        # if booking exists, next go to check every record of booking to get movies
        for dates_info in response.booking.dates:
            date = dates_info.date  # Get the booking date
            movies = dates_info.movie  # Get the booking movie list
            info = {"date": date, "movies": []}  #Store the booking and movie information in the dict on this date
            for id in movies:
                # build the query
                query = """
                    query GetMovieWithId($movieId: String!) {
                    movie_with_id(_id: $movieId) {
                        title
                        rating
                        actors {
                        firstname
                        lastname
                        birthyear
                        }
                    }
                    }
                    """
                # Define a dictionary of variables, passing the value of the movieId variable.
                variables = {
                    "movieId": id
                }
                # Get the movie information in graphql
                movie = requests.post("http://movie:3200/graphql",json={'query': query, 'variables': variables})
                if movie.status_code != 200:
                    return make_response(jsonify({"error": "movies in booking not found"}), 400)
                info["movies"].append(movie.json())
            res.append(info)
        return make_response(jsonify(res), 200)
    else:
        return make_response(jsonify({"error": "user ID not found"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)