from django.urls import path
from .views import *

urlpatterns = [
    # 영화 조회
    path('top-rated/', TopRated.as_view()),
    path('popular/', popular.as_view()),
    path('now-playing/', NowPlaying.as_view()),
    path('genre-movies/', GenreMovies.as_view()),
    # 영화 상세 정보 조회
    path('<int:movie_id>/', MovieDetail.as_view()),
    path('actor/<int:actor_id>/', ActorDetail.as_view()),
    path('director/<int:director_id>/', DirectorDetail.as_view()),
    # 좋아요 한 (영화, 배우, 감독, 장르) 정보 조회
    path('user-liked-movies/', UserLikedMovies.as_view()),
    path('user-liked-actor/', UserLikedActor.as_view()),
    path('user-liked-director/', UserLikedDirector.as_view()),
    path('user-liked-genre/', UserLikedGenreMovies.as_view()),
    # review CRUD
    path('<int:movie_id>/reviews/', MovieReviews.as_view()),
    path('<int:movie_id>/reviews/<int:review_id>/', UpdateMovieReview.as_view()),
    # 커뮤니티 기능 (좋아요)
    path('like-movie/<int:movie_id>/', LikeMovie.as_view()),
    path('like-actor/<int:actor_id>/', LikeActor.as_view()),
    path('like-director/<int:director_id>/', LikeDirector.as_view()),
    path('like-genre/<int:genre_id>/', LikeGenre.as_view()),
    path('<int:movie_id>/reviews/<int:review_id>/like/', LikeReview.as_view()),
]
