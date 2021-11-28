import os

import requests
from main import Movie, db

# this module is in charge of managing the request for de TMDB MOVIES

tmdb_username = os.environ.get('TMDB_USERNAME')
tmdb_password = os.environ.get('TMDB_PASSWORD')
tmdb_api_key = os.environ.get('TMDB_API_KEY')
tmdb_token = os.environ.get('TMDB_TOKEN')
aut_api_url = 'https://api.themoviedb.org/3/authentication/guest_session/new'


# Creates a guest session in case of been needed
aut_params = {
    'api_key': tmdb_api_key
}
aut_response = requests.get(url=aut_api_url, params=aut_params)
aut_data = aut_response.json()
guest_session_id = aut_data["guest_session_id"]
query_api_url = 'https://api.themoviedb.org/3/search/movie'

# When a movie_name is given its returns a list o movies with matching names
def get_movie_list(movie_name):
    query_api_url = 'https://api.themoviedb.org/3/search/movie'
    query_params = {
        'api_key': tmdb_api_key,
        'query': movie_name,
    }
    query_response = requests.get(url=query_api_url, params=query_params)
    query_data_json = query_response.json()
    query_data = query_data_json["results"]
    return query_data


# When original title of the movie its given its creates a new object (row) from the Movie class (table)
# and returns it
def get_movie(movie_original_name):
    query_api_url = 'https://api.themoviedb.org/3/search/movie'
    query_params = {
        'api_key': tmdb_api_key,
        'query': movie_original_name,
    }

    query_response = requests.get(url=query_api_url, params=query_params)
    query_data_json = query_response.json()
    query_data = query_data_json["results"][0]
    movie = Movie(
        title=query_data["original_title"],
        year=query_data["release_date"][0:4],
        description=query_data["overview"],
        rating=query_data["vote_average"],
        ranking="",
        review="",
        img_url="https://image.tmdb.org/t/p/w500"+query_data["poster_path"]
    )
    return movie

# Takes the movie movie's original title and calling get_movie() add the new object/row to the table Movie
def add_movie(movie_original_title):
    movie_object = get_movie(movie_original_title)
    db.session.add(movie_object)
    db.session.commit()

