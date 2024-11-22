<template>
  <div>
    <div v-if="movieStore.direcDetail">
      <img :src="imageUrl" alt="프로필 이미지">
      <div>
        <h3>{{ movieStore.direcDetail.name }}</h3>
        <p>감독</p>
        <p>{{ birth_year }}</p>
        <p>{{ gender }}</p>
        <div v-if="accountStore.isLogin">
          <div @click="direcLike(movieStore.direcDetail.id, movieStore.direcDetail.name, movieStore.direcDetail.profile_path)">
            <div v-if="isDirectorLiked(movieStore.direcDetail)">
              <font-awesome-icon :icon="['fas', 'heart']" />
            </div>
            <div v-else>
              <font-awesome-icon :icon="['far', 'heart']" />
            </div>
          </div>
        </div>
        <div v-else>
          <font-awesome-icon :icon="['far', 'heart']" />
        </div>
      </div>
      <div>
        <h2>{{ movieStore.direcDetail.name }}이 연출한 영화</h2>
        <div>
          <MovieCard
            v-for="movie in uniqueFilmography"
            :key="movie.id"
            :movie="movie"
          />
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useMovieStore } from '@/stores/movie'
import { useAccountStore } from '@/stores/account'
import { useRoute } from 'vue-router'
import MovieCard from '@/components/Movie/MovieCard.vue'
import { useLikeStore } from '@/stores/like'

const movieStore = useMovieStore()
const accountStore = useAccountStore()
const likeStore = useLikeStore()
const route = useRoute()

const direc_id = route.params.direc_id

const defaultImage = "/image/basic_profile.png"
const imageUrl = computed(() => {
  if(movieStore.direcDetail.profile_path) {
    return `https://image.tmdb.org/t/p/w200${movieStore.direcDetail.profile_path}`
  } else {
    return `${defaultImage}`
  }
})

const birth_year = computed(() => {
  return movieStore.direcDetail.birthday.substring(0, 4)
})

const gender = computed(() => {
  if (movieStore.direcDetail.gender === 2) {
    return '남성'
  } else if (movieStore.direcDetail.gender === 1) {
    return '여성'
  } else {
    return '알 수 없음'
  }
})

const liked_directors = computed(() => accountStore.userInfo.liked_directors)

const isDirectorLiked = function (director) {
  return liked_directors.value.some((liked_director) => liked_director.director_id === director.id)
}

const uniqueFilmography = computed(() => {
  const seenIds = new Set();
  return movieStore.direcDetail.filmography.filter((movie) => {
    if (!seenIds.has(movie.id)) {
      seenIds.add(movie.id);
      return true;
    }
    return false;
  });
});

const direcLike = function (director_id, name, profile_path) {
  const payload = {
    director_id: director_id,
    name: name,
    profile_path: profile_path
  }
  likeStore.direcLike(payload)
}

onMounted(() => {
  movieStore.getDirectorDetail(direc_id)
  console.log(movieStore.direcDetail)
  if (accountStore.isLogin) {
    accountStore.getUserInfo()
  }
})

</script>

<style scoped>

</style>