<template>
  <div class="nav-bar">
    <div class="home-link">
      <RouterLink :to="{ name: 'MainPageView' }">
        <img src="/image/logo_final.png" alt="Logo" height="60px" />
      </RouterLink>
    </div>
    <div class="w-25">
      <SearchBar class="mx-auto" />
    </div>
    <div class="account-link">
      <slot></slot> <!-- 상태에 따라 다른 콘텐츠를 표시 -->
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import SearchBar from '../Search/SearchBar.vue'
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
