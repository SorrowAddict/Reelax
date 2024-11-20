# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

import requests
from datetime import datetime

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_READ_ACCESS_TOKEN = settings.TMDB_READ_ACCESS_TOKEN
YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY

# Create your views here.
# TMDB API에서 평점 상위 10개 영화 조회
class TopRated(APIView):
    def get(self, request):
        url = f"{TMDB_BASE_URL}/movie/top_rated"
        params = { "api_key": TMDB_API_KEY, "language": "ko-KR", "page": 1 }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            movies = response.json().get("results", [])[:10]
            return Response({ 'results': movies }, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch top-rated movies"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# 현재 박스오피스 상위 10개 영화 조회
class popular(APIView):
    def get(self, request):
        url = f"{TMDB_BASE_URL}/movie/popular"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ko-KR",
            "page": 1,
            "region": "KR",
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            movies = response.json().get("results", [])[:10]
            return Response({ 'results': movies }, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch box-office movies"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# 최근 개봉 영화 10개 조회
class NowPlaying(APIView):
    def get(self, request):
        url = f"{TMDB_BASE_URL}/movie/now_playing"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ko-KR",
            "region": "KR",
            "page": 1,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            movies = response.json().get("results", [])
            today = datetime.today().date()
            # 개봉일 기준 필터링 및 정렬
            filtered_movies = [
                movie for movie in movies 
                if "release_date" in movie and datetime.strptime(movie["release_date"], "%Y-%m-%d").date() <= today
            ]
            sorted_movies = sorted(
                filtered_movies,
                key=lambda x: x.get("release_date", ""),
                reverse=True  # 내림차순 정렬
            )
            return Response({'results': sorted_movies[:10]}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch now playing movies"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def genre_movies(request):
    # 비로그인 시에는 랜덤으로 5개 장르를 선택하고 각 장르별로 10개씩 영화를 선택하여 반환
    # 로그인 시에는 사용자가 좋아요를 누르지 않은 장르 중 랜덤으로 1개를 선택하고 해당 장르의 영화를 10개씩 선택하여 반환
    # 이건 로그인 했을 때와 안 했을 때로 함수 자체를 나눠도 괜찮을 듯
    pass


def user_liked_actor(request):
    # 로그인 시 가능
    # 사용자가 좋아하는 배우 중 하나를 랜덤으로 뽑고 해당 배우의 영화를 랜덤으로 5개 뽑아서 반환
    pass


def user_liked_director(request):
    # 로그인 시 기능
    # 사용자가 좋아하는 감독 중 하나를 랜덤으로 뽑고 해당 배우의 영화를 랜덤으로 5개 뽑아서 반환
    pass


def user_liked_movies(request):
    # 로그인 시 기능
    # 사용자가 최근 좋아한 영화 5개 이내 조회
    pass


def user_liked_genre(request):
    # 로그인 시 기능
    # 사용자가 좋아하는 장르 중 하나를 랜덤으로 뽑고 해당 장르의 영화를 랜덤으로 5개 뽑아서 반환
    pass


def movie_detail(request, movie_id):
    # 영화 상세 정보 조회
    # 영화 상세 정보 api 요청이 한 번 있고
    # 그 후 해당 영화의 출연진에 대한 정보 api 요청이 한 번 있다.
    # 어느 엔드포인트로 보내야하는지는 GPT한테 물어보면 잘 알려준다.
    pass


def director_detail(request, director_id):
    # 감독 상세 정보 조회
    # 영화 상세 정보와 마찬가지로 감독 상세 정보 api 요청이 한 번 있고
    # 그 후 감독의 필모그래피에 대한 정보 api 요청이 한 번 있다.
    pass


def actor_detail(request, actor_id):
    # 배우 상세 정보 조회
    # 감독 상세 정보 조회와 거의 동일
    pass


def like_movie(request, movie_id):
    # 영화 좋아요 기능
    pass


def like_director(request, director_id):
    # 감독 좋아요 기능
    pass


def like_actor(request, actor_id):
    # 배우 좋아요 기능
    pass


def movie_reviews(request, movie_id):
    # 리뷰 조회 및 작성 기능
    pass


def update_movie_review(request, movie_id, review_id):
    # 리뷰 수정 및 삭제 기능
    pass


def like_review(request, movie_id, review_id):
    # 리뷰 좋아요 기능
    pass