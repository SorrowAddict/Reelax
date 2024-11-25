<template>
  <div class="login">
    <div class="login__content">
      <!-- Image Section -->
      <div class="login__img">
        <img src="https://image.freepik.com/free-vector/code-typing-concept-illustration_114360-3581.jpg" alt="user login" />
      </div>

      <!-- Forms Section -->
      <div class="login__forms">
        <!-- Sign In Form -->
        <form class="login__register" id="login-in" v-show="isSignIn" @submit.prevent="handleLogin">
          <h1 class="login__title">로그인</h1>
          <div class="login__box">
            <i class="bx bx-user login__icon"></i>
            <input v-model="loginForm.email" type="email" placeholder="Email" class="login__input" />
          </div>
          <div class="login__box">
            <i class="bx bx-lock login__icon"></i>
            <input v-model="loginForm.password" type="password" placeholder="Password" class="login__input" />
          </div>
          <a href="#" class="login__forgot">Forgot Password?</a>
          <button type="submit" class="login__button">로그인</button>
          <div>
            <span class="login__account login__account--account">계정이 없다면?</span>
            <span class="login__signin login__signin--signup" @click="toggleForm">회원가입</span>
          </div>
        </form>

        <!-- Sign Up Form -->
        <form class="login__create" id="login-up" v-show="!isSignIn" @submit.prevent="handleSignUp">
          <h1 class="login__title">계정 생성</h1>
          <div class="login__box">
            <i class="bx bx-user login__icon"></i>
            <input v-model="signUpForm.email" type="email" placeholder="Email" class="login__input" />
          </div>
          <div class="login__box">
            <i class="bx bx-user login__icon"></i>
            <input v-model="signUpForm.nickname" type="text" placeholder="Nickname" class="login__input" />
          </div>
          <div class="login__box">
            <i class="bx bx-lock login__icon"></i>
            <input v-model="signUpForm.password1" type="password" placeholder="Password" class="login__input" />
          </div>
          <div class="login__box">
            <i class="bx bx-lock login__icon"></i>
            <input v-model="signUpForm.password2" type="password" placeholder="Confirm Password" class="login__input" />
          </div>
          <button type="submit" class="login__button">회원가입</button>
          <div>
            <span class="login__account login__account--account">이미 계정이 있습니까?</span>
            <span class="login__signup login__signup--signup" @click="toggleForm">로그인</span>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useAccountStore } from '@/stores/account'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const accountStore = useAccountStore()
    const isSignIn = ref(true)
    const router = useRouter()

    const loginForm = ref({
      email: '',
      password: ''
    })

    const signUpForm = ref({
      email: '',
      nickname: '',
      password1: '',
      password2: ''
    })

    const toggleForm = () => {
      isSignIn.value = !isSignIn.value
    }

    const handleLogin = async () => {
      const payload = { ...loginForm.value }
      await accountStore.logIn(payload)
    }

    const handleSignUp = async () => {
      const payload = { ...signUpForm.value }
      accountStore.signUp(payload).then((token) => {
        if (token) {
          accountStore.token = token
          accountStore.fetchProfile()
          router.push({ name: 'GenreSelectionView' })
        }
      }).then((result) => {
        if (result) {
          console.log('회원가입이 완료되었습니다.')
          router.push({ name: 'GenreSelectionView' }) // GenreSelectionView로 이동
        }
      })
    }

    return {
      isSignIn,
      loginForm,
      signUpForm,
      toggleForm,
      handleLogin,
      handleSignUp
    }
  }
}
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');

/* CSS 스타일 */
$color: #4AD395;
$color-dark: #23004d;
$color-light: #a49eac;
$color-lighten: #f2f2f2;
$color-hover: #65bf97;
$font: "Open Sans", sans-serif;
$big-font-size: 1.5rem;
$normal-font-size: 0.938rem;
$small-font-size: 0.813rem;

@media screen and (min-width: 768px) {
  $normal-font-size: 1rem;
  $small-font-size: 0.875rem;
}

*, ::before, ::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: $font;
  font-size: $normal-font-size;
  color: $color-dark;
}

h1 {
  margin: 0;
  color: #23004d;
}

a {
  text-decoration: none;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}

.login {
  display: grid;
  grid-template-columns: 100%;
  height: 100vh;
  margin-left: 1.5rem;
  margin-right: 1.5rem;

  &__content {
    display: grid;
  }

  &__img {
    justify-self: center;

    img {
      width: 310px;
      margin-top: 1.5rem;
    }
  }

  &__forms {
    position: relative;
    height: 150px;
    margin: 0 25%;
  }

  &__register, &__create {
    position: absolute;
    bottom: 1rem;
    width: 100%;
    background-color: $color-lighten;
    padding: 2rem 1rem;
    border-radius: 1rem;
    text-align: center;
    box-shadow: 0 8px 20px rgba(35, 0, 77, .2);
    animation-duration: .4s;
    animation-name: animateLogin;
  }

  &__title {
    font-size: $big-font-size;
    margin-bottom: 2rem;
  }

  &__box {
    display: grid;
    grid-template-columns: max-content 1fr;
    column-gap: .5rem;
    padding: 1.125rem 1rem;
    background-color: #fff;
    margin-top: 1rem;
    border-radius: .5rem;
  }

  &__icon {
    font-size: 1.5rem;
    color: $color;
  }

  &__input {
    border: none;
    outline: none;
    font-size: $normal-font-size;
    font-weight: 700;
    color: $color-dark;
    width: 100%;

    &::placeholder {
      font-size: $normal-font-size;
      font-family: $font;
      color: $color-light;
    }
  }

  &__forgot {
    display: block;
    width: max-content;
    margin-left: auto;
    margin-top: .5rem;
    font-size: $small-font-size;
    font-weight: 600;
    color: $color-light;
  }

  &__button {
    width: 100%;
    padding: 1rem;
    padding: 0.75rem 2rem; /* 버튼 좌우 여백 추가 */
    margin-top: 1rem; /* 버튼과 입력 필드 간격 */
    background-color: $color;
    color: #fff;
    font-weight: 600;
    text-align: center;
    border-radius: .5rem;
    border: 2px solid $color-dark; /* 버튼 테두리 */
    transition: .3s;

    &:hover {
      background-color: $color-hover;
    }
  }

  &__account, &__signin, &__signup {
    font-weight: 600;
    font-size: $small-font-size;
    margin: 0.5rem; /* 버튼 사이 여백 추가 */

    &--account {
      color: $color-dark;
    }

    &--signin, &--signup {
      color: $color;
      cursor: pointer;
    }
  }
}

@keyframes animateLogin {
  0% {
    transform: scale(1, 1);
  }
  50% {
    transform: scale(1.1, 1.1);
  }
  100% {
    transform: scale(1, 1);
  }
}
</style>
