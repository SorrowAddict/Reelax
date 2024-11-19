<template>
  <div>
    <nav>
      <RouterLink :to="{ name: 'MainPageView' }"><h1>REELEX</h1></RouterLink>
      <RouterLink :to="{ name: 'LoginPageView' }"><h1>프로필</h1></RouterLink>
      <RouterLink :to="{ name: 'SignupPageView' }"><h1>로그아웃</h1></RouterLink>
    </nav>
  </div>
</template>

<script setup>

</script>

<style scoped>

</style>