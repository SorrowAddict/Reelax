<template>
  <BaseNavbar>
    <!-- 로그아웃 버튼 -->
    <button @click="logOut" class="btn btn-danger logout-button">
      <FontAwesomeIcon icon="sign-out-alt" />
    </button>

    <!-- 프로필 이미지 및 모달 -->
    <div class="profile-container">
      <img
        :src="`${BASE_URL}${store.loggedInUserInfo?.profile_image || '/media/profile_images/default_profile.jpg'}`"
        alt="User Profile"
        class="profile-image"
        @error="onImageError"
        @click="toggleModal"
      />
      <!-- 프로필 모달 -->
      <div
        v-if="isModalOpen"
        class="profile-modal"
        @click.self="closeModal"
      >
        <button @click="goToMyPage" class="btn btn-primary w-100 mb-2">
          마이페이지
        </button>
        <button @click="logOut" class="btn btn-danger w-100">
          <FontAwesomeIcon icon="sign-out-alt" />
          로그아웃
        </button>
      </div>
    </div>
  </BaseNavbar>
</template>

<script setup>
import BaseNavbar from './BaseNavbar.vue'
import { useAccountStore } from '@/stores/account'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import axios from 'axios';
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const store = useAccountStore()
const BASE_URL = import.meta.env.VITE_BASE_URL
const defaultProfileImage = `${BASE_URL}/media/profile_images/default_profile.jpg` // 기본 프로필 이미지 경로
// const defaultProfileImage = `http://localhost:8000/media/profile_images/default_profile.jpg` // 기본 프로필 이미지 경로
// const defaultProfileImage = `http://43.203.255.151:8000/media/profile_images/default_profile.jpg` // 기본 프로필 이미지 경로
const profileImage = ref(defaultProfileImage) // 프로필 이미지 URL
const router = useRouter()

const isModalOpen = ref(false)

onMounted(() => {
  if (!store.loggedInUserInfo) {
    store.getLoggedInUserInfo()
  }
  console.log('로그인 Navbar onMounted', store.userInfo)
})

// 이미지 로드 실패 시 기본 이미지로 대체
const onImageError = () => {
  profileImage.value = defaultProfileImage
}

const logOut = () => {
  store.logOut()
}

const goToMyPage = () => {
  // console.log(store.userId)
  isModalOpen.value = false
  router.push({ name: 'MyPageView', params: { id: store.userId }})
}

// 모달 열고 닫기
const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value
}
const closeModal = () => {
  isModalOpen.value = false
}

watch(
  () => store.loggedInUserInfo?.profile_image,
  (newImage) => {
    profileImage.value = newImage
      ? `${BASE_URL}${newImage}`
      : defaultProfileImage
  }
)
</script>

<style scoped>
/* 프로필 컨테이너 스타일 */
.profile-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  position: relative; /* 모달 위치를 프로필 이미지 기준으로 설정 */
}

/* 프로필 이미지 스타일 */
.profile-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
  transition: border-color 0.3s;
  cursor: pointer;
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

/* 프로필 모달 스타일 */
.profile-modal {
  position: absolute;
  top: 50px; /* 프로필 이미지 아래 */
  right: 0;
  z-index: 1000;
  width: 200px;
  background: #3a3a3a; /* 모달 배경색 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4); /* 더 강한 그림자 */
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #555555; /* 약간 어두운 테두리 */
  color: white;
}

/* 모달 내부 버튼 스타일 */
.profile-modal button {
  font-size: 14px;
  padding: 10px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s;
}

/* 마이페이지 버튼 */
.profile-modal .btn-primary {
  background-color: #4CAF50; /* 부드러운 녹색 */
  color: white;
}

.profile-modal .btn-primary:hover {
  background-color: #388E3C; /* hover 시 진한 녹색 */
}

/* 로그아웃 버튼 */
.profile-modal .btn-danger {
  background-color: #FF5722; /* 따뜻한 주황색 */
  color: white;
}

.profile-modal .btn-danger:hover {
  background-color: #E64A19; /* hover 시 진한 주황색 */
}
</style>
