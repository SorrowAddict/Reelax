from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movies.models import Actor, Director, Genre, Movie

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='followers')
    liked_actors = models.ManyToManyField(Actor, related_name='liked_by_users')
    liked_directors = models.ManyToManyField(Director, related_name='liked_by_users')
    liked_genres = models.ManyToManyField(Genre, related_name='liked_by_users')
    liked_movies = models.ManyToManyField(Movie, related_name='liked_by_users')