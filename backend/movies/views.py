# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.conf import settings
from django.db import transaction
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
        params = {"api_key": TMDB_API_KEY, "language": "ko-KR", "page": 1}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            movies = response.json().get("results", [])[:10]
            return Response({'results': movies}, status=status.HTTP_200_OK)
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
        liked_genres = user.liked_genres.values_list('genre_id', flat=True)
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
    def get(self, request, movie_id):
        # 기존 영화 데이터 조회
        movie_instance = Movie.objects.filter(movie_id=movie_id).first()
        if movie_instance:
            # 이미 존재하는 데이터 반환
            serializer = MovieCreateSerializer(movie_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # TMDB API에서 데이터 가져오기
        movie_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        movie_params = {"api_key": TMDB_API_KEY, "language": "ko-KR"}
        movie_response = requests.get(movie_url, params=movie_params)

        if movie_response.status_code == 200:
            movie_data = movie_response.json()

            # 크레딧 데이터 가져오기
            credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
            credits_response = requests.get(credits_url, params=movie_params)
            if credits_response.status_code == 200:
                credits_data = credits_response.json()
                movie_data["credits"] = credits_data

            # 데이터 가공
            formatted_data = self.format_movie_data(movie_data)

            # 데이터 저장 또는 업데이트
            serializer = MovieCreateSerializer(data=formatted_data)
            serializer.is_valid(raise_exception=True)
            saved_movie = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # TMDB API 호출 실패
        return Response(
            {"error": "Failed to fetch movie details"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def format_movie_data(self, movie_data):
        """
        TMDB에서 가져온 데이터를 Django 모델 필드에 맞게 가공하는 함수
        """
        formatted_data = {
            "movie_id": movie_data.get("id"),
            "title": movie_data.get("title"),
            "overview": movie_data.get("overview"),
            "release_date": movie_data.get("release_date"),
            "popularity": movie_data.get("popularity"),
            "vote_average": movie_data.get("vote_average"),
            "vote_count": movie_data.get("vote_count"),
            "poster_path": movie_data.get("poster_path"),
            "backdrop_path": movie_data.get("backdrop_path"),
            "genres": movie_data.get("genres", []),
            "actors": [
                {
                    "id": actor.get("id"),
                    "name": actor.get("name"),
                    "profile_path": actor.get("profile_path"),
                }
                for actor in movie_data.get("credits", {}).get("cast", [])
            ],
            "directors": [
                {
                    "id": crew.get("id"),
                    "name": crew.get("name"),
                    "profile_path": crew.get("profile_path"),
                }
                for crew in movie_data.get("credits", {}).get("crew", [])
                if crew.get("job") == "Director"
            ],
            "additional_data": {
                "runtime": movie_data.get("runtime"),
                "spoken_languages": movie_data.get("spoken_languages"),
                "production_companies": movie_data.get("production_companies"),
                "production_countries": movie_data.get("production_countries"),
            },
        }
        return formatted_data


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
        liked_movies = user.liked_movies.all()
        serializer = UserLikedMoviesSerializer(liked_movies, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)


# 좋아요 한 배우를 기반으로 영화 5개 조회 [완]
class UserLikedActor(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_actors = user.liked_actors.all()
        if liked_actors:
            random_actor = random.choice(liked_actors)
            actor_id = random_actor.actor_id
            actor_name = random_actor.name
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
                return Response({'results': movies, 'name': actor_name}, status=status.HTTP_200_OK)
        return Response(
            {"results": {}, "error": "Failed to fetch liked actor movies"},
            status=status.HTTP_200_OK,
        )


# 유저가 좋아요 한 감독을 기반으로 영화 5개 조회 [완]
class UserLikedDirector(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_directors = user.liked_directors.all()
        if liked_directors:
            random_director = random.choice(liked_directors)
            director_id = random_director.director_id
            director_name = random_director.name
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
                return Response({'results': movies, 'name': director_name}, status=status.HTTP_200_OK)
        return Response(
            {"results": {}, "error": "Failed to fetch liked director movies"},
            status=status.HTTP_200_OK,
        )


# 유저가 좋아요 한 장르를 기반으로 영화 5개 조회 [완]
class UserLikedGenreMovies(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_genres = user.liked_genres.all()
        if liked_genres:
            random_genre = random.choice(liked_genres)
            genre_id = random_genre.genre_id
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
            {"results": {}, "error": "Failed to fetch liked genre movies"},
            status=status.HTTP_200_OK,
        )


# 영화 리뷰 조회 및 작성 [완]
class MovieReviews(APIView):
    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie_id=movie_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, movie_id):
        user = request.user
        data = request.data
        content = data.get("content")
        # Movie 객체 가져오기 또는 생성
        movie, created = Movie.objects.get_or_create(movie_id=movie_id, defaults={
            'poster_path': data.get('poster_path', '')
        })
        # 리뷰 작성
        review = Review.objects.create(user=user, movie=movie, content=content)
        return Response(
            {
                "id": review.id,
                "content": review.content,
                "movie": {"id": movie.movie_id, "poster_path": movie.poster_path},
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


# 영화 좋아요 및 취소 기능 [완]
class LikeMovie(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        movie_data = request.data
        movie_id = movie_data.get('movie_id')
        # 1. Movie 객체 가져오기 또는 생성
        movie, created = Movie.objects.get_or_create(movie_id=movie_id, defaults={
            'poster_path': movie_data.get('poster_path', '')
        })
        # 3. 중복 좋아요 방지
        if user.liked_movies.filter(movie_id=movie_id).exists():
            user.liked_movies.remove(movie)
            return Response({"message": "Movie unliked successfully"}, status=status.HTTP_200_OK)
        # 4. 좋아요 추가
        user.liked_movies.add(movie)
        return Response({"message": "Movie liked successfully"}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        movie_data = request.data
        movie_id = movie_data.get('movie_id')
        # 사용자가 좋아요한 영화에 있는지 확인
        movie = user.liked_movies.filter(movie_id=movie_id).first()
        if not movie:
            return Response({"message": "You have not liked this movie"}, status=status.HTTP_400_BAD_REQUEST)
        # 좋아요 취소
        user.liked_movies.remove(movie)
        return Response({"message": "Movie unliked successfully"}, status=status.HTTP_200_OK)


# actor 좋아요 기능 [완]
class LikeActor(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        actor_data = request.data  # 프론트에서 전송된 데이터
        actor_id = actor_data.get('actor_id')
        # Actor 객체 가져오기 또는 생성
        actor, created = Actor.objects.get_or_create(actor_id=actor_id, defaults={
            'name': actor_data.get('name', 'Unknown Actor'),
            'profile_path': actor_data.get('profile_path', '')
        })
        # 중복 좋아요 방지
        if user.liked_actors.filter(actor_id=actor_id).exists():
            user.liked_actors.remove(actor)
            return Response({"message": "Actor unliked successfully"}, status=status.HTTP_200_OK)
        # 좋아요 추가
        user.liked_actors.add(actor)
        return Response({"message": "Actor liked successfully"}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        actor_id = request.data.get('actor_id')
        # 사용자가 좋아요한 배우인지 확인
        actor = user.liked_actors.filter(actor_id=actor_id).first()
        if not actor:
            return Response({"message": "You have not liked this actor"}, status=status.HTTP_400_BAD_REQUEST)
        # 좋아요 취소
        user.liked_actors.remove(actor)
        return Response({"message": "Actor unliked successfully"}, status=status.HTTP_200_OK)


# director 좋아요 기능
class LikeDirector(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        director_data = request.data  # 프론트에서 전송된 데이터
        director_id = director_data.get('director_id')
        # Director 객체 가져오기 또는 생성
        director, created = Director.objects.get_or_create(director_id=director_id, defaults={
            'name': director_data.get('name', 'Unknown Director'),
            'profile_path': director_data.get('profile_path', '')
        })
        # 중복 좋아요 방지
        if user.liked_directors.filter(director_id=director_id).exists():
            user.liked_directors.remove(director)
            return Response({"message": "Director unliked successfully"}, status=status.HTTP_200_OK)
        # 좋아요 추가
        user.liked_directors.add(director)
        return Response({"message": "Director liked successfully"}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        director_id = request.data.get('director_id')
        # 사용자가 좋아요한 감독인지 확인
        director = user.liked_directors.filter(director_id=director_id).first()
        if not director:
            return Response({"message": "You have not liked this director"}, status=status.HTTP_400_BAD_REQUEST)
        # 좋아요 취소
        user.liked_directors.remove(director)
        return Response({"message": "Director unliked successfully"}, status=status.HTTP_200_OK)


# 장르 좋아요 기능 [완]
class LikeGenre(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        genres_data = request.data.get("genres", [])  # 프론트에서 전송된 장르 데이터 리스트
        for genre_data in genres_data:
            genre_id = genre_data.get('genre_id')
            name = genre_data.get('name')
            # Genre 객체 가져오기 또는 생성
            genre, created = Genre.objects.get_or_create(
                genre_id=genre_id,
                defaults={'name': name}
            )
            # 좋아요 추가
            if not user.liked_genres.filter(genre_id=genre_id).exists():
                user.liked_genres.add(genre)
            else:
                pass
        return Response({"message": "Genres liked successfully"}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        genre_id = request.data.get("genre_id")  # 본문에서 genre_id 추출
        if not genre_id:
            return Response({"message": "genre_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        # 사용자가 좋아요한 장르인지 확인
        genre = user.liked_genres.filter(genre_id=genre_id).first()
        if not genre:
            return Response({"message": "You have not liked this genre"}, status=status.HTTP_400_BAD_REQUEST)
        # 좋아요 취소
        user.liked_genres.remove(genre)
        return Response({"message": "Genre unliked successfully"}, status=status.HTTP_200_OK)


# 리뷰 좋아요 기능 [완]
class LikeReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id, review_id):
        review = Review.objects.get(id=review_id, movie_id=movie_id)
        if request.user in review.liked_by.all():
            review.liked_by.remove(request.user)
            return Response({"message": "Review unliked successfully"}, status=status.HTTP)
        review.liked_by.add(request.user)
        return Response({"message": "Review liked successfully"}, status=status.HTTP_200_OK)


# 플레이리스트 CRUD [완]
class UserPlaylists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        playlists = Playlist.objects.filter(user=user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user  # 요청한 사용자
        data = request.data
        serializer = PlaylistSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            # Playlist 생성 및 User와 연결
            playlist = serializer.save(user=user)
            user.playlists.add(playlist)  # ManyToMany 관계에 추가
            # Many-to-Many 관계의 movies 추가
            movie_ids = data.get('movies', [])
            if movie_ids:
                movies = Movie.objects.filter(movie_id__in=movie_ids)
                playlist.movies.set(movies)
            playlist.save()
            return Response({'results': PlaylistSerializer(playlist).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateDeletePlaylist(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, playlist_id):
        user = request.user
        try:
            playlist = Playlist.objects.get(id=playlist_id, user=user)
        except Playlist.DoesNotExist:
            return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'results': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, playlist_id):
        user = request.user
        try:
            playlist = Playlist.objects.get(id=playlist_id, user=user)
        except Playlist.DoesNotExist:
            return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)
        
        playlist.delete()
        return Response({"message": "Playlist deleted successfully"}, status=status.HTTP_200_OK)


# 플레이리스트에 영화 추가 [완]
class PlaylistMovies(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, playlist_id):
        user = request.user
        try:
            playlist = Playlist.objects.get(id=playlist_id, user=user)
        except Playlist.DoesNotExist:
            return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)
        movies = playlist.movies.all()
        serializer = MovieSerializer(movies, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, playlist_id):
        user = request.user
        try:
            playlist = Playlist.objects.get(id=playlist_id, user=user)
        except Playlist.DoesNotExist:
            return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        movie_ids = data.get('movies', [])
        if movie_ids:
            movies = Movie.objects.filter(movie_id__in=movie_ids)
            playlist.movies.add(*movies)
        return Response({"message": "Movies added to playlist successfully"}, status=status.HTTP_200_OK)
    
    def delete(self, request, playlist_id):
        user = request.user
        try:
            playlist = Playlist.objects.get(id=playlist_id, user=user)
        except Playlist.DoesNotExist:
            return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        movie_ids = data.get('movies', [])
        if movie_ids:
            movies = Movie.objects.filter(movie_id__in=movie_ids)
            playlist.movies.remove(*movies)
        return Response({"message": "Movies removed from playlist successfully"}, status=status.HTTP_200_OK)


class SearchMovies(APIView):
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ko-KR",
            "query": query,
            "page": 1,
            "include_adult": False
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            serializer = MovieSearchSerializer(data['results'], many=True)
            return Response({'results': serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"error": "Failed to fetch search results"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateGenres(APIView):
    def get(self, request):
        # TMDB API 호출 URL 및 파라미터 설정
        url = f"{TMDB_BASE_URL}/genre/movie/list"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ko-KR"
        }
        response = requests.get(url, params=params)

        # API 요청 성공 시 데이터 저장
        if response.status_code == 200:
            genres = response.json().get("genres", [])
            for genre_data in genres:
                # 데이터 저장 또는 업데이트
                Genre.objects.update_or_create(
                    genre_id=genre_data["id"],
                    defaults={"name": genre_data["name"]}
                )

            return Response(
                {"message": "Genres successfully updated.", "count": len(genres)},
                status=status.HTTP_200_OK
            )

        # API 요청 실패 시 에러 반환
        return Response(
            {"error": "Failed to fetch genres from TMDB."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
