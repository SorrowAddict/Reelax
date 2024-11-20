import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const topRatedMovies = ref(null)
  const BASE_URL = 'http://127.0.0.1:8000/movies'
  
  const getTopRatedMovies = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/top-rated/`
    })
      .then((res) => {
        console.log(res)
        topRatedMovies.value = res.data.results
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return { getTopRatedMovies, topRatedMovies }
}, { persist: true })
