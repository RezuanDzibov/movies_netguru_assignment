import json
import re
from string import Template
from typing import Optional

import requests
from rest_framework.serializers import Serializer
from rest_framework import exceptions

from config import settings
from . import serializers
from .models import Comment, Movie

URI = Template(f"{settings.IMDB_API}&t=$movie_title&y=$movie_year")


class add_movie:
    def __init__(self, request_body: bytes) -> None:
        self.request_body: dict = json.loads(request_body)

    def _normalize_movie_data(self, data: dict) -> dict:
        movie_data: dict = {}
        for key, value in data.items():
            if key.isupper():
                key = key.lower()
                movie_data[key] = value
            else:
                key = re.sub("(?!^)([A-Z]+)", r"_\1", key).lower()
                movie_data[key] = value
        return movie_data

    def _fetch_movie_data(self, data_to_fetch: dict) -> dict:
        imdb_api_response = requests.get(
            URI.substitute(
                movie_title=data_to_fetch.get("title"),
                movie_year=data_to_fetch.get("release_year"),
            ),
        )
        imdb_api_response_data = json.loads(imdb_api_response.content)
        if imdb_api_response_data.get("Error", None):
            raise exceptions.APIException(detail=imdb_api_response_data.get("Error"))
        movie_data = self._normalize_movie_data(data=imdb_api_response_data)
        return movie_data

    def _serialize_movie_data(self, movie_data: dict) -> Serializer:
        serializer = serializers.MovieSerializerIn(data=movie_data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def _create_movie(self, movie_serializer: Serializer) -> Serializer:
        movie = Movie.objects.create(**movie_serializer.validated_data)
        movie_serializer_out = serializers.MovieSerializerOut(instance=movie)
        return movie_serializer_out

    def execute(self) -> Serializer:
        movie_data = self._fetch_movie_data(data_to_fetch=self.request_body)
        movie_data = self._serialize_movie_data(movie_data=movie_data)
        movie_serializer = self._create_movie(movie_serializer=movie_data)
        return movie_serializer


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
    comment_serializer_in = serializers.CommentCreateInSerializer(data=request_body)
    comment_serializer_in.is_valid(raise_exception=True)
    comment = Comment.objects.create(**comment_serializer_in.validated_data)
    comment_serializer_out = serializers.CommentCreateOutSerializer(instance=comment)
    return comment_serializer_out
