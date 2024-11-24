<template>
  <div v-if="accountStore.userInfo" class="container">
    <h1 class="current-title">{{ accountStore.userInfo?.nickname || '사용자' }}님이 좋아한 영화</h1>
    <div class="movies-grid">
      <div class="movie-item" v-for="movie in accountStore.userInfo.liked_movies" :key="movie.movie_id">
        <MovieCard
          :movie="movie"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account';
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import MovieCard from '@/components/Movie/MovieCard.vue';

const route = useRoute();
const router = useRouter();
const user_id = route.params.id;
const accountStore = useAccountStore();


onMounted(() => {
  accountStore.getUserInfo(user_id);
});
</script>

<style scoped>
/* 영화 리스트 그리드 */
.movies-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 한 줄에 4개 고정 */
  gap: 20px; /* 카드 간 간격 */
  justify-content: center; /* 가운데 정렬 */
}

/* 영화 카드 스타일 */
.movie-item {
  background-color: #2d2d2d;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* 제목 스타일 */
.current-title {
  margin-top: 20px;
  margin-bottom: 30px;
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
