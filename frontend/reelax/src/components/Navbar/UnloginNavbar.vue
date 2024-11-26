<!-- components/Navbar/UnloginNavbar.vue -->

<template>
  <BaseNavbar>
    <RouterLink :to="{ name: 'LoginPageView' }" class="btn btn-primary">
      <FontAwesomeIcon icon="sign-in-alt" /> 로그인
    </RouterLink>
    <RouterLink :to="{ name: 'LoginPageView' }" class="btn btn-secondary">
      <FontAwesomeIcon icon="user-plus" /> 회원가입
    </RouterLink>
  </BaseNavbar>
</template>

<script setup>
import BaseNavbar from './BaseNavbar.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { RouterLink } from 'vue-router'
</script>

<style scoped>
/* 버튼 스타일 */
.btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 4px;
  text-decoration: none;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
