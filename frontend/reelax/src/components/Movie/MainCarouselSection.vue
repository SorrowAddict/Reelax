<template>
  <div :id="carouselId" class="carousel slide movie-list" data-bs-ride="false">
    <div class="carousel-inner">
      <!-- 한 번에 5개의 포스터를 표시 -->
      <div
        class="carousel-item"
        v-for="(chunk, index) in chunkArray(movies, 5)"
        :key="index"
        :class="{ active: index === 0 }"
      >
        <div class="row gx-2 gy-3">
          <div class="col" v-for="movie in chunk" :key="movie.id">
            <MovieCard :movie="movie" />
          </div>
        </div>
      </div>
    </div>
    <!-- 이전/다음 버튼 -->
    <button
      class="carousel-control-prev"
      type="button"
      :data-bs-target="`#${carouselId}`"
      data-bs-slide="prev"
    >
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button
      class="carousel-control-next"
      type="button"
      :data-bs-target="`#${carouselId}`"
      data-bs-slide="next"
    >
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>

<script setup>
import MovieCard from "@/components/Movie/MovieCard.vue";

defineProps({
  carouselId: String,
  movies: Object
});

const chunkArray = (array, size) => {
  const chunks = [];
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size));
  }
  return chunks;
}
</script>

<style scoped>
.carousel {
  margin: 0; /* 좌우 여백 제거 */
  width: 100%; /* 화면 전체 너비 */
}

.carousel-wrapper {
  margin-left: -15px;
  margin-right: -15px;
  width: calc(100% + 30px); /* 여백만큼 확장 */
}

.carousel-control-prev,
.carousel-control-next {
  width: auto; /* 버튼 크기를 조정할 수 있도록 */
  transform: translateX(-30px); /* 이전 버튼을 왼쪽으로 이동 */
}

.carousel-control-next {
  transform: translateX(30px); /* 다음 버튼을 오른쪽으로 이동 */
}
</style>