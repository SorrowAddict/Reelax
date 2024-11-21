<template>
  <div class="container">
    <h1>영화 상세 페이지</h1>
    <div>여기에 영화 예고편이 들어갑니다.</div>
    <div>
      <!-- 영화 예고편 -->
      <MovieTrailer
        :title="store.movieDetail.title"
      />
    </div>
    <div>
      <!-- 영화 상세 정보 카드 -->
      <MovieDetailCard
        :movie="store.movieDetail"
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
import { onMounted } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router'
import MovieDetailCard from '@/components/Movie/MovieDetailCard.vue'
import MovieTrailer from '@/components/Movie/MovieTrailer.vue'

const store = useMovieStore()
const route = useRoute()

const movie_id = route.params.id

onMounted(() => {
  store.getMovieDetail(movie_id)
})

</script>

<style scoped>

</style>