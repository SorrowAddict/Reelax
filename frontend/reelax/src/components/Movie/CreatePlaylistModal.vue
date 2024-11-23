<template>
  <div>
    <div class="modal fade" id="createPlaylistModal" tabindex="-1" aria-labelledby="createPlaylistModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="createPlaylistModalLabel">새로운 플레이리스트 만들기</h1>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form id="createPlaylistForm" @submit.prevent="createPlaylist(movie.movie_id)">
              <label for="title">플레이리스트 제목</label> <br>
              <input type="text" id="title" v-model="title"> <br>
              <label for="description">플레이리스트 설명</label> <br>
              <textarea id="description" v-model="description"></textarea>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-target="#addPlaylistModal" data-bs-toggle="modal">취소</button>
            <button type="submit" class="btn btn-primary" form="createPlaylistForm" data-bs-dismiss="modal">생성</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { usePlaylistStore } from '@/stores/playlist'
const props = defineProps({
  movie: Object
})

const title = ref(null)
const description = ref(null)
const playlistStore = usePlaylistStore()

const createPlaylist = function (movie_id) {
  const payload = {
    title: title.value,
    description: description.value,
    movies: [
      movie_id
    ]
  }
  playlistStore.createPlaylist(payload)
  playlistStore.getPlaylist()
}
</script>

<style scoped>
.modal-content {
  background-color: #2d2d2d;
}

.modal-body>form {
  display: flex;
  flex-direction: column;
}

.modal-footer {
  border-top: none;
}
</style>