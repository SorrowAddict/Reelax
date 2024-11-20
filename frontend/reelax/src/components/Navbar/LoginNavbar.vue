<template>
  <div class="nav-bar">
    <div class="home-link">
      <RouterLink :to="{ name: 'MainPageView' }"><h1>REELEX</h1></RouterLink>
    </div>
    <div class="account-link">
      <RouterLink :to="{ name: '' }"><h1>프로필</h1></RouterLink>
      <h1 @click="logOut">로그아웃</h1>
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
}
.account-link {
  display: flex;
}
h1 {
  padding: 0px 10px;
}
a {
  text-decoration: none;
  color: black;
}
</style>