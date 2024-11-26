import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const BASE_URL = 'http://43.203.255.151/api/v1'
  const token = ref(null)
  const userInfo = ref(null)
  const loggedInUserInfo = ref(null)
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
  const getUserId = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/accounts/user/`, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      userId.value = res.data.pk
    } catch (err) {
      console.error('Failed to fetch user ID:', err)
    }
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

  const getLoggedInUserInfo = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/accounts/profile/${userId.value}/`, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      loggedInUserInfo.value = res.data
    } catch (err) {
      console.error('Failed to fetch logged-in user info:', err)
    }
  }

  const router = useRouter()

  // 이건 더 이상 현재 로그인한 사용자가 아니라
  // 그냥 아무 사용자의 info를 가져오는 로직이다.
  const getUserInfo = function (user_id) {
    return axios({
      method: 'get',
      url: `${BASE_URL}/accounts/profile/${user_id}/`,
      headers: {
        Authorization: `Bearer ${token.value}`
      },
    })
      .then((res) => {
        userInfo.value = res.data
        userprofile_path.value = res.data.profile_image
      })
      .catch((err) => {
        console.error(err)
      })
  }


  const logIn = async (payload) => {
    const { email, password } = payload
    try {
      const res = await axios.post(`${BASE_URL}/accounts/login/`, { email, password })
      token.value = res.data.access
      userId.value = res.data.user.pk
      if (token.value) {
        await getUserId()
        await getLoggedInUserInfo() // 로그인한 사용자 정보 로드
        router.push({ name: 'MainPageView' })
      }
    } catch (err) {
      console.error('Log in failed:', err)
    }
  }

  // const logIn = function (payload) {
  //   const { email, password } = payload
  //   axios({
  //     method: 'post',
  //     url: `${BASE_URL}/accounts/login/`,
  //     data: {
  //       email, password
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
    const { email, nickname, password1, password2 } = payload

    return axios({
      method: 'post',
      url: `${BASE_URL}/accounts/`,
      data: {
        email, nickname, password1, password2
      }
    })
      .then((res) => {
        console.log('회원가입이 완료되었습니다.', res.data.access)
        token.value = res.data.access
        if (token.value !== null) {
          getUserId()
            .then(() => getUserInfo(userId.value))
        }
        return res.data.access
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
    // axios({
    //   method: 'post',
    //   url: `${BASE_URL}/accounts/logout/`
    // })
    //   .then((res) => {
    //     console.log('로그아웃이 완료되었습니다.')
    //     token.value = null
    //     userId.value = null
    //     userInfo.value = null // userInfo 초기화
    //     loggedInUserInfo.value = null
    //     router.push({ name: 'MainPageView'})
    //   })
    //   .catch((err) => {
    //     console.log(err)
    //   })
    token.value = null
    userId.value = null
    loggedInUserInfo.value = null
    router.push({ name: 'MainPageView' })
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
  
  const follow = function (user_id) {
    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/follow-toggle/${user_id}/`,
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
      .then((res) => {
        getUserInfo(user_id)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {
    getUserId,
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
    userId,
    follow,
    loggedInUserInfo,
    getLoggedInUserInfo
  }
}, { persist: true })
