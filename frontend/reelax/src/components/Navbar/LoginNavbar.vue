<template>
  <div class="nav-bar">
    <div class="home-link">
      <RouterLink :to="{ name: 'MainPageView' }"><img src="/image/logo_final.png" alt="" height="60px"></RouterLink>
    </div>
    <div class="account-link">
      <RouterLink :to="{ name: '' }"><h3>프로필</h3></RouterLink>
      <h3 @click="logOut">로그아웃</h3>
    </div>
  </div>

</template>

<script setup>
import { useAccountStore } from '@/stores/account'

const store = useAccountStore()

const logOut = function () {
  store.logOut()
}
</script>

<style scoped>
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid white;
}
.account-link {
  display: flex;
}
h1 {
  padding: 0px 10px;
}
a {
  text-decoration: none;
  color: white;
}
</style>