import json
from typing import Optional
from string import Template

import requests
from rest_framework.serializers import Serializer

from config import settings
from . import serializers
from .models import Comment, Movie

URI = Template(f"{settings.IMDB_API}&t=$movie_title&y=$movie_year")


class AddMovie:
    def __call__(self, request_body: bytes) -> Serializer:
        request_body_data = json.loads(request_body)
        movie_data = self.get_movie_data(request_body_data=request_body_data)
        movie_serializer = self.create_movie(movie_data=movie_data)
        return movie_serializer

    def get_movie_data(self, request_body_data: dict) -> dict:
        imdb_api_response = requests.get(
            URI.substitute(
                movie_title=request_body_data.get("title"),
                movie_year=request_body_data.get("release_year"),
            ),
        )
        imdb_api_response_data = json.loads(imdb_api_response.content)
        movie_data = {k.lower(): v for k, v in imdb_api_response_data.items()}
        return movie_data

    def create_movie(self, movie_data: dict) -> Serializer:
        movie_serializer_in = serializers.MovieSerializerIn(data=movie_data)
        movie_serializer_in.is_valid(raise_exception=True)
        movie = Movie.objects.create(**movie_serializer_in.validated_data)
        movie_serializer_out = serializers.MovieSerializerOut(instance=movie)
        return movie_serializer_out


def get_movies() -> Serializer:
    movies = Movie.objects.all()
    movie_serializer = serializers.MovieListSerializer(many=True, instance=movies)
    return movie_serializer


def get_comments(movie_id: Optional[int] = None) -> Serializer:
    if movie_id:
        comments = Comment.objects.filter(movie__id=movie_id)
    else:
        comments = Comment.objects.all()
    comment_serializer = serializers.CommentListSerializer(many=True, instance=comments)
    return comment_serializer


def add_comment(request_body: bytes) -> Serializer:
    comment_data = json.loads(request_body)
    comment_serializer_in = serializers.CommentCreateInSerializer(data=comment_data)
    comment_serializer_in.is_valid(raise_exception=True)
    comment = Comment.objects.create(**comment_serializer_in.validated_data)
    comment_serializer_out = serializers.CommentCreateOutSerializer(instance=comment)
    return comment_serializer_out


class MovieService:
    get_all = staticmethod(get_movies)
    add = AddMovie()


class CommentService:
    get_all = staticmethod(get_comments)
    add = staticmethod(add_comment)
