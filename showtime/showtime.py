import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    # Open the dataset of showtime
    def __init__(self):
        with open('{}/showtime/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
    
<<<<<<< HEAD
    # Function to get the list of all the schedule information in the database
=======
>>>>>>> f438f61734203f7ca1573b2603f6b6531dd5c86d
    def GetListShowtimes(self, request, context):
        for schedule in self.db:
            yield showtime_pb2.Schedule(date = schedule["date"], movies = schedule["movies"])

<<<<<<< HEAD
    # Function to get the list of movies on the given date
    def GetMoviebyDate(self, request, context):
        for schedule in self.db:
            # If the date exists return the date and movies in "Message Schedule" format
            if schedule["date"] == request.date:
                print("Schedule found!")
                return showtime_pb2.Schedule(date = schedule["date"], movies = schedule["movies"])
        return showtime_pb2.Schedule(date = "", movies = [])
=======
    def GetMoviebyDate(self, request, context):
        for schedule in self.db:
            if schedule["date"] == request.date:
                print("Schedule found!")
                return showtime_pb2.Schedule(date = schedule["date"], movies = schedule["movies"])
        return showtime_pb2.Schedule(date = "", movies = "")
>>>>>>> f438f61734203f7ca1573b2603f6b6531dd5c86d

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3202')
    server.start()
    #server.wait_for_termination()


if __name__ == '__main__':
    serve()
