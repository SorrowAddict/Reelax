<template>
  <div v-if="accountStore.userInfo">
    <h1>{{ accountStore.userInfo?.nickname || '사용자' }}님이 좋아한 배우</h1>
    <div>
      <div v-for="actor in accountStore.userInfo.liked_actors">
        <img @click="seeDirectorDetail(actor.actor_id)" :src="`https://image.tmdb.org/t/p/w200/${actor.profile_path}`" alt="">
        <p>{{ actor.name }}</p>
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

const seeDirectorDetail = function (actor_id) {
  router.push({ name: 'ActorDetailView', params: { actor_id: actor_id }})
}

onMounted(() => {
  accountStore.getUserInfo(user_id)
})
</script>

<style scoped>

</style>