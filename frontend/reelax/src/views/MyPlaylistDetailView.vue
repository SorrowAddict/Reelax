<template>
  <div v-if="currentPlaylist" class="container">
    <div>
      <h1 class="current-title">{{ currentPlaylist.title }}</h1>
      <h4 class="current-description">{{ currentPlaylist.description }}</h4>
    </div>
    <div class="movies-grid">
      <div class="movie-item" v-for="movie in currentPlaylist.movies" :key="movie.movie_id">
        <MovieCard :movie="movie" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account'
import MovieCard from '@/components/Movie/MovieCard.vue'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()

const user_id = route.params.id
const playlist_id = route.params.playlist_id

const currentPlaylist = computed(() => {
  return accountStore.userInfo.playlists.find(
    playlist => playlist.id === Number(playlist_id)
  )
})

onMounted(() => {
  accountStore.getUserInfo(user_id)
})
</script>

<style scoped>
/* 영화 리스트 그리드 */
.movies-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 한 줄에 4개 */
  gap: 20px; /* 카드 간 간격 */
  margin-top: 20px;
}

/* 영화 카드 스타일 */
.movie-item {
  background-color: #2d2d2d;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* 제목 스타일 */
.current-title {
  margin-top: 20px;
  margin-bottom: 10px;
}

.current-description {
  margin-bottom: 30px;
  font-size: 16px;
}

/* 반응형 스타일 */
@media (max-width: 992px) {
  .movies-grid {
    grid-template-columns: repeat(3, 1fr); /* 한 줄에 3개 */
  }
}

@media (max-width: 768px) {
  .movies-grid {
    grid-template-columns: repeat(2, 1fr); /* 한 줄에 2개 */
  }
}

@media (max-width: 576px) {
  .movies-grid {
    grid-template-columns: repeat(1, 1fr); /* 한 줄에 1개 */
  }
}
</style>
