<template>
  <nav v-if="store.isLogin">
    <LoginNavbar />
  </nav>
  <nav v-else>
    <UnloginNavbar />
  </nav>
  <main>
    <RouterView />
  </main>
  <footer>
    <div>
      <p>서비스 이용 약관 | 개인정보 처리방침 | 회사 안내</p>
      <p>고객센터 | ssafy@ssafy.com, 02-000-0000</p>
      <p>REELAX | 대표 홍길동 | 서울 강남구 테헤란로 212</p>
      <p>Copyright© REELAX All rights reserved.</p>
    </div>
    <div>
      <p>X 로고</p>
      <p>인스타 로고</p>
      <p>gmail 로고</p>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAccountStore } from './stores/account'
import LoginNavbar from './components/Navbar/LoginNavbar.vue'
import UnloginNavbar from './components/Navbar/UnloginNavbar.vue'

const store = useAccountStore()
</script>

<style>
body {
  background-color: #2D2D2D;
  color: white;
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 화면의 전체 높이를 보장 */
  margin: 0;
}

nav {
  margin-bottom: 20px;
}

footer {
  display: flex;
  justify-content: space-between;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  padding: 10px 20px; /* 선택적으로 상하 좌우 여백 추가 */
  margin-top: 20px; /* 콘텐츠와 간격 추가 */
}

main {
  flex: 1; /* 콘텐츠 영역이 footer 위로 확장되도록 설정 */
}
</style>