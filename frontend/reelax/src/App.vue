<template>
  <nav v-if="store.isLogin">
    <LoginNavbar />
  </nav>
  <nav v-else>
    <UnloginNavbar />
  </nav>
  <RouterView />
  <footer>
    <p>Copyright© REELAX All rights reserved.</p>
    <p>X 로고</p>
    <p>인스타 로고</p>
    <p>gmail 로고</p>
  </footer>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAccountStore } from './stores/account'
import LoginNavbar from './components/Navbar/LoginNavbar.vue'
import UnloginNavbar from './components/Navbar/UnloginNavbar.vue'

const store = useAccountStore()
</script>

<style scoped>
footer {
  display: flex;
  position: absolute;
  bottom: 0px;
}

footer>p{
  padding: 0px 10px;
}
</style>