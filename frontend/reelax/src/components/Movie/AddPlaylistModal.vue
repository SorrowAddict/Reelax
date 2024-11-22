<template>
  <div>
    <div class="modal fade" id="addPlaylistModal" tabindex="-1" aria-labelledby="addPlaylistModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h3 class="modal-title fs-5" id="addPlaylistModalLabel">나의 플레이 리스트에 추가</h3>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="create-list-modal" data-bs-toggle="modal" data-bs-target="#createPlaylistModal">
              <font-awesome-icon :icon="['fas', 'plus']" size="lg"/>
              <h3>새로운 플레이리스트 만들기</h3>
            </div>
            <br>
            <div class="playlist">
              <div v-if="playlistStore.playlist.length === 0">
                <h3>플레이리스트가 없습니다.</h3>
              </div>
              <div v-else>
                <div v-for="list in playlistStore.playlist" :key="list.id" class="mb-3">
                  <div @click="addMovieToPlaylist(list.id, movie.movie_id)">
                    <h3>{{ list.title }}</h3>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <CreatePlaylistModal
      :movie="movie"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import CreatePlaylistModal from './CreatePlaylistModal.vue'
import { usePlaylistStore } from '@/stores/playlist'

const playlistStore = usePlaylistStore()

defineProps({
  movie: Object
})

const addMovieToPlaylist = function (playlist_id, movie_id) {
  const movies = [
    movie_id
  ]
  console.log(movies)
  playlistStore.addMovieToPlaylist(playlist_id, movies)
  playlistStore.getPlaylist()
}

onMounted(() => {
  playlistStore.getPlaylist()
})
</script>

<style scoped>
.modal-content {
  background-color: #2d2d2d;
}
.create-list-modal {
  display: flex;
  gap: 10px;
}
.modal-body {
  display: flex;
  flex-direction: column; /* 세로로 쌓이도록 설정 */
  align-items: center;    /* 가로 정렬: 가운데 */
  justify-content: center; /* 세로 정렬: 가운데 */
  text-align: center;     /* 텍스트 가운데 정렬 */
}
</style>