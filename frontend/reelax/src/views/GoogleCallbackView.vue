<template>
  <div>
    <h1>Google 로그인 중...</h1>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account'
import { onMounted } from 'vue'

const router = useRouter()
const accountStore = useAccountStore()

onMounted(() => {
  const currentUrl = new URL(window.location.href)
  const accessToken = currentUrl.searchParams.get('access_token') // 백엔드에서 전달된 토큰

  if (accessToken) {
    accountStore.token = accessToken // Pinia Store에 저장
    accountStore.getUserId()
    accountStore.getLoggedInUserInfo() // 사용자 정보 가져오기
    router.push({ name: 'GenreSelectionView' }) // 메인 페이지로 이동
  } else {
    console.error('Google 로그인 실패: 토큰이 없습니다.')
    router.push({ name: 'LoginPageView' }) // 로그인 페이지로 이동
  }
})
</script>