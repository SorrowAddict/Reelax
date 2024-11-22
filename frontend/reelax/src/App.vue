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
  <Footer />
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
body {
  background-color: #2d2d2d;
  color: white;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin: 0;
}

main {
  flex: 1; /* 콘텐츠 영역이 footer 위로 확장되도록 설정 */
}

footer {
  margin-top: auto;
}
</style>
