from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(
        max_length=50
    )

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', '')
        }