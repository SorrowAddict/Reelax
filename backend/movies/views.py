# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Genre, Movie, Director, Actor, Review
from .serializers import *

import requests
from datetime import datetime
import random

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_READ_ACCESS_TOKEN = settings.TMDB_READ_ACCESS_TOKEN
YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY

# Create your views here.
# TMDB API에서 평점 상위 10개 영화 조회 [완]
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


# 현재 박스오피스 상위 10개 영화 조회 [완]
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


# 최근 개봉 영화 10개 조회 [완]
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


# 좋아요 하지 않은 장르 반환 [완]
class GenreMovies(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        if request.user.is_authenticated:
            return self.get_user_genre_movies(request)
        else:
            return self.get_random_genre_movies()

    def get_random_genre_movies(self):
        url = f"{TMDB_BASE_URL}/genre/movie/list"
        params = { "api_key": TMDB_API_KEY, "language": "ko-KR" }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            genres = response.json().get("genres", [])
            random_genres = random.sample(genres, 5)
            genre_movies = {}
            for genre in random_genres:
                genre_id = genre["id"]
                genre_name = genre["name"]
                movies_url = f"{TMDB_BASE_URL}/discover/movie"
                movies_params = {
                    "api_key": TMDB_API_KEY,
                    "language": "ko-KR",
                    "with_genres": genre_id,
                    "page": 1,
                }
                movies_response = requests.get(movies_url, params=movies_params)
                if movies_response.status_code == 200:
                    movies = movies_response.json().get("results", [])[:10]
                    genre_movies[genre_name] = movies
            return Response({'results': genre_movies}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch genres"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def get_user_genre_movies(self, request):
        # 로그인 사용자: 좋아요를 누르지 않은 장르 중 하나를 랜덤 선택해 영화 반환
        user = request.user
        liked_genres = user.liked_genres.values_list('genreID', flat=True)

        # TMDB API로 모든 장르 가져오기
        all_genres_url = f"{TMDB_BASE_URL}/genre/movie/list"
        all_genres_params = {"api_key": TMDB_API_KEY, "language": "ko-KR"}
        all_genres_response = requests.get(all_genres_url, params=all_genres_params)
        if all_genres_response.status_code == 200:
            all_genres = all_genres_response.json().get("genres", [])
            not_liked_genres = [genre for genre in all_genres if genre["id"] not in liked_genres]
            if not_liked_genres:
                random_genre = random.choice(not_liked_genres)
                genre_id = random_genre["id"]
                genre_name = random_genre["name"]

                # 해당 장르의 영화 가져오기
                movies_url = f"{TMDB_BASE_URL}/discover/movie"
                movies_params = {
                    "api_key": TMDB_API_KEY,
                    "language": "ko-KR",
                    "with_genres": genre_id,
                    "page": 1,
                }
                movies_response = requests.get(movies_url, params=movies_params)
                if movies_response.status_code == 200:
                    movies = movies_response.json().get("results", [])[:10]
                    return Response({"results": {genre_name: movies}}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch user genre movies"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


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


class UserLikedActor(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_actors = user.profile.liked_actors.all()
        if liked_actors:
            random_actor = random.choice(liked_actors)
            actor_id = random_actor.id
            movies_url = f"{TMDB_BASE_URL}/discover/movie"
            movies_params = {
                "api_key": TMDB_API_KEY,
                "language": "ko-KR",
                "with_cast": actor_id,
                "page": 1,
            }
            movies_response = requests.get(movies_url, params=movies_params)
            if movies_response.status_code == 200:
                movies = movies_response.json().get("results", [])[:5]
                return Response({'results': movies}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch liked actor movies"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class UserLikedDirector(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_directors = user.profile.liked_directors.all()
        if liked_directors:
            random_director = random.choice(liked_directors)
            director_id = random_director.id
            movies_url = f"{TMDB_BASE_URL}/discover/movie"
            movies_params = {
                "api_key": TMDB_API_KEY,
                "language": "ko-KR",
                "with_crew": director_id,
                "page": 1,
            }
            movies_response = requests.get(movies_url, params=movies_params)
            if movies_response.status_code == 200:
                movies = movies_response.json().get("results", [])[:5]
                return Response({'results': movies}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch liked director movies"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class UserLikedMovies(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_movies = user.profile.liked_movies.all()[:5]
        movies = [{"id": movie.id, "title": movie.title} for movie in liked_movies]
        return Response({'results': movies}, status=status.HTTP_200_OK)


class UserLikedGenre(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_genres = user.profile.liked_genres.all()
        if liked_genres:
            random_genre = random.choice(liked_genres)
            genre_id = random_genre.id
            genre_name = random_genre.name
            movies_url = f"{TMDB_BASE_URL}/discover/movie"
            movies_params = {
                "api_key": TMDB_API_KEY,
                "language": "ko-KR",
                "with_genres": genre_id,
                "page": 1,
            }
            movies_response = requests.get(movies_url, params=movies_params)
            if movies_response.status_code == 200:
                movies = movies_response.json().get("results", [])[:5]
                return Response({'results': {genre_name: movies}}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch liked genre movies"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# 영화 상세 정보 조회 [완]
class MovieDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        movie_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        movie_params = {"api_key": TMDB_API_KEY, "language": "ko-KR"}
        movie_response = requests.get(movie_url, params=movie_params)
        if movie_response.status_code == 200:
            movie_detail = movie_response.json()
            credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
            credits_response = requests.get(credits_url, params=movie_params)
            if credits_response.status_code == 200:
                movie_detail["credits"] = credits_response.json()
            return Response(movie_detail, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch movie details"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# 감독 상세 조회 [완]
class DirectorDetail(APIView):
    def get(self, request, director_id):
        director_url = f"{TMDB_BASE_URL}/person/{director_id}"
        director_params = {"api_key": TMDB_API_KEY, "language": "ko-KR"}
        director_response = requests.get(director_url, params=director_params)
        if director_response.status_code == 200:
            director_detail = director_response.json()
            filmography_url = f"{TMDB_BASE_URL}/person/{director_id}/movie_credits"
            filmography_response = requests.get(filmography_url, params=director_params)
            if filmography_response.status_code == 200:
                director_detail["filmography"] = filmography_response.json().get("crew", [])
            return Response(director_detail, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch director details"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# 배우 상세 조회 [완]
class ActorDetail(APIView):
    def get(self, request, actor_id):
        actor_url = f"{TMDB_BASE_URL}/person/{actor_id}"
        actor_params = {"api_key": TMDB_API_KEY, "language": "ko-KR"}
        actor_response = requests.get(actor_url, params=actor_params)
        if actor_response.status_code == 200:
            actor_detail = actor_response.json()
            filmography_url = f"{TMDB_BASE_URL}/person/{actor_id}/movie_credits"
            filmography_response = requests.get(filmography_url, params=actor_params)
            if filmography_response.status_code == 200:
                actor_detail["filmography"] = filmography_response.json().get("cast", [])
            return Response(actor_detail, status=status.HTTP_200_OK)
        return Response(
            {"error": "Failed to fetch actor details"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# 영화 좋아요 기능 
class LikeMovie(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, movie_id):
        user = request.user
        # 1. Movie 객체 가져오기 또는 생성
        movie, created = Movie.objects.get_or_create(movieID=movie_id)
        if created:
            # 2. TMDB API 호출하여 영화 정보 가져오기
            movie_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
            params = {
                "api_key": TMDB_API_KEY,
                "language": "ko-KR",
            }
            response = requests.get(movie_url, params=params)
            if response.status_code == 200:
                movie_data = response.json()
                movie.poster_path = movie_data.get("poster_path", "")
                movie.save()
            else:
                # TMDB API 호출 실패 시 에러 처리
                return Response(
                    {"error": "Failed to fetch movie details from TMDB"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        # 3. 중복 좋아요 방지
        if user.liked_movies.filter(movieID=movie_id).exists():
            return Response({"message": "You already liked this movie"}, status=status.HTTP_400_BAD_REQUEST)
        # 4. 좋아요 추가
        user.liked_movies.add(movie)
        return Response({"message": "Movie liked successfully"}, status=status.HTTP_200_OK)


class LikeDirector(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, director_id):
        user = request.user
        director, created = Director.objects.get_or_create(id=director_id)
        user.profile.liked_directors.add(director)
        return Response({"message": "Director liked successfully"}, status=status.HTTP_200_OK)


class LikeActor(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, actor_id):
        user = request.user
        actor, created = Actor.objects.get_or_create(id=actor_id)
        user.profile.liked_actors.add(actor)
        return Response({"message": "Actor liked successfully"}, status=status.HTTP_200_OK)


# 영화 리뷰 조회 및 작성 [완]
class MovieReviews(APIView):
    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie_id=movie_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, movie_id):
        user = request.user
        content = request.data.get("content")
        movie, created = Movie.objects.get_or_create(movieID=movie_id)

        if created:
            # 2. TMDB API 호출하여 영화 정보 가져오기
            movie_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
            params = {
                "api_key": TMDB_API_KEY,
                "language": "ko-KR",
            }
            response = requests.get(movie_url, params=params)

            if response.status_code == 200:
                movie_data = response.json()
                # 3. 영화 데이터를 저장
                movie.poster_path = movie_data.get("poster_path", "")
                movie.save()
            else:
                return Response(
                    {"error": "Failed to fetch movie details from TMDB"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # 4. 리뷰 작성
        review = Review.objects.create(user=user, movie=movie, content=content)
        return Response(
            {
                "id": review.id,
                "content": review.content,
                "movie": {"id": movie.movieID, "poster_path": movie.poster_path},
            },
            status=status.HTTP_201_CREATED,
        )


class UpdateMovieReview(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, movie_id, review_id):
        review = Review.objects.get(id=review_id, movie_id=movie_id, user=request.user)
        review.content = request.data.get("content")
        review.save()
        return Response({"message": "Review updated successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, movie_id, review_id):
        review = Review.objects.get(id=review_id, movie_id=movie_id, user=request.user)
        review.delete()
        return Response({"message": "Review deleted successfully"}, status=status.HTTP_200_OK)


class LikeReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id, review_id):
        review = Review.objects.get(id=review_id, movie_id=movie_id)
        review.likes.add(request.user)
        return Response({"message": "Review liked successfully"}, status=status.HTTP_200_OK)
