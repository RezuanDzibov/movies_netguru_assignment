from django.urls import path

from . import views


urlpatterns = [
    path("", views.MovieCreate.as_view(), name="create_movie"),
]
