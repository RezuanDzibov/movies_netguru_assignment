from typing import Optional

from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, request, response, status

from . import serializers
from . import services


class MovieList(views.APIView):
    @swagger_auto_schema(responses={200: serializers.MovieListSerializer()})
    def get(self, request: request.Request) -> response.Response:
        """
        Returns all movies from the database
        """
        movies_serializer = services.get_movies()
        return response.Response(data=movies_serializer.data, status=status.HTTP_200_OK)


class MovieCreate(views.APIView):
    @swagger_auto_schema(
        request_body=serializers.MovieQuerySerializer,
        responses={201: serializers.MovieSerializerOut()},
    )
    def post(self, request: request.HttpRequest) -> response.Response:
        """
        Creates a movie in the database
        """
        movie_serializer = services.add_movie(request_body=request.body).execute()
        return response.Response(data=movie_serializer.data, status=status.HTTP_201_CREATED)


class CommentList(views.APIView):
    @swagger_auto_schema(responses={200: serializers.CommentListSerializer})
    def get(self, request: request.HttpRequest, movie_id: Optional[int] = None) -> response.Response:
        """
        Returns all comments or for a movie from the database
        """
        if movie_id:
            comment_serializer = services.get_comments(movie_id=movie_id)
        else:
            comment_serializer = services.get_comments()
        return response.Response(data=comment_serializer.data, status=status.HTTP_200_OK)


class CommentCreate(views.APIView):
    @swagger_auto_schema(
        request_body=serializers.CommentCreateInSerializer,
        responses={201: serializers.CommentCreateOutSerializer()},
    )
    def post(self, request: request.HttpRequest) -> response.Response:
        """
        Creates a comment in the database
        """
        comment_serializer = services.add_comment(request_body=request.body)
        return response.Response(data=comment_serializer.data, status=status.HTTP_201_CREATED)
