<template>
  <nav>
    <RouterLink :to="{ name: 'MainPageView' }"><h1>REELEX</h1></RouterLink>
    <RouterLink :to="{ name: 'LoginPageView' }"><h1>로그인</h1></RouterLink>
    <RouterLink :to="{ name: 'SignupPageView' }"><h1>회원가입</h1></RouterLink>
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
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
nav {
  display: flex;
}

nav>a {
  padding-left: 5px;
  padding-right: 5px;
}

a {
  text-decoration: none;
  color: black;
}

.login {
  display: flex;
}
.login>h1 {
  padding: 5px;
}

footer {
  display: flex;
  position: absolute;
  bottom: 0px;
}

footer>p{
  padding: 0px 10px;
}
</style>