import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './account'
import { useRouter } from 'vue-router'

export const useLikeStore = defineStore('like', () => {
  const BASE_URL = 'http://127.0.0.1:8000/api/v1/movies'
  const accountStore = useAccountStore()
  const router = useRouter()
  
  const movieLike = function(payload) {
    const { movie_id, poster_path } = payload
    axios({
      method: 'post',
      url: `${BASE_URL}/like-movie/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      },
      data: {
        movie_id, poster_path
      }
    })
      .then((res) => {
        accountStore.getUserInfo()
      })
      .catch((err) => {
        console.log(err)
      })
  }
  return {
    movieLike
  }
}, { persist: true })
