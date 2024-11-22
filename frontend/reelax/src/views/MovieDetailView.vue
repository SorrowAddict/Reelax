<template>
  <div class="container" v-if="movieStore.movieDetail">
    <h1>영화 상세 페이지</h1>
    <div>여기에 영화 예고편이 들어갑니다.</div>
    <div>
      <!-- 영화 예고편 -->
      <MovieTrailer
        :title="movieStore.movieDetail.title"
      />
    </div>
    <div>
      <!-- 영화 상세 정보 카드 -->
      <MovieDetailCard
        :movie="movieStore.movieDetail"
        :userInfo="accountStore.userInfo"
      />
    </div>
    <div>영화 상세 정보가 여기 들어갑니다.</div>
    <RouterLink :to="{ name: 'MovieCredit' }">감독/출연진</RouterLink>
    <RouterLink :to="{ name: 'MovieReview' }">리뷰</RouterLink>
    <RouterView />
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie'
import { useAccountStore } from '@/stores/account'
import { onMounted } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router'
import MovieDetailCard from '@/components/Movie/MovieDetailCard.vue'
import MovieTrailer from '@/components/Movie/MovieTrailer.vue'

const movieStore = useMovieStore()
const accountStore = useAccountStore()
const route = useRoute()

const movie_id = route.params.id

onMounted(() => {
  movieStore.getMovieDetail(movie_id)
})

</script>

<style scoped>

</style>