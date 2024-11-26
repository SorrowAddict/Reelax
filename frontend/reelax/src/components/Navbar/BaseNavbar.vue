<template>
  <div class="nav-bar">
    <div class="home-link">
      <RouterLink :to="{ name: 'MainPageView' }">
        <img src="/image/logo_final.png" alt="Logo" height="60px" />
      </RouterLink>
    </div>

    <!-- 분류 선택 + 검색창을 감싸는 컨테이너 -->
    <div class="search-container">
      <div class="search-select-wrapper">
        <select v-model="selectedSearchType" class="form-select">
          <option value="movies">Movies</option>
          <option value="people">People</option>
          <option value="tv-shows">TV Shows</option>
        </select>
      </div>
      <div class="w-100 search-section">
        <SearchBar class="mx-auto" :selectedSearchType="selectedSearchType" />
      </div>
    </div>

    <div class="account-link">
      <slot></slot> <!-- 상태에 따라 다른 콘텐츠를 표시 -->
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import SearchBar from '../Search/SearchBar.vue'
import { ref } from 'vue'

const selectedSearchType = ref('movies')
</script>

<style scoped>
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  border-bottom: 1px solid rgb(100, 100, 100);
}

.home-link img {
  display: block;
  max-height: 60px;
}

/* 분류 선택과 검색창을 감싸는 컨테이너 */
.search-container {
  display: flex;
  align-items: center;
  gap: 10px; /* 간격을 제거 */
  width: 25%;
}

.search-select-wrapper {
  width: 100px;
}

.search-section {
  display: flex;
  align-items: center;
}

.account-link {
  display: flex;
  align-items: center;
  gap: 20px;
}

a {
  text-decoration: none;
  color: white;
}

a:hover {
  text-decoration: underline;
}
</style>
