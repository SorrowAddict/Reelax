<template>
  <div>
    <div class="playlist-thumbnail">
      <div class="poster-grid">
        <div
          v-for="(poster, index) in firstFourPosters"
          :key="index"
          class="poster"
          :style="{ backgroundImage: `url(${poster})` }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  movies: Object
})

// 앞 4개의 포스터 추출
const firstFourPosters = computed(() => {
  return props.movies.slice(0, 4).map(movie => {
    return `https://image.tmdb.org/t/p/w200/${movie.poster_path}`
  })
})
</script>

<style scoped>
/* 썸네일 컨테이너 */
.playlist-thumbnail {
  width: 200px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  border: 1px solid #ddd;
  border-radius: 8px;
}

/* 포스터 그리드 (2x2) */
.poster-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 2px; /* 포스터 사이 간격 */
  width: 100%;
  height: 100%;
}

/* 개별 포스터 */
.poster {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  border-radius: 4px;
}
</style>