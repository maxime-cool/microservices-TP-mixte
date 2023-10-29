import grpc
import sys
from concurrent import futures
import booking_pb2
import booking_pb2_grpc

sys.path.append('showtime')
import showtime_pb2
import showtime_pb2_grpc

import json

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        # Define the path to the database and open the database
        self.data_file_path = './booking/data/bookings.json'
        with open('{}/booking/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    # Function defined for getting the booking information by user ID
    def GetBookings(self, request, context):
        for booking in self.db:
            # If user ID is finded in the database
            if booking["userid"] == request.userid:
                print("Booking found!")
                # Store all the booking information in the datatype GRPC
                dates = []
                for item in booking["dates"]:
                    dates.append(booking_pb2.Dates(date = item["date"], movie = item["movies"]))
                booking_info = booking_pb2.Booking_info(userid=booking['userid'], dates = dates)
                return booking_pb2.BookingResponse(booking = booking_info)
        return booking_pb2.BookingResponse(booking_pb2.Booking_info(userid="", dates = ""))

    #Function defined for getting the list of all the booking information in the dataset
    def GetListBookings(self, request, context):
        for booking in self.db:
            booking_info = booking_pb2.Booking_info(userid=booking['userid'], dates = booking_pb2.Dates(booking["dates"]["date"], booking["dates"]["movies"]))
            yield booking_pb2.BookingResponse(booking_info)

    #Add the booking for user
    def AddBooking(self, request, context):
        # Get all the necessary information for add a booking: userID, date for the booking, movie for the booking 
        userid = request.userid
        date = request.date
        movieid = request.movieid
        # Check if the movie is avaible on the date
        if(self.CheckMovieDate(movieid, date)):
            # If movie is avaible, check if the user has made the booking before
            for user_bookings in self.db:
                if str(user_bookings["userid"]) == str(userid):  # If userid exists
                    # Get the index of the user data in the reservation dataset to update the database    
                    index = self.db.index(user_bookings)  
                    for day in user_bookings["dates"]:
                        if str(day["date"]) == str(date):  # if user already has a booking on date
                            if movieid in day["movies"]: #if movie is already booked on this day
                                print("Booking already exists!")
                                return booking_pb2.BookingResponse(booking = booking_pb2.Booking_info(userid=user_bookings['userid'], dates=[]))
                            else:
                                # Get the index of the user movie data in the reservation dataset to update the database
                                index_movie = user_bookings["dates"].index(day)
                                self.db[index]["dates"][index_movie].append(movieid)  # Then add movie to existing list 
                                dates = booking_pb2.Dates(date = date, movie = [movieid])
                                booking_info = booking_pb2.Booking_info(userid=user_bookings['userid'], dates=[dates])
                                # Save the changes of booking in the dataset
                                self.save_data()
                                return booking_pb2.BookingResponse(booking=booking_info)
                        
                    # If user has existed in the booking dataset, but dont have the booking information on this date and movie
                    self.db[index]["dates"].append({
                        "date": date,
                        "movies": [movieid]})
                    booking_info = booking_pb2.Booking_info(userid=user_bookings['userid'], dates=[booking_pb2.Dates(date = date, movie = [movieid])])
                    self.save_data() ## Save the changes of booking in the dataset
                    return booking_pb2.BookingResponse(booking=booking_info)
                
            # If movie is avaible, but the first time for user to add a booking
            self.db.append({
                "userid": userid,
                "dates":[
                    {
                        "date":date,
                        "movies": [movieid]
                    }
                ]
            })
            # Save the changes of booking in the dataset
            self.save_data()
            dates = booking_pb2.Dates(date = date, movie = [movieid])
            booking_info = booking_pb2.Booking_info(userid=userid, dates = [dates])
            return booking_pb2.BookingResponse(booking = booking_info)
        else:
            # Movie is not avaible on the date
            print("error: " "movie or date not found")
            return booking_pb2.BookingResponse(booking = booking_pb2.Booking_info(userid=user_bookings['userid'], dates=[]))

    # Function defined to check if the movie is avaible on the given date
    def CheckMovieDate(self, movie, date):
        # Make the connection to the server of showtime to get list of movies on the date
        with grpc.insecure_channel('localhost:3202') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            date = showtime_pb2.Date(date=date)
            schedule = stub.GetMoviebyDate(date)
        # If the movie is in the list, then movie is avaible on the date, return true
        if(movie in schedule.movies): return True
        else: return False

    def save_data(self):
        try:
            with open(self.data_file_path, "w") as jsf:
                json.dump({"bookings": self.db}, jsf)
        except Exception as e:
            print(f"error when saving: {e}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3201')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
