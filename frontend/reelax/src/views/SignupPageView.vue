<template>
  <div class="signup-page">
    <div class="signup-container">
      <!-- 헤더 -->
      <div class="signup-header">
        <h1 tabindex="0" class="signup-title">회원가입</h1>
        <p class="signup-subtitle">
          이메일과 비밀번호만으로 <br />
          쉽게 가입하고 서비스를 즐겨보세요!
        </p>
      </div>

      <!-- 회원가입 폼 -->
      <form @submit.prevent="signUp" class="signup-form">
        <fieldset>
          <legend class="visually-hidden">회원가입 양식</legend>
          <ul class="input-group">
            <!-- 아이디 입력 -->
            <li>
              <label>
                <input
                  type="email"
                  v-model="email"
                  placeholder="이메일을 입력하세요"
                  title="이메일"
                  class="input-style"
                  required
                />
              </label>
              <p class="input-info">로그인에 사용할 정확한 아이디을 입력해주세요.</p>
            </li>
            <!-- 별명 입력 -->
            <li>
              <label>
                <input
                  type="text"
                  v-model="nickname"
                  placeholder="별명"
                  title="별명"
                  class="input-style"
                  required
                />
              </label>
            </li>
            <!-- 비밀번호 입력 -->
            <li>
              <label>
                <input
                  type="password"
                  v-model="password1"
                  placeholder="비밀번호"
                  title="비밀번호"
                  class="input-style"
                  required
                />
              </label>
              <p class="input-info">비밀번호는 8~20자, 영문/숫자/특수문자 혼합으로 입력해주세요.</p>
            </li>
            <!-- 비밀번호 확인 입력 -->
            <li>
              <label>
                <input
                  type="password"
                  v-model="password2"
                  placeholder="비밀번호 확인"
                  title="비밀번호 확인"
                  class="input-style"
                  required
                />
              </label>
            </li>
          </ul>

          <!-- 회원가입 버튼 -->
          <button type="submit" class="btn btn-primary">회원가입</button>
        </fieldset>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useAccountStore } from "@/stores/account"
import { useRouter } from "vue-router"

const store = useAccountStore()
const router = useRouter()

const email = ref("")
const nickname = ref("")
const password1 = ref("")
const password2 = ref("")

const signUp = function () {
  const payload = {
    email: email.value,
    nickname: nickname.value,
    password1: password1.value,
    password2: password2.value,
  }

  store.signUp(payload)
  router.push({ name: 'GenreSelectionView' })

  // store.signUp(payload).then((token) => {
  //   if (token) {
  //     store.token = token
  //     store.fetchProfile()
      
  //   }
  // })
}
</script>

<style scoped>
/* 전체 페이지 스타일 */
.signup-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #1b1b1b;
  color: #a5a5a5;
  font-family: NotoSans, sans-serif;
}

/* 회원가입 컨테이너 */
.signup-container {
  width: 600px;
  padding: 40px;
  background: #252525;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  text-align: center;
}

/* 제목 및 부제목 */
.signup-title {
  font-size: 1.8rem;
  color: white;
  margin-bottom: 10px;
}

.signup-subtitle {
  font-size: 1rem;
  color: #a5a5a5;
  margin-bottom: 20px;
  line-height: 1.5;
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
  width: 100%;
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
}

.input-style::placeholder {
  color: #777;
}

.input-info {
  font-size: 0.9rem;
  color: #777;
  text-align: left;
  margin-top: 5px;
  margin-bottom: 0px;
}

/* 버튼 스타일 */
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

/* 약관 동의 */
.terms-container {
  margin-top: 20px;
  text-align: left;
}

.terms-title {
  font-size: 1rem;
  margin-bottom: 10px;
}

.terms-list {
  list-style: none;
  padding: 0;
}

.terms-list li {
  margin-bottom: 10px;
}

.terms-list input {
  margin-right: 10px;
}
</style>
