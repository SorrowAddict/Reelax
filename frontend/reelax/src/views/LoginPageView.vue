<template>
  <div class="container d-flex flex-column align-items-center">
    <h1>로그인 페이지</h1>
    <br>
    <form @submit.prevent="logIn" class="d-flex flex-column align-items-center">
      <input class="form-control mb-3" type="text" placeholder="아이디" v-model="username">
      <input class="form-control mb-3" type="password" placeholder="비밀번호" v-model="password">
      <button class="btn">로그인</button>
    </form> <br>
    <p>비밀번호를 잊어버리셨나요?</p>
    <hr class="w-100"> <br>
    <h3>소셜 계정으로 로그인</h3>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'

const username = ref(null)
const password = ref(null)
const store = useAccountStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}
</script>

<style scoped>

</style>