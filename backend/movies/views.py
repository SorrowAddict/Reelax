# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.conf import settings
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


# 유저가 좋아요 한 영화 조회 [완]
class UserLikedMovies(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_movies = user.liked_movies.all()[:5]
        serializer = UserLikedMoviesSerializer(liked_movies, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)


# 영화 좋아요 기능 [완]
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


# 좋아요 한 배우를 기반으로 영화 5개 조회 [완]
class UserLikedActor(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_actors = user.liked_actors.all()
        if liked_actors:
            random_actor = random.choice(liked_actors)
            actor_id = random_actor.actorID
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


# 유저가 좋아요 한 감독을 기반으로 영화 5개 조회 [완]
class UserLikedDirector(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_directors = user.liked_directors.all()
        if liked_directors:
            random_director = random.choice(liked_directors)
            director_id = random_director.directorID
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


# 유저가 좋아요 한 장르를 기반으로 영화 5개 조회 [완]
class UserLikedGenreMovies(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_genres = user.liked_genres.all()
        if liked_genres:
            random_genre = random.choice(liked_genres)
            genre_id = random_genre.genreID
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


# director 좋아요 기능 [완]
class LikeDirector(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, director_id):
        user = request.user
        director, created = Director.objects.get_or_create(directorID=director_id)
        if created:
            director_url = f"{TMDB_BASE_URL}/person/{director_id}"
            params = {
                "api_key": TMDB_API_KEY,
                "language": "ko-KR",
            }
            response = requests.get(director_url, params=params)
            if response.status_code == 200:
                director_data = response.json()
                director.name = director_data.get("name", "Unknown Director")
                director.profile_path = director_data.get("profile_path", "")
                director.save()
            else:
                return Response(
                    {"error": "Failed to fetch director details from TMDB"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        if director in user.liked_directors.all():
            return Response({"message": "You already liked this director"}, status=status.HTTP_400_BAD_REQUEST)
        user.liked_directors.add(director)
        return Response({"message": "Director liked successfully"}, status=status.HTTP_200_OK)


# actor 좋아요 기능 [완]
class LikeActor(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, actor_id):
        user = request.user
        actor, created = Actor.objects.get_or_create(actorID=actor_id)
        user.liked_actors.add(actor)
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


# 영화 리뷰 수정 및 삭제 [완]
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


# 리뷰 좋아요 기능 [완]
class LikeReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id, review_id):
        review = Review.objects.get(id=review_id, movie_id=movie_id)
        review.liked_by.add(request.user)
        return Response({"message": "Review liked successfully"}, status=status.HTTP_200_OK)


# 장르 좋아요 기능 [완]
class LikeGenre(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        genre_ids = request.data.get("genre_ids", [])
        for genre_id in genre_ids:
            genre, created = Genre.objects.get_or_create(genreID=genre_id)
            user.liked_genres.add(genre)
        return Response({"message": "Genres liked successfully"}, status=status.HTTP_200_OK)
