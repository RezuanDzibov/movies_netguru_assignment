import json
from string import Template

import requests
from rest_framework.serializers import Serializer

from config import settings
from .models import Movie
from .serializers import MovieSerializerIn, MovieSerializerOut, MovieListSerializer

URI = Template(f"{settings.IMDB_API}&t=$movie_title&y=$movie_year")


def add_movie(request_body: dict) -> Serializer:
    imdb_api_response = requests.get(
        URI.substitute(
            movie_title=request_body.get("title"),
            movie_year=request_body.get("release_year"),
        ),
    )
    imdb_api_response_data = json.loads(imdb_api_response.content)
    movie_data = {k.lower(): v for k, v in imdb_api_response_data.items()}
    movie_serializer_in = MovieSerializerIn(data=movie_data)
    movie_serializer_in.is_valid(raise_exception=True)
    movie = Movie.objects.create(**movie_serializer_in.validated_data)
    movie_serializer_out = MovieSerializerOut(instance=movie)
    return movie_serializer_out


def get_movies() -> Serializer:
    movies = Movie.objects.all()
    movie_serializer = MovieListSerializer(many=True, instance=movies)
    return movie_serializer
