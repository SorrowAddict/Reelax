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
    <div class="playlist-section">
      <h2>{{ accountStore.userInfo?.nickname || '사용자' }}님의 영화 플레이리스트</h2>
      <div class="content-box">
        <div v-if="accountStore.userInfo.playlists">
          <div v-for="playlist in accountStore.userInfo.playlists" :key="playlist.id">
            <h3>{{ playlist.title }}</h3>
            <p>{{ playlist.description }}</p>
            <div v-for="movie in playlist.movies" :key="movie.id">
              <img :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`" alt="Movie Poster" />
              <p>{{ movie.title }}</p>
            </div>
          </div>
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
import { useRoute } from 'vue-router'

const accountStore = useAccountStore()
const route = useRoute()
const defaultProfileImage = '/path/to/default-profile-image.jpg'
const profileImage = ref(null)

// 닉네임 수정 상태
const isEditingNickname = ref(false)
const nickname = ref('')

// 컴포넌트 로드 시 데이터 가져오기
onMounted(() => {
  accountStore.getUserInfo(route.params.id)
  if (accountStore.userInfo.profile_image) {
    profileImage.value = `http://localhost:8000${accountStore.userInfo.profile_image}`
  } else {
    profileImage.value = defaultProfileImage
  }
  
})

// 프로필 이미지를 가져오는 함수
// const profileImage = computed(() => {
//   return accountStore.userInfo.profile_image
//   ? `http://localhost:8000${accountStore.userInfo.profile_image}`
//   : defaultProfileImage
// })
// const fetchUserProfile = () => {
//   profileImage.value = accountStore.userInfo.profile_image
//     ? `http://localhost:8000${accountStore.userInfo.profile_image}`
//     : defaultProfileImage
// }

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
