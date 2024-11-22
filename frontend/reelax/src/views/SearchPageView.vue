<template>
  <div class="search-page container py-4">
    <h1 class="text-center mb-4">Search Results</h1>
    <div v-if="searchError" class="alert alert-danger text-center">
      {{ searchError }}
    </div>
    <div v-else-if="!searchResults || searchResults.length === 0" class="text-center">
      <p>No results found for "{{ searchQuery }}"</p>
    </div>
    <div v-else>
      <div class="row">
        <!-- 영화 카드 -->
        <div class="col-6 col-sm-4 col-md-3 col-lg-2 mb-4" v-for="(movie, index) in searchResults" :key="index">
          <router-link :to="{ name: 'MovieDetailView', params: { id: movie.id } }" class="movie-card">
            <!-- 영화 포스터 -->
            <img
              :src="getPosterUrl(movie.poster_path)"
              alt="Movie Poster"
              class="img-fluid rounded shadow-sm movie-poster"
            />
            <!-- 마우스오버 시 표시되는 설명 -->
            <div class="movie-overlay">
              <h5 class="movie-title">{{ movie.title }}</h5>
              <p class="movie-overview">{{ truncateText(movie.overview, 100) }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSearchStore } from '@/stores/search'
import { storeToRefs } from 'pinia'
import { watchEffect } from 'vue'
import { useRoute } from 'vue-router'

const store = useSearchStore()
const { searchResults, searchQuery, searchError } = storeToRefs(store)
const route = useRoute()

// TMDB 포스터 URL 생성 함수
const getPosterUrl = (posterPath) => {
  const baseUrl = 'https://image.tmdb.org/t/p/w500'
  return posterPath ? `${baseUrl}${posterPath}` : 'https://via.placeholder.com/500x750?text=No+Image'
}

// 텍스트 자르기 함수
const truncateText = (text, maxLength) => {
  if (!text) return 'No description available'
  return text.length > maxLength ? text.slice(0, maxLength) + '...' : text
}

// 라우트 변경 감지 및 검색 실행
watchEffect(() => {
  const query = route.query.q
  if (query) {
    store.fetchSearchResults(query)
  }
})
</script>

<style scoped>
/* 전체 페이지 스타일 */
.search-page {
  min-height: 100vh;
}

/* 영화 카드 컨테이너 */
.movie-card {
  position: relative;
  overflow: hidden;
  display: block;
  transition: transform 0.3s ease, border 0.3s ease;
  border-radius: 8px;
}

.movie-card:hover {
  transform: scale(1.05); /* 카드 확대 */
  border: 2px solid white; /* 흰색 테두리 */
}

/* 영화 포스터 */
.movie-poster {
  width: 100%;
  height: auto;
  border-radius: 8px;
  display: block;
}

/* 마우스오버 시 표시되는 오버레이 */
.movie-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  padding: 10px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.2)); /* 그라데이션 */
  color: white;
  opacity: 0; /* 초기에는 숨김 */
  transition: opacity 0.3s ease;
  border-radius: 8px;
}

.movie-card:hover .movie-overlay {
  opacity: 1; /* 마우스오버 시 표시 */
}

/* 영화 제목 */
.movie-title {
  font-size: 1rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 5px;
}

/* 영화 설명 */
.movie-overview {
  font-size: 0.8rem;
  text-align: center;
}
</style>
