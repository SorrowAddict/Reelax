# Python 3.9.13 버전 기반 이미지 사용
FROM python:3.9.13-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (필요한 경우)
RUN apt-get update && apt-get install -y libpq-dev gcc

# requirements.txt 파일을 컨테이너로 복사하고 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . /app/

# entrypoint.sh 복사 및 실행 권한 부여
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# 환경 변수 설정 (RDS에 대한 설정 필요시 추가)
ENV DATABASE_URL=postgresql://postgres:pwd1234!@reelax.cnuo8ouyklem.ap-northeast-2.rds.amazonaws.com:5432/reelax

# gunicorn을 사용하여 Django 애플리케이션 실행
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "reelax.wsgi:application"]

ENTRYPOINT ["sh", "/app/entrypoint.sh"]