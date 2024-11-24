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
  // console.log(movieStore.movieDetail)
  accountStore.getUserInfo(accountStore.userId)
  // console.log(accountStore.userInfo)
})
</script>

<style scoped>
div {
  padding: 20px;
  color: #ffffff;
  background-color: #1c1c1e;
  border-radius: 10px;
  margin: 20px 0;
}

h3 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #f4f4f4;
  margin-bottom: 15px;
  text-transform: uppercase;
  letter-spacing: 1.2px;
}

.MovieDetailDirecCard,
.MovieDetailActorCard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
}

.MovieDetailDirecCard div,
.MovieDetailActorCard div {
  background-color: #2b2b2e;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  color: #f4f4f4;
  transition: transform 0.3s, box-shadow 0.3s;
}

.MovieDetailDirecCard div:hover,
.MovieDetailActorCard div:hover {
  transform: translateY(-5px);
  box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.3);
}
</style>
