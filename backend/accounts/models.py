from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movies.models import Actor, Director, Genre, Movie, Playlist
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_username, user_email, user_field

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='followers')
    liked_actors = models.ManyToManyField(Actor, related_name='liked_by_users')
    liked_directors = models.ManyToManyField(Director, related_name='liked_by_users')
    liked_genres = models.ManyToManyField(Genre, related_name='liked_by_users')
    liked_movies = models.ManyToManyField(Movie, related_name='liked_by_users')
    playlists = models.ManyToManyField(Playlist, related_name='user_playlists')


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        nickname = data.get('nickname')

        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, 'first_name', first_name)
        if last_name:
            user_field(user, 'last_name', last_name)
        if nickname:
            user_field(user, 'nickname', nickname)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user