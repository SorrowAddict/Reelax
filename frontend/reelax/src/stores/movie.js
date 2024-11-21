import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './account'

export const useMovieStore = defineStore('movie', () => {
  const topRatedMovies = ref(null)
  const boxOfficeMovies = ref(null)
  const recentlyReleasedMovies = ref(null)
  const genreMovies = ref(null)
  const userLikedGenreMovies = ref(null)
  const BASE_URL = 'http://127.0.0.1:8000/api/v1/movies'
  const accountStore = useAccountStore()
  
  // 평점 TOP 10 가져오기
  const getTopRatedMovies = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/top-rated/`
    })
      .then((res) => {
        topRatedMovies.value = res.data.results
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 박스오피스 TOP 10 가져오기
  const getBoxOfficeMovies = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/popular/`
    })
      .then((res) => {
        boxOfficeMovies.value = res.data.results
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 최근 개봉된 영화 가져오기
  const getRecentlyReleasedMovies = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/now-playing/`
    })
      .then((res) => {
        recentlyReleasedMovies.value = res.data.results
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 장르별 영화 가져오기
  const getGenreMovies = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/genre-movies/`,
      headers: accountStore.token ? { Authorization: `Token ${accountStore.token}` } : {}
    })
      .then((res) => {
        genreMovies.value = res.data.results
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const getUserLikedGenreMovies = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/user-liked-genre/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        userLikedGenreMovies.value = res.data.results
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return { 
    getTopRatedMovies,
    topRatedMovies,
    getBoxOfficeMovies,
    boxOfficeMovies,
    getRecentlyReleasedMovies,
    recentlyReleasedMovies,
    getGenreMovies,
    genreMovies,
    getUserLikedGenreMovies,
    userLikedGenreMovies
  }
}, { persist: true })
