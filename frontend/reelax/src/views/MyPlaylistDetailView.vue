<template>
  <div v-if="currentPlaylist">
    <div>
      <h1>{{ currentPlaylist.title }}</h1>
      <h3>{{ currentPlaylist.description }}</h3>
    </div>
    <div class="movies">
      <div v-for="movie in currentPlaylist.movies">
        <img @click="seeMovieDetail(movie.movie_id)" :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`" alt="">
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()

const user_id = route.params.id
const playlist_id = route.params.playlist_id

const currentPlaylist = computed(() => {
  return accountStore.userInfo.playlists.find(
    playlist => playlist.id === Number(playlist_id)
  )
})

const seeMovieDetail = function (movie_id) {
  router.push({ name: 'MovieDetailView', params: { id: movie_id }})
}

onMounted(() => {
  accountStore.getUserInfo(user_id)
  console.log(accountStore.userInfo)
})
</script>

<style scoped>
.movies {
  display: flex;
}
</style>