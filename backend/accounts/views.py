from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view

from .serializers import ProfileSerializer, UserSerializer
from .models import User

import requests
from json import JSONDecodeError
from allauth.socialaccount.models import SocialAccount
from http.cookies import SimpleCookie

state = settings.STATE
BASE_URL = 'http://localhost:8000/api/v1/'
# BASE_URL = 'http://43.203.255.151:8000/api/v1/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client

# Create your views here.
class Profile(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

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


# 구글 로그인
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


# 구글 콜백
def google_callback(request):
    client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
    client_secret = settings.SOCIAL_AUTH_GOOGLE_SECRET
    code = request.GET.get("code")
    frontend_url = "http://localhost:5173/google/callback/"  # 프론트엔드 Google Callback View 경로
    # frontend_url = "http://43.203.255.151:5173/google/callback/"  # 프론트엔드 Google Callback View 경로

    # 1. Access Token 요청
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")

    # 2. 사용자 이메일 요청
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse(
            {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
        )
    email_req_json = email_req.json()
    email = email_req_json.get("email")

    # 3. 사용자 회원가입 또는 로그인 처리
    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "google":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 로그인 처리
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=token_req_json)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)

        # 프론트엔드로 리디렉션
        accept_json = accept.json()
        access_token = accept_json.get("access")
        return redirect(f"{frontend_url}?access_token={access_token}")

    except User.DoesNotExist:
        # 신규 가입 처리
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=token_req_json)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)

        # 프론트엔드로 리디렉션
        accept_json = accept.json()
        access_token = accept_json.get("access")
        return redirect(f"{frontend_url}?access_token={access_token}")