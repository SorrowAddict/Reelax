from rest_framework import serializers
from .models import Review, Movie, Actor, Director, Genre, Playlist
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ('__all__')


class UserLikedMoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('__all__')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_id', 'name']
        read_only_fields = ['genre_id']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_id', 'name', 'profile_path']
        read_only_fields = ['actor_id']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_id', 'name', 'profile_path']
        read_only_fields = ['director_id']


class ReviewSerializer(serializers.ModelSerializer):
    liked_by_count = serializers.IntegerField(source='liked_by.count', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'content', 'liked_by_count']
        read_only_fields = ['id', 'user', 'liked_by_count']


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'  # 모든 필드 반환
        # read_only_fields = ['movieID']  # movieID는 읽기 전용


class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'movie_id', 'title', 'overview', 'release_date', 'popularity',
            'vote_average', 'vote_count', 'poster_path', 'backdrop_path',
            'genres', 'actors', 'directors', 'additional_data'
        ]


class PlaylistSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'title', 'description', 'movies']
        read_only_fields = ['id']
