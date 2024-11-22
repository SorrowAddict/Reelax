<template>
  <div v-if="movie" class="movie-card">
    <img
      @click="movieDetail(getMovieId(movie))"
      :src="movie.poster_path ? `${imgBaseUrl}/${movie.poster_path}` : defaultImage"
      alt="영화 포스터"
      class="movie-poster"
    />
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

const getMovieId = (movie) => {
  return movie.id || movie.movie_id; // id가 없으면 movieID 반환
}

const movieDetail = function (movieId) {
  router.push({ name: 'MovieDetailView', params: { id: movieId }})
}

const imgBaseUrl = ref('https://image.tmdb.org/t/p/w300')
const defaultImage = ref('/image/no_poster.jpg')

</script>

<style scoped>
.movie-card {
  width: 250px; /* 고정된 너비 */
  height: 375px; /* 고정된 높이 (비율에 맞게 설정) */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden; /* 넘치는 이미지를 숨김 */
  border-radius: 10px; /* 선택적으로 둥근 모서리 */
  background-color: #000; /* 이미지가 없을 경우 대비 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* 약간의 그림자 효과 */
}

/* 영화 포스터 이미지 */
.movie-poster {
  width: 100%; /* 컨테이너 너비에 맞춤 */
  height: 100%; /* 컨테이너 높이에 맞춤 */
  object-fit: cover; /* 이미지가 잘리지 않으면서 비율 유지 */
  border-radius: 10px; /* 모서리를 둥글게 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 부드러운 확대/축소 */
}

.movie-poster:hover {
  transform: scale(1.05); /* 살짝 확대 */
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.3); /* 확대 시 그림자 강조 */
}
</style>