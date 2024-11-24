<template>
  <div v-if="accountStore.userInfo" class="container">
    <h1 class="playlist-title">{{ accountStore.userInfo?.nickname || '사용자' }}님의 플레이리스트</h1>
    <div class="row playlist">
      <!-- 부트스트랩의 그리드 클래스 활용 -->
      <div 
        class="col-6 col-md-4 col-lg-3 mb-4" 
        v-for="playlist in accountStore.userInfo.playlists" 
        :key="playlist.id"
      >
        <div class="list" @click="seePlaylistDetail(user_id, playlist.id)">
          <ListThumbnail :movies="playlist.movies" />
          <p class="text-center mt-2">{{ playlist.title }}</p>
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

.list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.list:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.playlist-title {
  margin-top: 20px;
  margin-bottom: 50px;
}
</style>