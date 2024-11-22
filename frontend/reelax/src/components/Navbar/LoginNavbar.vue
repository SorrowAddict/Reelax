<template>
  <BaseNavbar>
    <h3>프로필</h3>
    <h3 @click="logOut" class="logout-link">로그아웃</h3>
  </BaseNavbar>
</template>

<script setup>
import BaseNavbar from './BaseNavbar.vue'
import { useAccountStore } from '@/stores/account'

const store = useAccountStore()

const logOut = function () {
  store.logOut()
}
</script>

<style scoped>
.logout-link {
  cursor: pointer;
  transition: color 0.3s;
}

.logout-link:hover {
  color: #ff4444;
}
</style>