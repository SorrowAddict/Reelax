from django.urls import path, include
from . import views
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', include('dj_rest_auth.registration.urls')),
    path('', include('allauth.urls')),
    path('google/login', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
    path('profile/<int:user_id>/', Profile.as_view()),
    path('profile/update-image/', UpdateProfileImage.as_view()),
    path('follow-toggle/<int:user_id>/', FollowToggle.as_view()),
]