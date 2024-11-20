<template>
  <div class="container d-flex flex-column align-items-center">
    <h1>회원가입 페이지</h1>
    <form @submit.prevent="signUp" class="d-flex flex-column align-items-center">
      <input class="form-control" type="text" placeholder="아이디" v-model="username"> <br>
      <input class="form-control" type="password" placeholder="비밀번호" v-model="password1"> <br>
      <input class="form-control" type="password" placeholder="비밀번호 확인" v-model="password2"> <br>
      <button class="btn">회원가입</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'

const store = useAccountStore()

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }

  store.signUp(payload)  
}
</script>

<style scoped>

</style>