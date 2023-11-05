import json

# Function of getting the movie by giving movie id
def movie_with_id(_,info,_id):
    with open('{}/movie/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

# Function of getting the movie by giving movie title        
def movie_with_title(_,info,_title):
    with open('{}/movie/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie

# Function of getting the actors by giving the movie id            
def actor_with_id(_,info,_id): 
    with open('{}/movie/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors['actors']:
            if _id in actor['films']:
                return actor

# Function of updating the movie rate by giving movie id and new rate           
def update_movie_rate(_,info,_id,_rate):
    newmovies = {}
    newmovie = {}
    with open('{}/movie/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                # If movie exists, update the rate
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    # Store the changement in the database
    with open('{}/movie/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

# Function of updating the movie title by giving movie id and new rate
def update_movie_title(_,info,_id,_title):
    newmovies = {}
    newmovie = {}
    with open('{}/movie/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                # If movie exists, update the title
                movie['title'] = _title
                newmovie = movie
                newmovies = movies
    # Store the changement in the database
    with open('{}/movie/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

# Function of connecting to the parent movie object to provide a list of actors for the returned movie type
def resolve_actors_in_movie(movie, info):
    with open('{}/movie/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
    return actors
    
# Function of adding a new movie
def add_movie(_,info, _input):
    with open('{}/movie/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            # If movie already exists, print error
            if movie['id'] == _input['id']:
                print("error:movie ID already exists!")
                return movie
        # If movie dosen't exist, add the movie
        movies['movies'].append(_input)
    with open('{}/movie/data/movies.json'.format("."), "w") as wfile:
        json.dump(movies, wfile)
    return _input

# Function of deleting the movie by giving id   
def del_movie(_,info, _id):
    del_movie = {}
    with open('{}/movie/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            # If movie exists, delete the movie
            if movie['id'] == _id:
                del_movie = movie
                break
    # Store the changement in the database
    if(del_movie != {}):
        movies['movies'].remove(del_movie)
        with open('{}/movie/data/movies.json'.format("."), "w") as wfile:
            json.dump(movies, wfile)
        return del_movie
    else:
        print("error: Movie not find!")
        return movies['movies'][-1]
    






            




