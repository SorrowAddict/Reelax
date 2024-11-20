<template>
  <v-app>
    <v-container class="d-flex justify-center align-center" style="height: 100vh;">
      <v-card class="pa-6" elevation="2" style="max-width: 400px; width: 100%;">
        <v-card-title class="text-h5 text-center">로그인</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="logIn">
            <!-- 아이디 입력 -->
            <v-text-field
              v-model="username"
              label="아이디"
              outlined
              class="mb-4"
              dense
            ></v-text-field>

            <!-- 비밀번호 입력 -->
            <v-text-field
              v-model="password"
              label="비밀번호"
              type="password"
              outlined
              class="mb-4"
              dense
            ></v-text-field>

            <!-- 로그인 버튼 -->
            <v-btn type="submit" color="primary" block large>
              로그인
            </v-btn>
          </v-form>
        </v-card-text>
        <v-divider class="my-4"></v-divider>
        <v-card-text class="text-center">
          <p>비밀번호를 잊으셨나요?</p>
          <v-btn text color="secondary">비밀번호 찾기</v-btn>
        </v-card-text>
        <v-divider class="my-4"></v-divider>
        <v-card-text class="text-center">
          <h3>소셜 계정으로 로그인</h3>
          <v-btn icon color="blue">
            <v-icon>mdi-facebook</v-icon>
          </v-btn>
          <v-btn icon color="red">
            <v-icon>mdi-google</v-icon>
          </v-btn>
          <v-btn icon color="blue darken-3">
            <v-icon>mdi-twitter</v-icon>
          </v-btn>
        </v-card-text>
      </v-card>
    </v-container>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'

const username = ref(null)
const password = ref(null)
const store = useAccountStore()

const logIn = () => {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}
</script>

<style scoped>
/* 필요하면 스타일 추가 */
</style>