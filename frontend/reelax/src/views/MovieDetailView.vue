<template>
  <div>
    <div v-if="isLoading" class="spinner-container">
      <div class="spinner"></div>
    </div>
    <div class="container" v-if="movieStore.movieDetail && !isLoading">
      <div v-if="movieStore.movieDetail.title">
        <!-- 영화 예고편 -->
        <MovieTrailer
          :title="movieStore.movieDetail.title"
          :movie="movieStore.movieDetail"
          :userInfo="accountStore.userInfo || undefined"
          data-aos="fade-up"
        />
      </div>
      <div v-if="movie_id" data-aos="fade-up" data-aos-delay="150">
        <RouterLink :to="{ name: 'MovieCredit', params: { id: movie_id } }">감독/출연진</RouterLink>
        <RouterLink :to="{ name: 'MovieReview', params: { id: movie_id } }">리뷰</RouterLink>
        <RouterView />
      </div>
      <AddPlaylistModal 
        :movie="movieStore.movieDetail"
      />
    </div>
  </div>
  
</template>

<script setup>
import { useMovieStore } from '@/stores/movie'
import { useAccountStore } from '@/stores/account'
import { onMounted, ref, watch } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router'
import MovieTrailer from '@/components/MovieDetailPage/MovieTrailer.vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import AddPlaylistModal from '@/components/MovieDetailPage/AddPlaylistModal.vue'

const movieStore = useMovieStore()
const accountStore = useAccountStore()
const route = useRoute()
const isLoading = ref(true); // 로딩 상태 초기화

watch(
  () => movieStore.movieDetail, // movieStore.direcDetail 변화를 감시
  (newValue) => {
    if (newValue) {
      isLoading.value = false; // 데이터가 로드되면 로딩 상태를 false로 변경
    }
  }
);

const movie_id = route.params.id

onMounted(() => {
  movieStore.getMovieDetail(movie_id)
  if (accountStore.isLogin) {
    accountStore.getUserInfo(accountStore.userId)
  }
  AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: false,
  })
})

</script>

<style scoped>
.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

/* 스피너 애니메이션 */
.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #ccc; /* 회색 테두리 */
  border-top: 5px solid #007bff; /* 파란색 테두리 */
  border-radius: 50%; /* 원 모양 */
  animation: spin 1s linear infinite;
}

/* 애니메이션 키프레임 */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.director-page {
  background-color: #2d2d2d;
  min-height: 100vh;
  color: white;
}
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.container a {
  text-decoration: none;
  color: #1e90ff;
  font-weight: bold;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.container a:hover {
  background-color: rgba(30, 144, 255, 0.1);
  color: #00bfff;
}

.container > div[data-aos]:not(.movie-trailer-container) {
  margin-top: 30px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
}

</style>