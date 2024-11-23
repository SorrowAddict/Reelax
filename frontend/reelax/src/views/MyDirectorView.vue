<template>
  <div v-if="accountStore.userInfo">
    <h1>{{ accountStore.userInfo?.nickname || '사용자' }}님이 좋아한 감독</h1>
    <div>
      <div v-for="director in accountStore.userInfo.liked_directors">
        <img @click="seeDirectorDetail(director.director_id)" :src="`https://image.tmdb.org/t/p/w200/${director.profile_path}`" alt="">
        <p>{{ director.name }}</p>
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

const seeDirectorDetail = function (direc_id) {
  router.push({ name: 'DirecDetailView', params: { direc_id: direc_id }})
}

onMounted(() => {
  accountStore.getUserInfo(user_id)
})
</script>

<style scoped>

</style>