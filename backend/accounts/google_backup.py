from http.cookies import SimpleCookie
from json.decoder import JSONDecodeError
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import status
from accounts.models import User
from allauth.socialaccount.models import SocialAccount
import requests

state = settings.STATE
BASE_URL = 'http://43.203.255.151:8000/api/v1/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'

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
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
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
    """
    Signup or Signin Request
    """

    cookie_max_age = 3600 * 24 * 14 # 14 days

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

        # Google로 로그인 요청
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=token_req_json)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)

        # Set-Cookie 헤더에서 refresh_token 추출
        refresh_token_header = accept.headers.get('Set-Cookie')
        if refresh_token_header:
            cookie = SimpleCookie()
            cookie.load(refresh_token_header)
            refresh_token = cookie.get('my-refresh-token')
            if refresh_token:
                refresh_token_value = refresh_token.value
            else:
                return JsonResponse({"err_msg": "refresh_token not found"}, status=400)
        else:
            return JsonResponse({"err_msg": "Set-Cookie header not found"}, status=400)

        # Response에 refresh_token 설정
        accept_json = accept.json()
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie(
            'refresh_token',
            refresh_token_value,
            max_age=cookie_max_age,
            httponly=True,
            samesite='Lax',
        )
        return response_cookie

    except User.DoesNotExist:
        # 신규 가입 처리
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=token_req_json)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)

        # Set-Cookie 헤더에서 refresh_token 추출
        refresh_token_header = accept.headers.get('Set-Cookie')
        if refresh_token_header:
            cookie = SimpleCookie()
            cookie.load(refresh_token_header)
            refresh_token = cookie.get('my-refresh-token')
            if refresh_token:
                refresh_token_value = refresh_token.value
            else:
                return JsonResponse({"err_msg": "refresh_token not found"}, status=400)
        else:
            return JsonResponse({"err_msg": "Set-Cookie header not found"}, status=400)

        # Response에 refresh_token 설정
        accept_json = accept.json()
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie(
            'refresh_token',
            refresh_token_value,
            max_age=cookie_max_age,
            httponly=True,
            samesite='Lax',
        )
        return response_cookie
