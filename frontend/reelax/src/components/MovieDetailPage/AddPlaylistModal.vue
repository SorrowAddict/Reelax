<template>
  <div>
    <div class="modal fade" id="addPlaylistModal" tabindex="-1" aria-labelledby="addPlaylistModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h3 class="modal-title fs-5" id="addPlaylistModalLabel">나의 플레이리스트에 추가</h3>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- 새 플레이리스트 생성 -->
            <div class="create-list-modal" data-bs-toggle="modal" data-bs-target="#createPlaylistModal">
              <font-awesome-icon :icon="['fas', 'plus']" size="2x" />
              <h3>새로운 플레이리스트 만들기</h3>
            </div>

            <hr class="divider" />

            <!-- 플레이리스트 목록 -->
            <div class="playlist">
              <div v-if="playlistStore.playlist.length === 0" class="empty-playlist">
                <font-awesome-icon :icon="['fas', 'folder-open']" size="3x" />
                <h3>플레이리스트가 없습니다.</h3>
                <p>새로운 플레이리스트를 만들어보세요.</p>
              </div>
              <div v-else>
                <div v-for="list in playlistStore.playlist" :key="list.id" class="playlist-item" @click="addMovieToPlaylist(list.id, movie.movie_id)">
                  <font-awesome-icon :icon="['fas', 'list']" size="lg" />
                  <h3>{{ list.title }}</h3>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <CreatePlaylistModal :movie="movie" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import CreatePlaylistModal from './CreatePlaylistModal.vue';
import { usePlaylistStore } from '@/stores/playlist';
import { useAccountStore } from '@/stores/account';

const playlistStore = usePlaylistStore();
const accountStore = useAccountStore()

defineProps({
  movie: Object,
});

const addMovieToPlaylist = function (playlist_id, movie_id) {
  const movies = [movie_id];
  console.log(movies);
  playlistStore.addMovieToPlaylist(playlist_id, movies);
  playlistStore.getPlaylist();
};

onMounted(() => {
  if (accountStore.isLogin) {
    playlistStore.getPlaylist();
  }
});
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

.modal-header h3 {
  font-size: 1.5rem;
  color: #ffffff;
}

.create-list-modal {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  border: 1px dashed #888;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.create-list-modal:hover {
  background-color: #383838;
}

.create-list-modal h3 {
  font-size: 1.2rem;
  color: white
}

.divider {
  margin: 20px 0;
  border: none;
  border-top: 1px solid #555;
}

.empty-playlist {
  text-align: center;
  color: #aaaaaa;
}

.empty-playlist h3 {
  margin-top: 10px;
  font-size: 1.2rem;
}

.empty-playlist p {
  font-size: 0.9rem;
  margin-top: 5px;
}

.playlist-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 6px;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.playlist-item:hover {
  background-color: #383838;
}

.playlist-item h3 {
  font-size: 1.1rem;
  margin: 0;
  color: #ffffff;
}
</style>
