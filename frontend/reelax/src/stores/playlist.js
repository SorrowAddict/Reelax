import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './account'
import { useRouter } from 'vue-router'

export const usePlaylistStore = defineStore('playlist', () => {
  const BASE_URL = 'http://localhost:8000/api/v1/movies'
  // const BASE_URL = 'http://43.203.255.151:8000/api/v1/movies'
  const accountStore = useAccountStore()
  const router = useRouter()
  const playlist = ref({})

  const getPlaylist = function() {
    axios({
      method: 'get',
      url: `${BASE_URL}/playlists/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
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
        Authorization: `Bearer ${accountStore.token}`
      },
      data: {
        title, description, movies
      }
    })
      .then((res) => {
        console.log('생성 성공!')
        getPlaylist()
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const addMovieToPlaylist = function (playlist_id, movies) {
    axios({
      method: 'post',
      url: `${BASE_URL}/playlists/${playlist_id}/movies/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      },
      data: {
        movies
      }
    })
      .then((res) => {
        alert('성공적으로 추가되었습니다.')
        console.log('추가 성공!')
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const listDelete = function (user_id, playlist_id) {
    axios({
      method: 'delete',
      url: `${BASE_URL}/playlists/${playlist_id}/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      },
    })
      .then((res) => {
        alert('성공적으로 삭제 되었습니다.')
        router.push({ name: 'MyPlaylistView', params: { id: user_id }})
        console.log('삭제 성공!')
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const listDeleteMovie = function (user_id, playlist_id, movies) {
    axios({
      method: 'delete',
      url: `${BASE_URL}/playlists/${playlist_id}/movies/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      },
      data: {
        movies
      }
    })
      .then((res) => {
        alert('성공적으로 삭제 되었습니다.')
        window.location.reload()
        console.log('삭제 성공!')
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {
    getPlaylist,
    playlist,
    createPlaylist,
    addMovieToPlaylist,
    listDelete,
    listDeleteMovie
  }
}, { persist: true })
