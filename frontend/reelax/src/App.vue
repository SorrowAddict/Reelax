<template>
  <div class="page-container">
    <nav v-if="store.isLogin">
      <LoginNavbar />
    </nav>
    <nav v-else>
      <UnloginNavbar />
    </nav>
    <main>
      <RouterView />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import { useAccountStore } from '@/stores/account';
import LoginNavbar from '@/components/Navbar/LoginNavbar.vue';
import UnloginNavbar from '@/components/Navbar/UnloginNavbar.vue';
import Footer from '@/components/Footer.vue';

const store = useAccountStore();
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
}

.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #2d2d2d;
  color: white;
}
main {
  flex: 1; /* 콘텐츠 영역이 footer 위로 확장되도록 설정 */
}
</style>
