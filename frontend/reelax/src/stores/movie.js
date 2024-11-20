import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const topRatedMovies = ref(null)
  const boxOfficeMovies = ref(null)
  const recentlyReleasedMovies = ref(null)
  const BASE_URL = 'http://127.0.0.1:8000/api/v1/movies'
  
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

  return { 
    getTopRatedMovies,
    topRatedMovies,
    getBoxOfficeMovies,
    boxOfficeMovies,
    getRecentlyReleasedMovies,
    recentlyReleasedMovies
  }
}, { persist: true })
