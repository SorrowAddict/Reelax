<template>
  <div class="container">
    <!-- 캐러셀 영역 -->
    <div class="carousel-wrapper">
      <div id="carouselExample" class="carousel slide" data-bs-ride="carousel" data-bs-interval="4000">
        <div class="carousel-inner">
          <div
            v-for="(image, index) in carouselImages"
            :key="index"
            :class="['carousel-item', { active: index === 0 }]"
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
    
    <!-- Top rated movie -->
    <div class="movie">
      <h3>좋은 평가를 받은 영화 TOP 10</h3>
      <MainCarouselSection
        carousel-id="topRatedCarousel"
        :movies="store.topRatedMovies"
      />
    </div>

    <div class="movie">
      <h3>박스 오피스 TOP 10</h3>
      <MainCarouselSection
        carousel-id="boxOfficeCarousel"
        :movies="store.boxOfficeMovies"
      />
    </div>

    <div class="movie">
      <h3>최근 개봉한 영화</h3>
      <MainCarouselSection
        carousel-id="recentlyReleasedCarousel"
        :movies="store.recentlyReleasedMovies"
      />
    </div>
  </div>
</template>

<script setup>
import MainCarouselSection from "@/components/Movie/MainCarouselSection.vue"
import { useMovieStore } from '@/stores/movie'
import { onMounted, ref } from 'vue'

const store = useMovieStore()

const carouselImages = ref([
  '/image/1.jpg',
  '/image/1.jpg',
  '/image/1.jpg',
  '/image/1.jpg',
])

onMounted(() => {
  store.getTopRatedMovies()
  store.getBoxOfficeMovies()
  store.getRecentlyReleasedMovies()
})
</script>

<style scoped>
.carousel-inner img {
  width: auto; /* 이미지 너비를 자동으로 설정 */
  height: auto; /* 이미지 높이를 자동으로 설정 */
  max-width: 100%; /* 이미지가 캐러셀 너비를 넘지 않도록 제한 */
  margin: 0 auto; /* 이미지를 중앙 정렬 */
  display: block; /* 블록 요소로 설정 */
  border-radius: 15px;
}

.carousel {
  margin: 0; /* 좌우 여백 제거 */
  width: 100%; /* 화면 전체 너비 */
}

.carousel-wrapper {
  margin-left: -15px;
  margin-right: -15px;
  width: calc(100% + 30px); /* 여백만큼 확장 */
}

.carousel-control-prev,
.carousel-control-next {
  width: auto; /* 버튼 크기를 조정할 수 있도록 */
  transform: translateX(-30px); /* 이전 버튼을 왼쪽으로 이동 */
}

.carousel-control-next {
  transform: translateX(30px); /* 다음 버튼을 오른쪽으로 이동 */
}

.movie {
  margin: 100px 0px;
}

.movie-list {
  margin: 20px 0px;
}
</style>