<template>
  <div class="container" v-if="movieStore.movieDetail">
    <div v-if="!movieStore.movieDetailLoading && movieStore.movieDetail.title">
      <!-- 영화 예고편 -->
      <MovieTrailer
        :title="movieStore.movieDetail.title"
        :movie="movieStore.movieDetail"
        :userInfo="accountStore.userInfo || undefined"
        data-aos="fade-up"
      />
    </div>
    <div v-if="movie_id" data-aos="fade-up" data-aos-delay="150">
      <RouterLink :to="{ name: 'MovieCreditDefault', params: { id: movie_id } }">감독/출연진</RouterLink>
      <RouterLink :to="{ name: 'MovieReview', params: { id: movie_id } }">리뷰</RouterLink>
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie'
import { useAccountStore } from '@/stores/account'
import { onMounted } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router'
import MovieTrailer from '@/components/Movie/MovieTrailer.vue'
import AOS from 'aos'
import 'aos/dist/aos.css'

const movieStore = useMovieStore()
const accountStore = useAccountStore()
const route = useRoute()

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