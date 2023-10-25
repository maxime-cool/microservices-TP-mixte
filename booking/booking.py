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
        self.data_file_path = '{}/booking/data/bookings.json'
        with open('{}/booking/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookings(self, request, context):
        for booking in self.db:
            if booking["userid"] == request.userid:
                print("Booking found!")
                dates = []
                for item in booking["dates"]:
                    dates.append(booking_pb2.Dates(date = item["date"], movie = item["movies"]))
                booking_info = booking_pb2.Booking_info(userid=booking['userid'], dates = dates)
                return booking_pb2.BookingResponse(booking = booking_info)
        return booking_pb2.BookingResponse(booking_pb2.Booking_info(userid="", dates = ""))

    def GetListBookings(self, request, context):
        for booking in self.db:
            booking_info = booking_pb2.Booking_info(userid=booking['userid'], dates = booking_pb2.Dates(booking["dates"]["date"], booking["dates"]["movies"]))
            yield booking_pb2.BookingResponse(booking_info)

    def AddBooking(self, request, context):
        userid = request.userid
        date = request.date
        movieid = request.movieid
        if(self.CheckMovieDate(movieid, date)):
            for user_bookings in self.db:
                if str(user_bookings["userid"]) == str(userid):  # if userid exists
                    for day in user_bookings["dates"]:
                        if str(day["date"]) == str(date):  # if user already has a booking on date
                            if movieid in day["movies"]: #if movie is already booked on this day
                                print("Booking already exists!")
                            day["movies"].append(movieid)  # then add movie to existing list
                            self.save_data()
                            booking_info = booking_pb2.Booking_info(userid=user_bookings['userid'], dates = booking_pb2.Dates(date = date, movie = movieid))
                            return booking_pb2.BookingResponse(booking_info)

                    user_bookings["dates"].append({
                        "date": date,
                        "movies": [movieid]})
                    self.save_data()
                    booking_info = booking_pb2.Booking_info(userid=user_bookings['userid'], dates = booking_pb2.Dates(date = date, movie = movieid))
                    return booking_pb2.BookingResponse(booking_info)
            user_bookings.append({
                "userid": userid,
                "dates":[
                    {
                        "date":date,
                        "movies": [movieid]
                    }
                ]
            })
        else:
            print("error: " "movie or date not found")

    def CheckMovieDate(self, movie, date):
        with grpc.insecure_channel('localhost:3002') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            date = showtime_pb2.Dates(date=date)
            schedule = stub.GetMoviebyDate(date)
        if(movie in schedule.movies): return True
        else: return False

    def save_data(self):
        try:
            with open(self.data_file_path, "w") as jsf:
                json.dump({"schedule": self.db}, jsf)
        except Exception as e:
            print(f"error when saving: {e}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3201')
    server.start()
    #server.wait_for_termination()

if __name__ == '__main__':
    serve()
