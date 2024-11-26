#!/bin/sh
# 엔트리포인트 스크립트

# 데이터베이스 마이그레이션 파일 생성
echo "Running makemigrations..."
python manage.py makemigrations

# 데이터베이스 마이그레이션 실행
echo "Applying database migrations..."
python manage.py migrate --noinput

# 데이터 로드
echo "Loading fixture data from genre_fixture.json..."
python manage.py loaddata genre_fixture.json

# Gunicorn 서버 시작
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 reelax.wsgi:application