import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const BASE_URL = 'http://127.0.0.1:8000/api/v1'
  const token = ref(null)
  const userInfo = ref(null)
  const isLogin = computed(() => {
    if (token.value !== null) {
      return true
    } else {
      return false
    }
  })
  const router = useRouter()
  
  const logIn = function (payload) {
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        console.log('로그인이 완료되었습니다.')
        token.value = res.data.key
        router.push({ name: 'MainPageView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const getUserInfo = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/accounts/login/`
    })
  }

  const signUp = function (payload) {
    const { username, nickname, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/registration/`,
      data: {
        username, nickname, password1, password2
      }
    })
      .then((res) => {
        console.log('회원가입이 완료되었습니다.')
        router.push({ name: 'MainPageView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const logOut = function () {
    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/logout/`
    })
      .then((res) => {
        console.log('로그아웃이 완료되었습니다.')
        token.value = null
        console.log(token.value)
        router.push({ name: 'MainPageView'})
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return { BASE_URL, signUp, logIn, token, isLogin, logOut }
}, { persist: true })
