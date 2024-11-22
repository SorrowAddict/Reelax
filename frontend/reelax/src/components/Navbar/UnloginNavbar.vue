<template>
  <BaseNavbar>
    <RouterLink :to="{ name: 'LoginPageView' }"><h3>로그인</h3></RouterLink>
    <RouterLink :to="{ name: 'SignupPageView' }"><h3>회원가입</h3></RouterLink>
  </BaseNavbar>
</template>

<script setup>
import BaseNavbar from './BaseNavbar.vue'
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
h2 {
  padding: 0px 10px;
}
a {
  text-decoration: none;
  color: white;
}
</style>