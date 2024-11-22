<template>
  <div class="login-page container d-flex flex-column align-items-center justify-content-center">
    <h1 class="mb-4">로그인</h1>
    <form @submit.prevent="logIn" class="login-form d-flex flex-column align-items-center">
      <!-- 아이디 입력 -->
      <input
        class="form-control mb-3"
        type="text"
        placeholder="아이디"
        v-model="username"
        required
      />
      <!-- 비밀번호 입력 -->
      <input
        class="form-control mb-4"
        type="password"
        placeholder="비밀번호"
        v-model="password"
        required
      />
      <!-- 로그인 버튼 -->
      <button class="btn btn-primary w-100 mb-3">로그인</button>
    </form>

    <!-- 비밀번호 재설정 링크 -->
    <p class="text-muted small">
      <a href="#" class="text-decoration-none">비밀번호를 잊으셨나요?</a>
    </p>

    <!-- 구분선 -->
    <hr class="w-100 my-4" />

    <!-- 소셜 로그인 -->
    <h3 class="mb-3">소셜 계정으로 로그인</h3>
    <div class="d-flex gap-3">
      <button class="btn btn-outline-primary">
        <i class="fab fa-google"></i> Google
      </button>
      <button class="btn btn-outline-info">
        <i class="fab fa-facebook-f"></i> Facebook
      </button>
      <button class="btn btn-outline-dark">
        <i class="fab fa-github"></i> GitHub
      </button>
    </div>
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
/* 로그인 페이지 스타일 */
.login-page {
  min-height: 100vh; /* 화면 전체 높이 */
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #2d2d2d;
  color: white;
  padding: 20px;
}

/* 로그인 폼 */
.login-form {
  width: 100%;
  max-width: 400px; /* 폼 최대 너비 */
  background-color: #444444; /* 배경색 */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); /* 그림자 효과 */
}

/* 버튼 스타일 */
.btn-primary {
  background-color: #007bff;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-outline-primary:hover {
  background-color: #007bff;
  color: white;
}

.btn-outline-info:hover {
  background-color: #17a2b8;
  color: white;
}

.btn-outline-dark:hover {
  background-color: #343a40;
  color: white;
}

/* 링크 스타일 */
a {
  color: #007bff;
}

a:hover {
  text-decoration: underline;
}

/* 반응형 조정 */
@media (max-width: 576px) {
  .login-form {
    padding: 15px;
  }

  .btn {
    font-size: 14px;
    padding: 10px;
  }
}
</style>
