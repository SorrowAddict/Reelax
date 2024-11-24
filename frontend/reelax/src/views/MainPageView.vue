<template>
  <div class="container">
    <!-- 그라데이션 보더 -->
    <div class="gradient-border">
      <!-- 캐러셀 영역 -->
      <div class="carousel-wrapper" data-aos="zoom-in" data-aos-easing="ease-in-quint">
        <div id="carouselExample" class="carousel slide" data-bs-ride="carousel" data-bs-interval="4000">
          <div class="carousel-inner">
            <div
              v-for="(image, index) in carouselImages"
              :key="index"
              :class="['carousel-item', { active: index === 0 }]"
              @mouseover="updateGradient(image)"
            >
              <img :src="image" class="d-block w-100" alt="영화 이미지" />
            </div>
          </div>
          <!-- 캐러셀 이전/다음 버튼 -->
          <button
            class="carousel-control-prev"
            type="button"
            data-bs-target="#carouselExample"
            data-bs-slide="prev"
          >
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button
            class="carousel-control-next"
            type="button"
            data-bs-target="#carouselExample"
            data-bs-slide="next"
          >
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 로그인 한 상태일 때만 보여지는 영화 리스트들 -->
    <div v-if="accountStore.token !== null">
      <!-- 사용자가 좋아한 장르의 영화 -->
      <div v-if="movieStore.userLikedGenreMovies && Object.keys(movieStore.userLikedGenreMovies).length > 0" class="movie">
        <div v-for="(movies, genre) in movieStore.userLikedGenreMovies" :key="genre" data-aos="fade-right">
          <h3>사용자가 좋아한 {{ genre }} 영화</h3>
          <MainCarouselSection
            carousel-id="likedGenreCarousel"
            :movies="movies"
          />
        </div>
      </div>
      <div v-else class="movie">
        <h1>아직 좋아한 장르가 없습니다!</h1>
      </div>

      <!-- 사용자가 좋아한 최근 영화 -->
      <div v-if="movieStore.userLikedMovies && Object.keys(movieStore.userLikedMovies).length > 0" class="movie" data-aos="fade-left">
        <h3>사용자가 최근 좋아한 영화</h3>
        <MainCarouselSection
          carousel-id="likedMovieCarousel"
          :movies="movieStore.userLikedMovies"
        />
      </div>
      <div v-else class="movie">
        <h1>아직 좋아한 영화가 없습니다!</h1>
      </div>

      <!-- 유저가 좋아한 배우 중 랜덤으로 하나 뽑아서 필모 5개 표시 -->
      <div v-if="movieStore.userLikedActorMovies && Object.keys(movieStore.userLikedActorMovies).length > 0" class="movie" data-aos="fade-right">
        <h3>사용자가 좋아한 배우 {{ movieStore.userLikedActor }}의 영화</h3>
        <MainCarouselSection
          carousel-id="likedActorCarousel"
          :movies="movieStore.userLikedActorMovies"
        />
      </div>
      <div v-else class="movie">
        <h1>아직 좋아한 배우가 없습니다!</h1>
      </div>

      <!-- 유저가 좋아한 감독 중 랜덤으로 하나 뽑아서 필모 5개 표시 -->
      <div v-if="movieStore.userLikedDirecMovies && Object.keys(movieStore.userLikedDirecMovies).length > 0" class="movie" data-aos="fade-left">
        <h3>사용자가 좋아한 감독 {{ movieStore.userLikedDirec }}의 영화</h3>
        <MainCarouselSection
          carousel-id="likedDirecCarousel"
          :movies="movieStore.userLikedDirecMovies"
        />
      </div>
      <div v-else class="movie">
        <h1>아직 좋아한 감독이 없습니다!</h1>
      </div>
    </div>
    
    <!-- Top rated movie -->
    <div v-if="movieStore.topRatedMovies" class="movie" data-aos="fade-right">
      <h3>좋은 평가를 받은 영화 TOP 10</h3>
      <MainCarouselSection
        carousel-id="topRatedCarousel"
        :movies="movieStore.topRatedMovies"
      />
    </div>

    <div v-if="movieStore.boxOfficeMovies" class="movie" data-aos="fade-left">
      <h3>박스 오피스 TOP 10</h3>
      <MainCarouselSection
        carousel-id="boxOfficeCarousel"
        :movies="movieStore.boxOfficeMovies"
      />
    </div>

    <div v-if="movieStore.recentlyReleasedMovies" class="movie" data-aos="fade-right">
      <h3>최근 개봉한 영화</h3>
      <MainCarouselSection
        carousel-id="recentlyReleasedCarousel"
        :movies="movieStore.recentlyReleasedMovies"
      />
    </div>

    <div v-if="accountStore.token !== null && movieStore.genreMovies">
      <!-- 로그인 되어있는 상태 -->
      <div v-for="(movies, genre) in movieStore.genreMovies" :key="genre" class="movie" data-aos="fade-left">
        <h3>이런 영화는 어떠세요?</h3>
        <MainCarouselSection
          carousel-id="genreCarousel"
          :movies="movies"
        />
      </div>
    </div>
    <div v-else-if="accountStore.token === null && movieStore.genreMovies">
      <!-- 로그인 되어있지 않은 상태 -->
      <div v-for="(movies, genre) in movieStore.genreMovies" :key="genre" class="movie" data-aos="fade-left">
        <h3>당신이 좋아할만한 {{ genre }} 영화</h3>
        <MainCarouselSection
          carousel-id="genreCarousel"
          :movies="movies"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import MainCarouselSection from "@/components/MainPage/MainCarouselSection.vue"
import { useAccountStore } from "@/stores/account"
import { useMovieStore } from '@/stores/movie'
import { onMounted, ref } from 'vue'
import AOS from 'aos'
import 'aos/dist/aos.css'

const movieStore = useMovieStore()
const accountStore = useAccountStore()

const carouselImages = ref([
  '/image/1.jpg',
  '/image/2.jpg',
  '/image/3.jpg',
  '/image/4.jpg',
])

const gradientColors = ref("to right, #ff7e5f, #feb47b")

const updateGradient = (imageSrc) => {
  // 예: 이미지 경로에 따라 색상을 결정
  const colorMapping = {
    "/image/1.jpg": "to right, #ff7e5f, #feb47b",
    "/image/2.jpg": "to right, #6a11cb, #2575fc",
    "/image/3.jpg": "to right, #00c6ff, #0072ff",
    "/image/4.jpg": "to right, #ff9966, #ff5e62",
  }
  gradientColors.value = colorMapping[imageSrc] || "to right, #ff7e5f, #feb47b"
}

onMounted(() => {
  movieStore.getTopRatedMovies()
  movieStore.getBoxOfficeMovies()
  movieStore.getRecentlyReleasedMovies()
  movieStore.getGenreMovies()
  AOS.init({
    duration: 800,
    easing: 'ease-in-out-quint',
    mirror: 'true',
    once: false,
  })
  if (accountStore.isLogin) {
    // 로그인 되어있을 경우
    movieStore.getUserLikedGenreMovies()
    movieStore.getUserLikedMovies()
    movieStore.getUserLikedActorMovies()
    movieStore.getUserLikedDirecMovies()
  }
  
})
</script>

<style scoped>
.carousel-inner img {
  width: 100%;
  height: 500px;
  object-fit: cover;
  margin: 0 auto;
  display: block;
  border-radius: 30px;
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.carousel-wrapper {
  border-radius: 30px;
  margin: 2rem auto 0 auto;
  max-width: 1400px;
  overflow: hidden;
}

.carousel {
  width: 100%;
}

.carousel-control-prev,
.carousel-control-next {
  width: 40px;
  height: 40px;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
  background-color: rgba(0, 0, 0, 0.8);
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
  width: 20px;
  height: 20px;
}

.movie {
  margin: 50px 0px;
}

.movie-list {
  margin: 20px 0px;
}

.genre-movie {
  margin: 50px 0px;
}
</style>
