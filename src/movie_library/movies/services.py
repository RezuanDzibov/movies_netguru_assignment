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
        """
        It takes a dictionary of movie data, and returns a dictionary of movie data with all the keys
        lowercased and with underscores instead of camel case
        
        :param data: dict = {}
        :type data: dict
        :return: A dictionary of movie data.
        """
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
        """
        It takes a dictionary of movie data, makes a request to the IMDB API, and returns a dictionary of
        movie data
        
        :param data_to_fetch: This is the data that we want to fetch from the API
        :type data_to_fetch: dict
        :return: A dictionary of movie data.
        """
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
        """
        It takes a dictionary of movie data, validates it, and returns a serializer
        
        :param movie_data: The data that will be serialized
        :type movie_data: dict
        :return: A serializer object.
        """
        serializer = serializers.MovieSerializerIn(data=movie_data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def _create_movie(self, movie_serializer: Serializer) -> Serializer:
        """
        It creates a movie and returns a serializer of the created movie
        
        :param movie_serializer: Serializer
        :type movie_serializer: Serializer
        :return: A serializer object
        """
        movie = Movie.objects.create(**movie_serializer.validated_data)
        movie_serializer_out = serializers.MovieSerializerOut(instance=movie)
        return movie_serializer_out

    def execute(self) -> Serializer:
        """
        It fetches the movie data, serializes it, and then creates the movie
        :return: A serializer object
        """
        movie_data = self._fetch_movie_data(data_to_fetch=self.request_body)
        movie_data = self._serialize_movie_data(movie_data=movie_data)
        movie_serializer = self._create_movie(movie_serializer=movie_data)
        return movie_serializer


def get_movies() -> Serializer:
    """
    It returns a serializer of all the movies in the database
    :return: A serializer object
    """
    movies = Movie.objects.all()
    movie_serializer = serializers.MovieListSerializer(many=True, instance=movies)
    return movie_serializer


def get_comments(movie_id: Optional[int] = None) -> Serializer:
    """
    It returns a list of comments for a given movie
    
    :param movie_id: Optional[int] = None
    :type movie_id: Optional[int]
    :return: A serializer object
    """
    if movie_id:
        comments = Comment.objects.filter(movie__id=movie_id)
    else:
        comments = Comment.objects.all()
    comment_serializer = serializers.CommentListSerializer(many=True, instance=comments)
    return comment_serializer


def add_comment(request_body: bytes) -> Serializer:
    """
    It takes a request body, validates it, creates a new comment, and returns a serialized version of
    the comment
    
    :param request_body: bytes
    :type request_body: bytes
    :return: A serializer object.
    """
    comment_serializer_in = serializers.CommentCreateInSerializer(data=request_body)
    comment_serializer_in.is_valid(raise_exception=True)
    comment = Comment.objects.create(**comment_serializer_in.validated_data)
    comment_serializer_out = serializers.CommentCreateOutSerializer(instance=comment)
    return comment_serializer_out
