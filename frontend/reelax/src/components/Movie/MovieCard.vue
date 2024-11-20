<template>
  <div class="top-rated-movie" v-if="movie">
    <img :src="`${imgBaseUrl}/${movie.poster_path}`" alt="영화 포스터">
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  movie: Object
})

const imgBaseUrl = ref('https://image.tmdb.org/t/p/w200')
</script>

<style scoped>
</style>