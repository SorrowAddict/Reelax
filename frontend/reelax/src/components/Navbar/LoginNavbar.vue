<!-- components/Navbar/LoginNavbar.vue -->

<template>
  <BaseNavbar>
    <button @click="logOut" class="btn btn-danger logout-button">
      <FontAwesomeIcon icon="sign-out-alt" />
    </button>
    <div class="profile-container">
      <img
        :src="profileImage"
        alt="User Profile"
        class="profile-image"
        @error="onImageError"
      />
    </div>
  </BaseNavbar>
</template>

<script setup>
import BaseNavbar from './BaseNavbar.vue'
import { useAccountStore } from '@/stores/account'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ref } from 'vue'
import { onMounted } from 'vue'

const store = useAccountStore()
const defaultProfileImage = '/default-profile.png' // 기본 프로필 이미지 경로
const profileImage = ref(defaultProfileImage) // 프로필 이미지 URL

// DRF 요청으로 프로필 이미지 가져오기
const fetchProfileImage = async () => {
  try {
    const response = await store.fetchProfile() // DRF 요청 함수 호출
    profileImage.value = response.image || defaultProfileImage
  } catch (error) {
    console.error('Failed to fetch profile image:', error)
  }
}

// 이미지 로드 실패 시 기본 이미지로 대체
const onImageError = () => {
  profileImage.value = defaultProfileImage
}

// 로그아웃 처리
const logOut = function () {
  store.logOut()
}

// 컴포넌트가 로드될 때 프로필 이미지 가져오기
onMounted(() => {
  fetchProfileImage()
})
</script>

<style scoped>
.profile-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
}

.profile-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
  transition: border-color 0.3s;
}

.profile-image:hover {
  border-color: #007bff;
}

/* 로그아웃 버튼 스타일 */
.logout-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background-color: #444444; /* 배경과 조화를 이루는 어두운 회색 */
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.logout-button:hover {
  background-color: #555555; /* hover 시 약간 밝은 회색 */
  color: #e0e0e0; /* hover 시 텍스트 색상을 밝게 */
}
</style>