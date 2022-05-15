from django.urls import path

from . import views


urlpatterns = [
    path("list/", views.MovieList.as_view(), name="list_movies"),
    path("create/", views.MovieCreate.as_view(), name="create_movie"),
]
