from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    genreID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class Movie(models.Model):
    movieID = models.BigIntegerField(primary_key=True)
    poster_path = models.CharField(max_length=225, null=True, blank=True)

class Actor(models.Model):
    actorID = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255)

class Director(models.Model):
    directorID = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255)

class Review(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_reviews')

class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    movies = models.ManyToManyField("Movie", related_name='playlists')
