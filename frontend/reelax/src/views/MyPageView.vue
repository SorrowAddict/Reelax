<template>
  <div class="my-page-container">
    <!-- 프로필 정보 -->
    <div class="profile-section" data-aos="fade-up">
      <div class="profile-header">
        <img
          :src="profileImage || defaultProfileImage"
          alt="프로필 이미지"
          class="profile-image"
          @error="onImageError"
          @click="triggerImageUpload"
        />
        <!-- 프로필 이미지 업로드 -->
        <input
          type="file"
          ref="imageInput"
          class="hidden"
          @change="uploadProfileImage"
          accept="image/*"
        />
        <div class="profile-info">
          <h1>
            <span v-if="!isEditingNickname">{{ accountStore.userInfo?.nickname || '사용자' }}</span>
            <input
              v-else
              type="text"
              v-model="nickname"
              class="nickname-input"
              @keyup.enter="updateNickname"
              @blur="cancelEditing"
            />
            <span class="edit-icon" @click="editNickname">✎</span>
          </h1>
          <div v-if="accountStore.userInfo" class="follow-info">
            <span>팔로우 {{ accountStore.userInfo.followers_count ?? -1 }}</span>
            <span>팔로잉 {{ accountStore.userInfo.followings_count ?? -1 }}</span>
          </div>
          <div v-else class="follow-info">
            <span>팔로우 -</span>
            <span>팔로잉 -</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 영화 플레이리스트 -->
    <div class="playlist-section" data-aos="fade-up" data-aos-delay="150">
      <h2>{{ accountStore.userInfo?.nickname || '사용자' }}님의 영화 플레이리스트</h2>
      <div class="content-box">
        <div v-if="accountStore.userInfo.playlists">
          <div class="playlist-box">
            <div v-for="playlist in accountStore.userInfo.playlists.slice(0, 4)" :key="playlist.id">
              <div @click="seePlaylistDetail(user_id, playlist.id)">
                <ListThumbnail
                  :movies="playlist.movies"
                />
                <h3>{{ playlist.title }}</h3>
                <p>{{ playlist.description }}</p>
              </div>
            </div>
          </div>
          <p @click="seeAllPlaylist(user_id)">더보기</p>
        </div>
        <p v-else>플레이리스트가 비어 있습니다.</p>
      </div>
    </div>

    <!-- 좋아하는 영화 -->
    <div class="movie-section" data-aos="fade-up" data-aos-delay="150">
      <h2>{{ accountStore.userInfo?.nickname || '사용자' }}님이 좋아한 영화</h2>
      <div class="content-box">
        <div v-if="accountStore.userInfo.liked_movies">
          <div class="movie-box">
            <div v-for="movie in accountStore.userInfo.liked_movies.slice(0, 4)" :key="movie.movie_id">
              <img @click="seeMovieDetail(movie.movie_id)" :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`" alt="">
            </div>
          </div>
          <p @click="seeAllMovies(user_id)">더보기</p>
        </div>
        <p v-else>플레이리스트가 비어 있습니다.</p>
      </div>
    </div>

    <!-- 좋아하는 감독 -->
    <div class="director-section" data-aos="fade-up" data-aos-delay="150">
      <h2>{{ accountStore.userInfo?.nickname || '사용자' }}님이 좋아한 감독</h2>
      <div class="content-box">
        <div v-if="accountStore.userInfo.liked_directors">
          <div class="director-box">
            <div v-for="director in accountStore.userInfo.liked_directors.slice(0, 4)" :key="director.director_id">
              <div @click="seeDirecDetail(director.director_id)">
                <img :src="`https://image.tmdb.org/t/p/w200/${director.profile_path}`" alt="">
                <h3>{{ director.name }}</h3>
              </div>
              
            </div>
          </div>
          <p @click="seeAllDirectors(user_id)">더보기</p>
        </div>
        <p v-else>플레이리스트가 비어 있습니다.</p>
      </div>
    </div>

    <!-- 좋아하는 배우 -->
    <div class="actor-section" data-aos="fade-up" data-aos-delay="150">
      <h2>{{ accountStore.userInfo?.nickname || '사용자' }}님이 좋아한 배우</h2>
      <div class="content-box">
        <div v-if="accountStore.userInfo.liked_actors">
          <div class="actor-box">
            <div v-for="actor in accountStore.userInfo.liked_actors.slice(0, 4)" :key="actor.actor_id">
              <img @click="seeActorDetail(actor.actor_id)" :src="`https://image.tmdb.org/t/p/w200/${actor.profile_path}`" alt="">
              <h3>{{ actor.name }}</h3>
            </div>
          </div>
          <p @click="seeAllActors(user_id)">더보기</p>
        </div>
        <p v-else>플레이리스트가 비어 있습니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAccountStore } from '@/stores/account'
import axios from 'axios'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { useRoute, useRouter } from 'vue-router'
import ListThumbnail from '@/components/Movie/ListThumbnail.vue'

const accountStore = useAccountStore()
const route = useRoute()
const router = useRouter()
const defaultProfileImage = '/path/to/default-profile-image.jpg'
const profileImage = ref(null)

// 닉네임 수정 상태
const isEditingNickname = ref(false)
const nickname = ref('')
const user_id = route.params.id

// 컴포넌트 로드 시 데이터 가져오기
onMounted(() => {
  AOS.init({
    duration: 800,
    easing: 'ease-in-out-quint',
    once: false,
  })
  accountStore.getUserInfo(route.params.id)
  if (accountStore.userInfo.profile_image) {
    profileImage.value = `http://localhost:8000${accountStore.userInfo.profile_image}`
  } else {
    profileImage.value = defaultProfileImage
  }
  console.log(accountStore.userInfo)
  
})

// 프로필 이미지 업로드
const triggerImageUpload = () => {
  const input = document.querySelector('input[type="file"]')
  input.click()
}

const uploadProfileImage = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('profile_image', file)

  try {
    const response = await axios.put(
      'http://localhost:8000/api/v1/accounts/profile/update-image/',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Token ${accountStore.token}`
        }
      }
    )
    profileImage.value = `http://localhost:8000${response.data.profile_image}`
    alert('프로필 이미지가 성공적으로 업데이트되었습니다.')
  } catch (error) {
    console.error('프로필 이미지를 업로드하는 중 오류가 발생했습니다.', error)
    alert('프로필 이미지를 업로드할 수 없습니다.')
  }
}

// 닉네임 수정
const editNickname = () => {
  nickname.value = accountStore.userInfo?.nickname || ''
  isEditingNickname.value = true
}

const cancelEditing = () => {
  isEditingNickname.value = false
}

const updateNickname = async () => {
  if (!nickname.value.trim()) return

  try {
    const response = await axios.patch(
      'http://localhost:8000/api/v1/accounts/user/',
      { nickname: nickname.value },
      {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      }
    )
    accountStore.userInfo.nickname = response.data.nickname
    isEditingNickname.value = false
    alert('닉네임이 성공적으로 업데이트되었습니다.')
  } catch (error) {
    console.error('닉네임을 업데이트하는 중 오류가 발생했습니다.', error)
    alert('닉네임을 업데이트할 수 없습니다.')
  }
}

// 프로필 이미지 로드 실패 시 기본 이미지로 대체
const onImageError = () => {
  profileImage.value = defaultProfileImage
}

const seeAllPlaylist = function (user_id) {
  router.push({ name: 'MyPlaylistView', params: { id: user_id }})
}

const seePlaylistDetail = function (user_id, playlist_id) {
  router.push({ name: 'MyPlaylistDetailView', params: { id: user_id, playlist_id: playlist_id }})
}

const seeAllMovies = function (user_id) {
  router.push({ name: 'MyMovieView', params: { id: user_id }})
}

const seeMovieDetail = function (movie_id) {
  router.push({ name: 'MovieDetailView', params: { id: movie_id }})
}

const seeAllDirectors = function (user_id) {
  router.push({ name: 'MyDirectorView', params: { id: user_id }})
}

const seeDirecDetail = function (direc_id) {
  router.push({ name: 'DirecDetailView', params: { direc_id: direc_id }})
}

const seeAllActors = function (user_id) {
  router.push({ name: 'MyActorView', params: { id: user_id }})
}

const seeActorDetail = function (actor_id) {
  router.push({ name: 'ActorDetailView', params: { actor_id: actor_id }})
}
</script>


<style scoped>
/* 전체 페이지 스타일 */
.my-page-container {
  background-color: #454545;
  color: white;
  padding: 40px 20px;
  max-width: 1440px;
  margin: 0 auto;
  font-family: 'DM Sans', sans-serif;
}

.hidden {
  display: none;
}

/* 프로필 섹션 */
.profile-section {
  margin-bottom: 40px;
  border-bottom: 1px solid #666666;
  padding-bottom: 20px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: #d9d9d9;
  object-fit: cover;
  cursor: pointer;
}

.nickname-input {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px;
  font-size: 18px;
}

.profile-info h1 {
  font-size: 36px;
  margin-bottom: 10px;
}

.nickname {
  font-size: 24px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.nickname .edit-icon {
  font-size: 18px;
  cursor: pointer;
  color: #aaaaaa;
  transition: color 0.3s;
}

.nickname .edit-icon:hover {
  color: white;
}

.follow-info {
  margin-top: 10px;
  display: flex;
  gap: 20px;
  font-size: 18px;
}

.playlist-box, .movie-box, .director-box, .actor-box {
  display: flex;
}
</style>
