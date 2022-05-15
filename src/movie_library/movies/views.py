from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, request, response, status

from . import serializers, services


class MovieCreate(views.APIView):
    @swagger_auto_schema(
        request_body=serializers.MovieQuerySerializer,
        responses={201: serializers.MovieSerializerOut()},
    )
    def post(self, request: request.HttpRequest) -> response.Response:
        movie_serializer = services.add_movie(request_body=request.body)
        return response.Response(data=movie_serializer.data, status=status.HTTP_201_CREATED)


class MovieList(views.APIView):
    @swagger_auto_schema(responses={200: serializers.MovieListSerializer()})
    def get(self, request: request.Request) -> response.Response:
        movies_serializer = services.get_movies()
        return response.Response(data=movies_serializer.data, status=status.HTTP_200_OK)
