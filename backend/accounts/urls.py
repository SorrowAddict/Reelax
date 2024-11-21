from django.urls import path, include
from . import views
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('profile/', Profile.as_view()),
    path('profile/update-image/', UpdateProfileImage.as_view())
]
