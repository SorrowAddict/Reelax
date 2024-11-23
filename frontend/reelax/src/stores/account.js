import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const BASE_URL = 'http://127.0.0.1:8000/api/v1'
  const token = ref(null)
  const userInfo = ref(null)
  // 이것도 로그인한 사용자의 정보를 담는 것이 아니라
  // 모든 사용자의 정보를 담는 것이다.
  const userprofile_path = ref(null)
  const isLogin = computed(() => {
    if (token.value !== null) {
      return true
    } else {
      return false
    }
  })
  const userId = ref(null)

  // 이건 현재 로그인한 사용자의 아이디를 가져오는 것
  const getUserId = function () {
    return axios({
      method: 'get',
      url: `${BASE_URL}/accounts/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
      .then((res) => {
        userId.value = res.data.pk
        console.log('User ID fetched:', userId.value)
      })
      .catch((err) => {
        console.error('Failed to fetch User ID:', err)
      })
  }
  // const getUserId = function () {
  //   axios({
  //     method: 'get',
  //     url: `${BASE_URL}/accounts/user/`,
  //     headers: {
  //       Authorization: `Token ${token.value}`
  //     },
  //   })
  //     .then((res) => {
  //       userId.value = res.data.pk
  //     })
  //     .catch((err) => {
  //       console.log(err)
  //     })
  // }
  const router = useRouter()

  // 이건 더 이상 현재 로그인한 사용자가 아니라
  // 그냥 아무 사용자의 info를 가져오는 로직이다.
  const getUserInfo = function (user_id) {
    return axios({
      method: 'get',
      url: `${BASE_URL}/accounts/profile/${user_id}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
      .then((res) => {
        userInfo.value = res.data
      })
      .catch((err) => {
        console.error(err)
      })
  }

  const logIn = function (payload) {
    const { username, password } = payload
    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/login/`,
      data: { username, password }
    })
      .then((res) => {
        console.log('로그인이 완료되었습니다.')
        token.value = res.data.key
  
        if (token.value !== null) {
          return getUserId() // getUserId 프로미스 반환
        }
      })
      .then(() => {
        console.log('User ID:', userId.value)
        if (userId.value !== null) {
          return getUserInfo(userId.value) // getUserInfo 호출
        }
      })
      .then(() => {
        router.push({ name: 'MainPageView' }) // 페이지 이동
      })
      .catch((err) => {
        console.error('로그인 또는 사용자 정보 로드 실패:', err)
      })
  }

  // const logIn = function (payload) {
  //   const { username, password } = payload
  //   axios({
  //     method: 'post',
  //     url: `${BASE_URL}/accounts/login/`,
  //     data: {
  //       username, password
  //     }
  //   })
  //     .then((res) => {
  //       console.log('로그인이 완료되었습니다.')
  //       token.value = res.data.key
  //       // if (token.value !== null) { 
  //       //   getUserId()
  //       //   if (userId.value !== null) {
  //       //     console.log(userId.value)
  //       //   }
  //       //     // .then(() => getUserInfo(userId.value))
  //       //     // .then(() => router.push({ name: 'MainPageView' }))
  //       // }
  //     })
  //     .then(() => {
  //       getUserId()
  //     })
  //     .then(() => {
  //       getUserInfo(userId.value)
  //       router.push({ name: 'MainPageView' })
  //     })
  //     .catch((err) => {
  //       console.log(err)
  //     })
  // }

  const signUp = function (payload) {
    const { username, nickname, password1, password2 } = payload

    return axios({
      method: 'post',
      url: `${BASE_URL}/accounts/registration/`,
      data: {
        username, nickname, password1, password2
      }
    })
      .then((res) => {
        console.log('회원가입이 완료되었습니다.')
        token.value = res.data.key
        if (token.value !== null) {
          getUserId()
            .then(() => getUserInfo(userId.value))
        }
        return res.data.key
      })
      .catch((err) => {
        // console.log(err)
        if (err.response.data) {
          const errorMessage = Object.values(err.response.data).join('\n')
          console.log(errorMessage)
          alert(errorMessage)
        }
        return null
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
        userId.value = null
        userInfo.value = null // userInfo 초기화
        router.push({ name: 'MainPageView'})
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // const fetchProfile = async function () {
  //   try {
  //     const res = await axios({
  //       method: 'get',
  //       url: `${BASE_URL}/accounts/profile/`,

  //     })
  //     userInfo.value = res.data
  //     // console.log(userInfo.value)
  //     userprofile_path.value = res.data.profile_image
  //     return res.data.profile_image
  //   } catch (err) {
  //     console.error(err)
  //     return null // 에러 발생 시 기본값 반환
  //   }
  // }  

  return {
    BASE_URL,
    signUp,
    logIn,
    token,
    isLogin,
    logOut,
    getUserInfo,
    userInfo,
    // fetchProfile,
    userprofile_path,
    userId
  }
}, { persist: true })
