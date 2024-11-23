<template>
  <div v-if="accountStore.userInfo">
    <h1>{{ accountStore.userInfo?.nickname || '사용자' }}님이 좋아한 영화</h1>
    <div>
      <div v-for="movie in accountStore.userInfo.liked_movies">
        <img @click="seeMovieDetail(movie.movie_id)" :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`" alt="">
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account'
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const user_id = route.params.id
const accountStore = useAccountStore()

const seeMovieDetail = function (movie_id) {
  router.push({ name: 'MovieDetailView', params: { id: movie_id }})
}

onMounted(() => {
  accountStore.getUserInfo(user_id)
})
</script>

<style scoped>

</style>