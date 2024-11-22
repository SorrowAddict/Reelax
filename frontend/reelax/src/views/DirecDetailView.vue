<template>
  <div>
    <div>
      
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useMovieStore } from '@/stores/movie'
import { useAccountStore } from '@/stores/account'
import { useRoute } from 'vue-router'

const movieStore = useMovieStore()
const accountStore = useAccountStore()
const route = useRoute()

const direc_id = route.params.direc_id

const defaultImage = "/image/basic_profile.png"
const baseImageUrl = "https://image.tmdb.org/t/p/w200"
const imageUrl = `https://image.tmdb.org/t/p/w200/${movieStore}`

onMounted(() => {
  movieStore.getDirectorDetail(direc_id)
  accountStore.getUserInfo()
})

</script>

<style scoped>

</style>