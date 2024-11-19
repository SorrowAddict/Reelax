<template>
  <div>
    <h1>영화 상세 페이지</h1>
    <div>여기에 영화 예고편이 들어갑니다.</div>
    <div>영화 상세 정보가 여기 들어갑니다.</div>
    <RouterLink :to="{ name: 'MovieCredit' }">감독/출연진</RouterLink>
    <RouterLink :to="{ name: 'MovieReview' }">리뷰</RouterLink>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>

</style>