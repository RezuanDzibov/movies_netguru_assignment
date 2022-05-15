import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, request, response, status

from .serializers import MovieQuerySerializer
from . import services


class MovieCreate(views.APIView):
    @swagger_auto_schema(request_body=MovieQuerySerializer)
    def post(self, request: request.HttpRequest) -> response.Response:
        request_body = json.loads(request.body)
        movie_serializer = services.add_movie(request_body=request_body)
        return response.Response(data=movie_serializer.data, status=status.HTTP_201_CREATED)
