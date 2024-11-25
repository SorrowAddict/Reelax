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
              <div class="form-group">
                <label for="title">플레이리스트 제목</label>
                <input type="text" id="title" v-model="title" class="form-control" placeholder="제목을 입력하세요" />
              </div>
              <div class="form-group">
                <label for="description">플레이리스트 설명</label>
                <textarea id="description" v-model="description" class="form-control" placeholder="설명을 입력하세요"></textarea>
              </div>
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
import { ref } from 'vue';
import { usePlaylistStore } from '@/stores/playlist';

const props = defineProps({
  movie: Object,
});

const title = ref('');
const description = ref('');
const playlistStore = usePlaylistStore();

const createPlaylist = function (movie_id) {
  const payload = {
    title: title.value,
    description: description.value,
    movies: [movie_id],
  };
  playlistStore.createPlaylist(payload);
  playlistStore.getPlaylist();
};
</script>

<style scoped>
.modal-content {
  background-color: #2d2d2d;
  color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  padding: 20px;
}

.modal-header {
  border-bottom: 1px solid #444;
}

.modal-header h1 {
  font-size: 1.5rem;
  color: #ffffff;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-size: 1rem;
  margin-bottom: 8px;
  color: #cccccc;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #555555;
  border-radius: 6px;
  background-color: #3a3a3a;
  color: #ffffff;
  font-size: 1rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input[type="text"]::placeholder,
textarea::placeholder {
  color: #aaaaaa;
}

input[type="text"]:focus,
textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.5);
  outline: none;
  background-color: #3a3a3a;
  color: #ffffff;
  outline: none;
}

textarea {
  resize: none;
  height: 100px;
}

.modal-footer {
  border-top: none;
  display: flex;
  justify-content: space-between;
}

button {
  border-radius: 4px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
  transform: translateY(-2px);
}
</style>
