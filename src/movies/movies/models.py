from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()
    description = models.TextField()
