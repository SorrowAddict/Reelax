<template>
  <div v-if="movie">
    <img @click="movieDetail(movie.id)" :src="`${imgBaseUrl}/${movie.poster_path}`" alt="영화 포스터">
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const store = useMovieStore()
const router = useRouter()

defineProps({
  movie: Object
})

const movieDetail = function (movieId) {
  router.push({ name: 'MovieDetailView', params: { id: movieId }})
}

const imgBaseUrl = ref('https://image.tmdb.org/t/p/w200')
</script>

<style scoped>
</style>