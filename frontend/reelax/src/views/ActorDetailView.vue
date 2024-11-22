<template>
  <div>
    <div v-if="movieStore.actorDetail">
      <img :src="imageUrl" alt="프로필 이미지">
      <div>
        <h3>{{ movieStore.actorDetail.name }}</h3>
        <p>배우</p>
        <p>{{ birth_year }}</p>
        <p>{{ gender }}</p>
        <div v-if="accountStore.isLogin">
          <div @click="actorLike(movieStore.actorDetail.id, movieStore.actorDetail.name, movieStore.actorDetail.profile_path)">
            <div v-if="isActorLiked(movieStore.actorDetail)">
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
        <h2>{{ movieStore.actorDetail.name }}이 출연한 영화</h2>
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
import { useLikeStore } from '@/stores/like';

const movieStore = useMovieStore()
const accountStore = useAccountStore()
const likeStore = useLikeStore()
const route = useRoute()

const actor_id = route.params.actor_id

const defaultImage = "/image/basic_profile.png"
const imageUrl = computed(() => {
  if(movieStore.actorDetail.profile_path) {
    return `https://image.tmdb.org/t/p/w200${movieStore.actorDetail.profile_path}`
  } else {
    return `${defaultImage}`
  }
})

const birth_year = computed(() => {
  return movieStore.actorDetail.birthday.substring(0, 4)
})

const gender = computed(() => {
  if (movieStore.actorDetail.gender === 2) {
    return '남성'
  } else if (movieStore.actorDetail.gender === 1) {
    return '여성'
  } else {
    return '알 수 없음'
  }
})

const liked_actors = computed(() => accountStore.userInfo.liked_actors)

const isActorLiked = function (actor) {
  return liked_actors.value.some((liked_actor) => liked_actor.actor_id === actor.id)
}

const uniqueFilmography = computed(() => {
  const seenIds = new Set();
  return movieStore.actorDetail.filmography.filter((movie) => {
    if (!seenIds.has(movie.id)) {
      seenIds.add(movie.id);
      return true;
    }
    return false;
  });
});

const actorLike = function (actor_id, name, profile_path) {
  const payload = {
    actor_id: actor_id,
    name: name,
    profile_path: profile_path
  }
  likeStore.actorLike(payload)
}

onMounted(() => {
  movieStore.getActorDetail(actor_id)
  if (accountStore.isLogin) {
    accountStore.getUserInfo()
  }
})
</script>

<style scoped>

</style>