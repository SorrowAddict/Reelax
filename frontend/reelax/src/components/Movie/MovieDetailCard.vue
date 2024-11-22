<template>
  <div>
    <div>
      <h1>{{ movie.title }}</h1>
    </div>
    <div class="movie-detail">
      <p>{{ release_year }}</p>
      <p>상영시간</p>
      <p>장르</p>
      <p>국가?</p>
    </div>
    <div class="movie-rated">
      <div>
        <font-awesome-icon
          v-for="star in 5"
          :key="star"
          :icon="['fas', star <= convertedRating ? 'star' : 'star-half-alt']"
          class="star"
        />
      </div>
      <p>{{ movie.vote_average }}</p>
      <div v-if="isMovieLiked">
        <font-awesome-icon :icon="['fas', 'heart']" />
      </div>
      <div v-else>
        <font-awesome-icon :icon="['far', 'heart']" />
      </div>
    </div>
    <div class="movie-overview">
      <p>
        {{ isExpanded ? movie.overview : truncatedOverview }}
        <button @click="toggleExpand">
          {{ isExpanded ? "간략히" : "더보기" }}
        </button>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faStar, faStarHalfAlt } from '@fortawesome/free-solid-svg-icons'
import { library } from "@fortawesome/fontawesome-svg-core"

library.add(faStar, faStarHalfAlt)

const props = defineProps({
  movie: Object,
  userInfo: Object
})

const liked_movies = computed(() => props.userInfo.liked_movies)

const isMovieLiked = computed(() => {
  return liked_movies.value.some((liked_movie) => liked_movie.movie_id === props.movie.movie_id)
})

const isExpanded = ref(false); // 줄거리를 확장할지 여부

// 일부만 보여줄 줄거리 계산
const truncatedOverview = computed(() => {
  if (!props.movie.overview) return ""; // 줄거리가 없을 경우 빈 문자열 반환
  return props.movie.overview.length > 50
    ? props.movie.overview.substring(0, 50) + "..."
    : props.movie.overview;
});

// 줄거리 확장/축소 상태 변경
const toggleExpand = () => {
  isExpanded.value = !isExpanded.value;
};

const release_year = computed(() => {
  return props.movie.release_date.substring(0, 4)
})

const convertedRating = computed(() => {
  return Math.min((props.movie.vote_average / 10) * 5, 5)
})
</script>

<style scoped>
.movie-detail, .movie-rated {
  display: flex;
}

.movie-detail>p, .movie-rated>p {
  padding: 0px 5px;
}

.star {
  font-size: 24px;
  color: gold;
}
</style>