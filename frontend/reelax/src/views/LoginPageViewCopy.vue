<template>
  <div class="login-page">
    <div class="login-container">
      <!-- 헤더 -->
      <h1 tabindex="0" class="login-title">로그인</h1>
      
      <!-- 로그인 폼 -->
      <form @submit.prevent="logIn" class="login-form">
        <fieldset>
          <legend class="visually-hidden">로그인 양식</legend>
          <ul class="input-group">
            <!-- 아이디 입력 -->
            <li>
              <label>
                <input 
                  type="text" 
                  v-model="username" 
                  placeholder="이메일 주소 또는 아이디" 
                  title="아이디" 
                  class="input-style"
                  required
                >
              </label>
            </li>
            <!-- 비밀번호 입력 -->
            <li>
              <label>
                <input 
                  type="password" 
                  v-model="password" 
                  placeholder="비밀번호" 
                  title="비밀번호" 
                  class="input-style"
                  required
                >
              </label>
            </li>
          </ul>

          <!-- 체크박스 -->
          <ul class="checkbox-group">
            <li>
              <input type="checkbox" id="id-save" class="checkbox">
              <label for="id-save">아이디 저장</label>
            </li>
            <li>
              <input type="checkbox" id="login-auto" class="checkbox">
              <label for="login-auto">자동 로그인</label>
            </li>
          </ul>

          <!-- 로그인 버튼 -->
          <button type="submit" class="btn btn-primary">로그인</button>
        </fieldset>
      </form>

      <!-- 추가 링크 -->
      <ul class="additional-links">
        <li><a href="#">아이디 찾기</a></li>
        <li><a href="#">비밀번호 재설정</a></li>
        <li><a href="#">회원가입</a></li>
      </ul>

      <!-- 소셜 로그인 -->
      <div class="social-login">
        <div class="divider">
          <span class="line"></span>
          <span class="text">또는 다른 서비스 계정으로 로그인</span>
          <span class="line"></span>
        </div>
        <ul class="social-buttons">
          <li class="social-button kakao">
            <a href="#"><span class="icon">카카오</span></a>
          </li>
          <li class="social-button naver">
            <a href="#"><span class="icon">네이버</span></a>
          </li>
          <li class="social-button facebook">
            <a href="#"><span class="icon">페이스북</span></a>
          </li>
          <li class="social-button apple">
            <a href="#"><span class="icon">Apple ID</span></a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'

const store = useAccountStore()

const username = ref('')
const password = ref('')

const logIn = () => {
  const playload = {
    username: username.value,
    password: password.value
  }
  store.logIn(playload)
}
</script>

<style scoped>
/* 전체 페이지 스타일 */
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #1b1b1b;
  color: #a5a5a5;
  font-family: NotoSans, sans-serif;
}

/* 로그인 컨테이너 */
.login-container {
  width: 560px;
  padding: 40px;
  background: #252525;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  box-sizing: border-box;
  text-align: center;
}

/* 제목 스타일 */
.login-title {
  font-size: 1.8rem;
  color: white;
  margin-bottom: 20px;
}

/* 입력 그룹 */
.input-group {
  display: flex;
  flex-direction: column;
  list-style: none;
  padding: 0;
  margin: 0 0 20px 0;
}

.input-group label {
  display: block;
}

.input-group li {
  margin-bottom: 15px;
}

.input-style {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #555;
  border-radius: 4px;
  background: #1b1b1b;
  color: white;
  font-size: 1rem;
  box-sizing: border-box;
}

.input-style::placeholder {
  color: #777;
}

/* 체크박스 그룹 */
.checkbox-group {
  list-style: none;
  padding: 0;
  margin: 0 0 20px 0;
  display: flex;
  justify-content: left;
  align-items: center;
  gap: 16px;
}

.checkbox {
  margin-right: 5px;
}

label {
  color: #a5a5a5;
  font-size: 0.9rem;
}

/* 로그인 버튼 */
.btn-primary {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  color: white;
  background: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #0056b3;
}

/* 추가 링크 */
.additional-links {
  list-style: none;
  padding: 0;
  margin: 20px 0;
  display: flex;
  justify-content: space-around;
}

.additional-links a {
  color: #007bff;
  text-decoration: none;
  font-size: 0.9rem;
}

.additional-links a:hover {
  text-decoration: underline;
}

/* 소셜 로그인 */
.social-login {
  margin-top: 20px;
}

.divider {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px 0;
}

.line {
  flex: 1;
  height: 1px;
  background: #555;
}

.text {
  margin: 0 10px;
  font-size: 0.9rem;
  color: #a5a5a5;
}

.social-buttons {
  list-style: none;
  padding: 0;
  display: flex;
  justify-content: space-around;
}

.social-button a {
  color: white;
  text-decoration: none;
  background: #444;
  padding: 10px 20px;
  border-radius: 4px;
  transition: background 0.3s;
}

.social-button a:hover {
  background: #666;
}
</style>
