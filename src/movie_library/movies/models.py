from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    # TODO: #5 #4 add slug field
    year = models.CharField(max_length=4)
    rated = models.CharField(max_length=15)
    released = models.CharField(max_length=50)
    runtime = models.CharField(max_length=20)
    genre = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    plot = models.TextField()
    language = models.CharField(max_length=255)
    country = models.CharField(max_length=255)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
