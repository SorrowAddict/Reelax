import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './account'
import { useRouter } from 'vue-router'

export const usePlaylistStore = defineStore('playlist', () => {
  const BASE_URL = 'http://127.0.0.1:8000/api/v1/movies'
  const accountStore = useAccountStore()
  const router = useRouter()
  const playlist = ref(null)

  const getPlaylist = function() {
    axios({
      method: 'get',
      url: `${BASE_URL}/playlists/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        playlist.value = res.data.results
        console.log(playlist.value)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const createPlaylist = function(payload) {
    const { title, description, movies } = payload
    axios({
      method: 'post',
      url: `${BASE_URL}/playlists/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      },
      data: {
        title, description, movies
      }
    })
      .then((res) => {
        console.log('생성 성공!')
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const addMovieToPlaylist = function (playlist_id, movies) {
    axios({
      method: 'put',
      url: `${BASE_URL}/playlists/${playlist_id}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      },
      data: {
        movies
      }
    })
      .then((res) => {
        console.log('추가 성공!')
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {
    getPlaylist,
    playlist,
    createPlaylist,
    addMovieToPlaylist
  }
}, { persist: true })
