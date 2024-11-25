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
        Authorization: `Bearer ${accountStore.token}`
      },
      data: {
        movie_id, poster_path
      }
    })
      .then((res) => {
        accountStore.getUserInfo(accountStore.userId)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const direcLike = function(payload) {
    const { director_id, name, profile_path } = payload
    axios({
      method: 'post',
      url: `${BASE_URL}/like-director/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      },
      data: {
        director_id, name, profile_path
      }
    })
      .then((res) => {
        accountStore.getUserInfo(accountStore.userId)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const actorLike = function(payload) {
    const { actor_id, name, profile_path } = payload
    axios({
      method: 'post',
      url: `${BASE_URL}/like-actor/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      },
      data: {
        actor_id, name, profile_path
      }
    })
      .then((res) => {
        accountStore.getUserInfo(accountStore.userId)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {
    movieLike,
    direcLike,
    actorLike
  }
}, { persist: true })
