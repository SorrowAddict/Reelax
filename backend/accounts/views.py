from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ProfileSerializer, UserSerializer
from .models import User

# Create your views here.
class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileImage(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # 파일 업로드를 위한 파서

    def put(self, request):
        user = request.user
        profile_image = request.FILES.get('profile_image')

        if profile_image:
            user.profile_image = profile_image
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)


class FollowToggle(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_toggle = get_object_or_404(User, id=user_id)
        if user_to_toggle != request.user:
            if user_to_toggle in request.user.followings.all():
                request.user.followings.remove(user_to_toggle)
                return Response({"detail": "User unfollowed successfully"}, status=status.HTTP_200_OK)
            else:
                request.user.followings.add(user_to_toggle)
                return Response({"detail": "User followed successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "You cannot follow/unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)
