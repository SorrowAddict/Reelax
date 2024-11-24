<template>
  <div>
    <div v-if="movieTrailer" class="movie-trailer-block">
      <iframe class="movie-trailer" :src="trailerUrl" frameborder="0" allow="autoplay; encrypted-media;" allowfullscreen></iframe>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed } from 'vue'

const props = defineProps({
  title: String
})
const movieTrailer = ref(null)
const trailerUrl = computed(() => {
  if (movieTrailer.value) {
    return `https://www.youtube.com/embed/${movieTrailer.value.id.videoId}?autoplay=1&mute=1&controls=0`
  }
})
const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY2
onMounted(() => {
  axios({
    method: 'get',
    url: 'https://www.googleapis.com/youtube/v3/search',
    params: {
        part: 'snippet',
        q: `${props.title} 한국 공식 예고편`,
        type: 'video',
        key: API_KEY,
        maxResults: 1,
      }
  })
    .then((res) => {
        movieTrailer.value = res.data.items[0]
      })
    .catch((err) => {
      console.log(err)
    })

})
</script>

<style scoped>
.movie-trailer-block {
  width: 100%; /* 컨테이너 너비 설정 */
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
  height: 0;
  overflow: hidden;
}
.movie-trailer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%; /* 100% 너비 */
  height: 100%; /* 16:9 비율 유지 */
  pointer-events: none;
}
</style>