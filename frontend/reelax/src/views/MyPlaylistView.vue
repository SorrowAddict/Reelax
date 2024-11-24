<template>
  <div v-if="accountStore.userInfo">
    <h1>{{ accountStore.userInfo?.nickname || '사용자' }}님의 플레이리스트</h1>
    <div class="playlist">
      <div v-for="playlist in accountStore.userInfo.playlists" :key="playlist.id">
        <div @click="seePlaylistDetail(user_id, playlist.id)">
          <ListThumbnail
            :movies="playlist.movies"
          />
          <h3>{{ playlist.title }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account'
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ListThumbnail from '@/components/MyPage/ListThumbnail.vue';

const route = useRoute()
const router = useRouter()
const user_id = route.params.id
const accountStore = useAccountStore()

const seePlaylistDetail = function (user_id, playlist_id) {
  router.push({ name: 'MyPlaylistDetailView', params: { id: user_id, playlist_id: playlist_id }})
}

onMounted(() => {
  accountStore.getUserInfo(user_id)
})
</script>

<style scoped>
.playlist {
  display: flex;
  flex-wrap: wrap;
}
</style>