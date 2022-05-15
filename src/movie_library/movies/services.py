import json
from string import Template

import requests
from rest_framework.serializers import Serializer

from config import settings
from . import serializers
from .models import Movie

URI = Template(f"{settings.IMDB_API}&t=$movie_title&y=$movie_year")


def add_movie(request_body: bytes) -> Serializer:
    request_body_data = json.loads(request_body)
    imdb_api_response = requests.get(
        URI.substitute(
            movie_title=request_body_data.get("title"),
            movie_year=request_body_data.get("release_year"),
        ),
    )
    imdb_api_response_data = json.loads(imdb_api_response.content)
    movie_data = {k.lower(): v for k, v in imdb_api_response_data.items()}
    # TODO: #1 move api fetch to a function
    movie_serializer_in = serializers.MovieSerializerIn(data=movie_data)
    movie_serializer_in.is_valid(raise_exception=True)
    movie = Movie.objects.create(**movie_serializer_in.validated_data)
    movie_serializer_out = serializers.MovieSerializerOut(instance=movie)
    return movie_serializer_out


def get_movies() -> Serializer:
    movies = Movie.objects.all()
    movie_serializer = serializers.MovieListSerializer(many=True, instance=movies)
    return movie_serializer
