<template>
  <div class="nav-bar">
    <div class="home-link">
      <RouterLink :to="{ name: 'MainPageView' }"><h1>REELEX</h1></RouterLink>
    </div>
    <div class="account-link">
      <RouterLink :to="{ name: 'LoginPageView' }"><h1>로그인</h1></RouterLink>
      <RouterLink :to="{ name: 'SignupPageView' }"><h1>회원가입</h1></RouterLink>
    </div>
  </div>
</template>

<script setup>

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