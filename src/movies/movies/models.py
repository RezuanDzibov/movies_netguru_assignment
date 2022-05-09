from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()
    description = models.TextField()


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
