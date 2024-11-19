import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const BASE_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const isLogin = computed(() => {
    
  })
  const router = useRouter()

  if (token !== null) {
    
  }
  
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
        router.push({ name: 'MainPageView' })
        token.value = res.data.key
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const signUp = function (payload) {
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/registration/`,
      data: {
        username, password1, password2
      }
    })
      .then((res) => {
        console.log('회원가입이 완료되었습니다.')
        router.push({ name: 'MainPageView' })
        token.value = res.data.key
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return { BASE_URL, signUp, logIn, token }
})
