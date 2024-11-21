from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    genreID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)


class Movie(models.Model):
    movieID = models.BigIntegerField(primary_key=True)  # TMDB의 고유 ID
    title = models.CharField(max_length=255, null=False, blank=True)  # 영화 제목
    overview = models.TextField(null=True, blank=True)  # 영화 설명
    release_date = models.DateField(null=True, blank=True)  # 개봉일
    popularity = models.FloatField(null=True, blank=True)  # 인기 점수
    vote_average = models.FloatField(null=True, blank=True)  # 평균 평점
    vote_count = models.IntegerField(null=True, blank=True)  # 평점 수
    poster_path = models.CharField(max_length=225, null=True, blank=True)  # 포스터 이미지 경로
    backdrop_path = models.CharField(max_length=225, null=True, blank=True)  # 배경 이미지 경로
    genres = models.ManyToManyField('Genre', related_name='movies')  # 장르와의 다대다 관계
    actors = models.ManyToManyField('Actor', related_name='movies')  # 출연진
    directors = models.ManyToManyField('Director', related_name='movies')  # 제작진
    additional_data = models.JSONField(null=True, blank=True)  # 추가 데이터 저장

    def __str__(self):
        return self.title


class Actor(models.Model):
    actorID = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Director(models.Model):
    directorID = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_reviews')

    def __str__(self):
        return self.content

class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    movies = models.ManyToManyField("Movie", related_name='playlists')

    def __str__(self):
        return self.title
