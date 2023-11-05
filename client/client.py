import grpc
import sys

sys.path.append('showtime')
import showtime_pb2
import showtime_pb2_grpc

sys.path.append('booking')
import booking_pb2
import booking_pb2_grpc


def get_list_showtimes(stub):
    allSchedules = stub.GetListShowtimes(showtime_pb2.Empty())
    print(allSchedules)

def get_movie_by_date(stub, date):
    schedule = stub.GetMoviebyDate(date)
    print(schedule)

def get_booking_for_user(stub, userid):
    allbookings = stub.GetBookings(userid)
    print(allbookings)

def add_booking_byuser(stub, bookingRequest):
    reponse = stub.AddBooking(bookingRequest)
    print(reponse)

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3202') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- Test of showtime --------------")
        get_list_showtimes(stub)
        date = showtime_pb2.Date(date="20151130")
        get_movie_by_date(stub, date)

    with grpc.insecure_channel('localhost:3201') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)

        print("-------------- Test of booking --------------")
        userid = booking_pb2.UserID(userid = "garret_heaton")
        get_booking_for_user(stub, userid)

        bookingRequest = booking_pb2.AddBookingRequest(userid="chris_rivers", date="20151202", movieid="276c79ec-a26a-40a6-b3d3-fb242a5947b6")
        add_booking_byuser(stub, bookingRequest)

    channel.close()

if __name__ == '__main__':
    run()