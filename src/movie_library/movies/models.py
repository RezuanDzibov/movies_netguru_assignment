from django.db import models
from django.utils.text import slugify


class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
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

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.title)}-{self.year}"
        return super().save(*args, **kwargs)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
