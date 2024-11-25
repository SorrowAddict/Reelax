<template>
  <div class="movie-trailer-container">
    <div v-if="movieTrailer" class="movie-trailer-block">
      <!-- 영화 예고편 -->
      <iframe
        class="movie-trailer"
        :src="trailerUrl"
        frameborder="0"
        allow="autoplay; encrypted-media;"
        allowfullscreen
      ></iframe>

      <!-- 검은색 그라데이션 -->
      <div class="movie-trailer-overlay"></div>

      <!-- 영화 상세 정보 카드 -->
      <div class="movie-detail-card-overlay">
        <MovieDetailCard
          :movie="movie"
          :userInfo="userInfo"
          data-aos="fade-up"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed } from 'vue'
import MovieDetailCard from '@/components/MovieDetailPage/MovieDetailCard.vue'

const props = defineProps({
  title: String,
  movie: Object,
  userInfo: Object,
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
.movie-trailer-container {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 비율 */
  overflow: hidden;
}

.movie-trailer-block {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.movie-trailer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.movie-trailer-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle at 10% 90%,
    rgba(0, 0, 0, 0.9) 0%,
    rgba(0, 0, 0, 0.0) 70%
  );
  z-index: 2;
}

.movie-detail-card-overlay {
  position: absolute;
  bottom: 5%;
  left: 5%;
  z-index: 3;
  color: white;
}
</style>