<template>
  <div>
    <h1>메인 페이지</h1>
    <div>
      여기에 커다란 영화 이미지가 들어갑니다. 랜덤으로! 형태는 carousels!
    </div>
    <div>
      <h3>좋은 평가를 받은 영화 TOP 10</h3>
      <MovieCard />
    </div>
    <div>
      <h3>박스오피스 TOP 10</h3>
      <MovieCard />
    </div>
    <div>
      <h3>최근 개봉한 영화</h3>
      <MovieCard />
    </div>
  </div>
</template>

<script setup>
import MovieCard from '@/components/Movie/MovieCard.vue'
</script>

<style scoped>

</style>