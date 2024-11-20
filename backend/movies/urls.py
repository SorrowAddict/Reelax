from django.urls import path
from . import views

urlpatterns = [
    path('top-rated/', views.top_rated_movies, name='top_rated_movies'),
    path('box-office/', views.box_office_movies, name='box_office_movies'),
    path('recently-released/', views.recently_released_movies, name='recently_released_movies'),
    path('genre-movies/', views.genre_movies, name='genre_movies'),
    path('user-liked-actor/', views.user_liked_actor, name='user_liked_actor'),
    path('user-liked-director/', views.user_liked_director, name='user_liked_director'),
    path('user-liked-movies/', views.user_liked_movies, name='user_liked_movies'),
    path('user-liked-genre/', views.user_liked_genre, name='user_liked_genre'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('director/<int:director_id>/', views.director_detail, name='director_detail'),
    path('actor/<int:actor_id>/', views.actor_detail, name='actor_detail'),
    path('like-movie/<int:movie_id>/', views.like_movie, name='like_movie'),
    path('like-director/<int:director_id>/', views.like_director, name='like_director'),
    path('like-actor/<int:actor_id>/', views.like_actor, name='like_actor'),
    path('<int:movie_id>/reviews/', views.movie_reviews, name='movie_reviews'),
    path('<int:movie_id>/reviews/<int:review_id>/', views.update_movie_review, name='update_movie_review'),
    path('<int:movie_id>/reviews/<int:review_id>/like/', views.like_review, name='like_review'),
    # 여기에 추가로 유저 마이페이지, 유저가 좋아한 영화, 감독, 배우 리스트 이런거 만들어야 하는데
    # 일단 졸려서 여기까지 해야겠다.
]
