from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, render_template, request, jsonify, make_response
from flask import Flask, request, jsonify

import resolvers as r

PORT = 3200
HOST = 'localhost'
app = Flask(__name__)

# Create elements for Ariadne
type_defs = load_schema_from_path('./movie/movie.graphql')
query = QueryType()

# Get the movie by its id, by passing in the appropriate options, you can get info of a Movie
movie = ObjectType('Movie')
query.set_field('movie_with_id', r.movie_with_id)

# Get the movie by its title, by passing in the appropriate options, you can get info of a Movie
query.set_field('movie_with_title', r.movie_with_title)

# Get the list of actors as the "actors" elementin the  type "Movie" when getting the movie information
actor = ObjectType('Actor')
movie.set_field('actors', r.resolve_actors_in_movie)

# Get directly the actor list by giving the movie id
query.set_field('actor_with_id', r.actor_with_id)

mutation = MutationType()
# Update the rate if movie by giving movie id
mutation.set_field('update_movie_rate', r.update_movie_rate)

# Update the title of movie by giving movie id
mutation.set_field('update_movie_title', r.update_movie_title)

# Add the new movie into the database
mutation.set_field('add_movie', r.add_movie)

# Delete the movie from the database by giving the movie id
mutation.set_field('del_movie', r.del_movie)

schema = make_executable_schema(type_defs, movie, query, mutation, actor)

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200

@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
                        schema,
                        data,
                        context_value=None,
                        debug=app.debug
                    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)