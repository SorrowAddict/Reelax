<template>
  <div>
    <div v-if="movieStore.movieDetail">
      출연진 및 감독
      <MovieDetailDirecCard
        :director="movieStore.movieDetail.directors"
        :userInfo="accountStore.userInfo"
      />
      <MovieDetailActorCard
        :actors="movieStore.movieDetail.actors"
        :userInfo="accountStore.userInfo"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router'
import MovieDetailActorCard from './MovieDetailActorCard.vue'
import MovieDetailDirecCard from './MovieDetailDirecCard.vue'
import { useAccountStore } from '@/stores/account'
import { useMovieStore } from '@/stores/movie'

const movieStore = useMovieStore()
const accountStore = useAccountStore()
const route = useRoute()

const movie_id = route.params.id

onMounted(() => {
  movieStore.getMovieDetail(movie_id)
  console.log(movieStore.movieDetail)
  accountStore.getUserInfo()
  console.log(accountStore.userInfo)
})
</script>

<style scoped>

</style>