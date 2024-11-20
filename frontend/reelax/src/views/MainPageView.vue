<template>
  <div>
    <h1>메인 페이지</h1>
    <div>
      여기에 커다란 영화 이미지가 들어갑니다. 랜덤으로! 형태는 carousels!
    </div>
    <div>
      <h3>좋은 평가를 받은 영화 TOP 10</h3>
      <div class="top-rated-movie">
        <MovieCard
        v-for="movie in store.topRatedMovies"
        :key="movie.id"
        :movie="movie"
      />
      </div>
    </div>
    <div>
      <h3>박스오피스 TOP 10</h3>
      <div class="top-rated-movie">
        <MovieCard
          v-for="movie in store.boxOfficeMovies"
          :key="movie.id"
          :movie="movie"
        />
      </div>
    </div>
    <div>
      <h3>최근 개봉한 영화</h3>
      <div class="top-rated-movie">
        <MovieCard
          v-for="movie in store.recentlyReleasedMovies"
          :key="movie.id"
          :movie="movie"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import MovieCard from '@/components/Movie/MovieCard.vue'
import { useMovieStore } from '@/stores/movie'
import { onMounted } from 'vue'

const store = useMovieStore()

onMounted(() => {
  store.getTopRatedMovies()
  store.getBoxOfficeMovies()
  store.getRecentlyReleasedMovies()
})
</script>

<style scoped>
.top-rated-movie {
  display: flex;
  flex-wrap: wrap;
}
</style>