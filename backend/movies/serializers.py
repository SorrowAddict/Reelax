from rest_framework import serializers
from .models import Review, Movie
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
