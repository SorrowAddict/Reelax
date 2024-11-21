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
  movie: Object
})

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