<template>
  <div class="my-page-container">
    <!-- 프로필 정보 -->
    <div class="profile-section">
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
            <span v-if="!isEditingNickname">{{ userInfo?.nickname || '사용자' }}</span>
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
          <div v-if="userInfo" class="follow-info">
            <span>팔로우 {{ userInfo.followers_count ?? -1 }}</span>
            <span>팔로잉 {{ userInfo.followings_count ?? -1 }}</span>
          </div>
          <div v-else class="follow-info">
            <span>팔로우 -</span>
            <span>팔로잉 -</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 영화 플레이리스트 -->
    <div class="playlist-section">
      <h2>{{ userInfo?.nickname || '사용자' }}님의 영화 플레이리스트</h2>
      <div class="content-box">
        <ul v-if="userLikedMovies && userLikedMovies.length > 0">
          <li v-for="movie in userLikedMovies" :key="movie.id">
            {{ movie.title }}
          </li>
        </ul>
        <p v-else>플레이리스트가 비어 있습니다.</p>
      </div>
    </div>

    <!-- 좋아한 영화 -->
    <div class="liked-movies-section">
      <h2>{{ userInfo?.nickname || '사용자' }}님이 좋아한 영화</h2>
      <div class="content-box">
        <ul v-if="userLikedGenreMovies && userLikedGenreMovies.length > 0">
          <li v-for="movie in userLikedGenreMovies" :key="movie.id">
            {{ movie.title }}
          </li>
        </ul>
        <p v-else>좋아한 영화가 없습니다.</p>
      </div>
    </div>

    <!-- 좋아한 배우 -->
    <div class="liked-actors-section">
      <h2>{{ userLikedActor }} 배우가 출연한 영화</h2>
      <div class="content-box">
        <ul v-if="userLikedActorMovies && userLikedActorMovies.length > 0">
          <li v-for="movie in userLikedActorMovies" :key="movie.id">
            {{ movie.title }}
          </li>
        </ul>
        <p v-else>좋아한 배우가 없습니다.</p>
      </div>
    </div>

    <!-- 좋아한 감독 -->
    <div class="liked-directors-section">
      <h2>{{ userLikedDirec }} 감독의 영화</h2>
      <div class="content-box">
        <ul v-if="userLikedDirecMovies && userLikedDirecMovies.length > 0">
          <li v-for="movie in userLikedDirecMovies" :key="movie.id">
            {{ movie.title }}
          </li>
        </ul>
        <p v-else>좋아한 감독이 없습니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/account'
import { useMovieStore } from '@/stores/movie'
import axios from 'axios'

// Pinia 스토어 가져오기
const accountStore = useAccountStore()
const movieStore = useMovieStore()

// 기본 프로필 이미지
const defaultProfileImage = '/path/to/default-profile-image.jpg'

// 프로필 데이터 상태
const profileImage = ref(null)
const userInfo = ref(null)

// 닉네임 수정 상태
const isEditingNickname = ref(false)
const nickname = ref('')

// 영화 데이터 상태
const {
  userLikedMovies,
  getUserLikedMovies,
  userLikedGenreMovies,
  getUserLikedGenreMovies,
  userLikedActorMovies,
  userLikedActor,
  getUserLikedActorMovies,
  userLikedDirecMovies,
  userLikedDirec,
  getUserLikedDirecMovies,
} = movieStore

// 프로필 이미지를 가져오는 함수
const fetchUserProfile = async () => {
  try {
    const image = await accountStore.fetchProfile()
    profileImage.value = image
      ? `http://localhost:8000${image}`
      : defaultProfileImage
    userInfo.value = accountStore.userInfo
  } catch (error) {
    console.error('프로필 데이터를 가져오는 데 실패했습니다.', error)
  }
}

// 영화 데이터를 가져오는 함수
const fetchMovieData = async () => {
  try {
    await Promise.all([
      getUserLikedMovies(),
      getUserLikedGenreMovies(),
      getUserLikedActorMovies(),
      getUserLikedDirecMovies(),
    ])
  } catch (error) {
    console.error('영화 데이터를 가져오는 데 실패했습니다.', error)
  }
}

// 컴포넌트 로드 시 데이터 가져오기
onMounted(() => {
  fetchUserProfile()
  fetchMovieData()
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
  nickname.value = userInfo?.nickname || ''
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
    userInfo.value.nickname = response.data.nickname
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
</style>
