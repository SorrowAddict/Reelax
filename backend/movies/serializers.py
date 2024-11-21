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
        fields = ['genreID', 'name']
        read_only_fields = ['genreID']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)  # M:N 관계 (장르)

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['movieID']


class MovieCreateSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all()
    )
    actors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all(), required=False
    )
    directors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Director.objects.all(), required=False
    )

    class Meta:
        model = Movie
        fields = [
            'movieID', 'title', 'overview', 'release_date', 'popularity',
            'vote_average', 'vote_count', 'poster_path', 'backdrop_path',
            'genres', 'actors', 'directors'
        ]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actorID', 'name', 'profile_path']
        read_only_fields = ['actorID']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['directorID', 'name', 'profile_path']
        read_only_fields = ['directorID']


class ReviewSerializer(serializers.ModelSerializer):
    liked_by_count = serializers.IntegerField(source='liked_by.count', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'content', 'liked_by_count']
        read_only_fields = ['id', 'user', 'liked_by_count']


class PlaylistSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'title', 'description', 'movies']
        read_only_fields = ['id']
