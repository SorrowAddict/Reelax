<template>
  <div class="nav-bar">
    <div class="home-link">
      <RouterLink :to="{ name: 'MainPageView' }"><img src="/image/logo_final.png" alt="" height="60px"></RouterLink>
    </div>
    <div class="account-link">
      <RouterLink :to="{ name: 'LoginPageView' }"><h2>로그인</h2></RouterLink>
      <RouterLink :to="{ name: 'SignupPageView' }"><h2>회원가입</h2></RouterLink>
    </div>
  </div>
</template>

<script setup>

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