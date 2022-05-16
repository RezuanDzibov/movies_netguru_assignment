from django.urls import path

from . import views


urlpatterns = [
    path("movies/list/", views.MovieList.as_view(), name="list_movies"),
    path("movies/create/", views.MovieCreate.as_view(), name="create_movie"),
    path("comments/list/", views.CommentList.as_view(), name="list_comments"),
]
