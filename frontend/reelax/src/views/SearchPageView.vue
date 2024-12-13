<template>
  <div class="search-page container py-4">
    <div v-if="searchError" class="alert alert-danger text-center">
      {{ searchError }}
    </div>
    <div v-else-if="!searchResults || searchResults.length === 0" class="text-center">
      <p>"{{ searchQuery }}"로 검색하신 작품은 현재 Reelax에 없어요.</p>
    </div>
    <div v-else>
      <div class="row">
        <!-- 영화 카드 -->
        <div class="col-6 col-sm-4 col-md-3 col-lg-2 mb-4" v-for="(item, index) in searchResults" :key="index" data-aos="fade-up">
          <router-link :to="getRouterLink(item)" class="movie-card">
            <!-- 영화 포스터 -->
            <img
              :src="getPosterUrl(item.poster_path, item.profile_path)"
              alt="Movie Poster"
              class="img-fluid rounded shadow-sm movie-poster"
            />
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSearchStore } from '@/stores/search'
import { storeToRefs } from 'pinia'
import { watchEffect, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AOS from 'aos'
import 'aos/dist/aos.css'

onMounted(() => {
  AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: false,
  })
})

const store = useSearchStore()
const { searchResults, searchQuery, searchError } = storeToRefs(store)
const route = useRoute()

// TMDB 포스터 URL 생성 함수
const getPosterUrl = (posterPath, profilePath) => {
  const baseUrl = 'https://image.tmdb.org/t/p/w500'
  if (posterPath) {
    return `${baseUrl}${posterPath}`
  }
  if (profilePath) {
    return `${baseUrl}${profilePath}`
  }
  return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNNLEL-qmmLeFR1nxJuepFOgPYfnwHR56vcw&s'
}

// 검색 타입에 따라 router path를 다르게 설정하는 함수
const getRouterLink = (item) => {
  if (route.query.type === 'movies') {
    return { name: 'MovieDetailView', params: { id: item.id }}
  }
  else if (route.query.type === 'people') {
    if (item.known_for_department === 'Directing') {
      return { name: 'DirecDetailView', params: { direc_id: item.id }}
    }
    else if (item.known_for_department === 'Acting') {
      return { name: 'ActorDetailView', params: { actor_id: item.id }}
    }
  }
}

// 라우트 변경 감지 및 검색 실행
watchEffect(() => {
  const query = route.query.q
  const type = route.query.type
  console.log(query, type)
  if (query) {
    store.fetchSearchResults(query, type)
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
  transform: scale(1.10); /* 카드 확대 */
  border: 2px solid white; /* 흰색 테두리 */
}

/* 영화 포스터 */
.movie-poster {
  width: 100%;
  height: auto;
  border-radius: 8px;
  display: block;
}
</style>
