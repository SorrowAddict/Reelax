from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer
from movies.serializers import MovieSerializer, ActorSerializer, DirectorSerializer, GenreSerializer, PlaylistSerializer

UserModel = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(
        max_length=50
    )

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'nickname': self.validated_data.get('nickname', '')
        }


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'nickname'):
            extra_fields.append('nickname')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)


class ProfileSerializer(serializers.ModelSerializer):
    # Count fields
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)
    liked_movies_count = serializers.IntegerField(source='liked_movies.count', read_only=True)
    liked_actors_count = serializers.IntegerField(source='liked_actors.count', read_only=True)
    liked_directors_count = serializers.IntegerField(source='liked_directors.count', read_only=True)
    liked_genres_count = serializers.IntegerField(source='liked_genres.count', read_only=True)

    # Related fields
    liked_movies = MovieSerializer(many=True, read_only=True)
    liked_actors = ActorSerializer(many=True, read_only=True)
    liked_directors = DirectorSerializer(many=True, read_only=True)
    liked_genres = GenreSerializer(many=True, read_only=True)
    playlists = PlaylistSerializer(many=True, read_only=True)  # Playlist 추가

    class Meta:
        model = UserModel
        fields = [
            'id',
            'username',
            'nickname',
            'followers_count',
            'followings_count',
            'liked_movies_count',
            'liked_actors_count',
            'liked_directors_count',
            'liked_genres_count',
            'liked_movies',
            'liked_actors',
            'liked_directors',
            'liked_genres',
            'playlists',  # Profile에 Playlist 포함
        ]
        read_only_fields = [
            'followers_count', 'followings_count',
            'liked_movies_count', 'liked_actors_count',
            'liked_directors_count', 'liked_genres_count',
            'liked_movies', 'liked_actors',
            'liked_directors', 'liked_genres', 'playlists'
        ]
