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
      <div v-if="accountStore.isLogin">
        <!-- 로그인 상태일 경우 -->
        <div @click="movieLike">
          <div v-if="isMovieLiked">
            <font-awesome-icon :icon="['fas', 'heart']" />
          </div>
          <div v-else>
            <font-awesome-icon :icon="['far', 'heart']" />
          </div>
        </div>
      </div>
      <div v-else>
        <div @click="moveToLogin">
          <font-awesome-icon :icon="['far', 'heart']" />
        </div>
      </div>
      <div v-if="accountStore.isLogin">
        <!-- 로그인 상태일 경우 -->
        <div data-bs-toggle="modal" data-bs-target="#addPlaylistModal">
          <font-awesome-icon :icon="['fas', 'plus']" />
        </div>
        <AddPlaylistModal 
          :movie="movie"
        />
      </div>
      <div v-else>
        <div @click="moveToLogin">
          <font-awesome-icon :icon="['fas', 'plus']" />
        </div>
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
import { useLikeStore } from '@/stores/like'
import { useAccountStore } from '@/stores/account'
import AddPlaylistModal from './AddPlaylistModal.vue'
import { useRouter } from 'vue-router'

library.add(faStar, faStarHalfAlt)

const props = defineProps({
  movie: Object,
  userInfo: Object
})
const likeStore = useLikeStore()
const accountStore = useAccountStore()
const router = useRouter()

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

const movieLike = function () {
  const payload = {
    movie_id: props.movie.movie_id,
    poster_path: props.movie.poster_path
  }
  likeStore.movieLike(payload)
}

const moveToLogin = function () {
  alert('로그인이 필요한 기능입니다.')
  router.push({ name: 'LoginPageView' })
}
</script>

<style scoped>
.movie-detail, .movie-rated {
  display: flex;
  gap: 10px;
}

.star {
  font-size: 24px;
  color: gold;
}
</style>