from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('top-rated/', TopRated.as_view()),
    path('popular/', popular.as_view()),
    path('now-playing/', NowPlaying.as_view()),
    path('genre-movies/', GenreMovies.as_view()),
    path('user-liked-actor/', views.user_liked_actor),
    path('user-liked-director/', views.user_liked_director),
    path('user-liked-movies/', views.user_liked_movies),
    path('user-liked-genre/', views.user_liked_genre),
    path('<int:movie_id>/', MovieDetail.as_view()),
    path('director/<int:director_id>/', DirectorDetail.as_view()),
    path('actor/<int:actor_id>/', ActorDetail.as_view()),
    path('like-movie/<int:movie_id>/', LikeMovie.as_view()),
    path('like-director/<int:director_id>/', views.like_director),
    path('like-actor/<int:actor_id>/', views.like_actor),
    path('<int:movie_id>/reviews/', MovieReviews.as_view()),
    path('<int:movie_id>/reviews/<int:review_id>/', views.update_movie_review),
    path('<int:movie_id>/reviews/<int:review_id>/like/', views.like_review),
    # 여기에 추가로 유저 마이페이지, 유저가 좋아한 영화, 감독, 배우 리스트 이런거 만들어야 하는데
    # 일단 졸려서 여기까지 해야겠다.
]

# 오전동안 해야될 일
# 기능별로 다 따로 만들었어 url -> 반환하는 정보가 매번 다르니까 이건 필요할 수도 있긴 할텐데
# 그냥 함수로 TMDB에 요청을 보내는 과정
# 그걸 반환값으로 받아서 실제 우리 서버 views에서는 받은 요청을 serialzer든 뭐든 이용해서 반환만 하는걸로
