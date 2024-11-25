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
  const userLikedMovies = ref(null)
  const userLikedActorMovies = ref(null)
  const userLikedActor = ref(null)
  const userLikedDirecMovies = ref(null)
  const userLikedDirec = ref(null)
  const movieDetail = ref(null)
  const movieReview = ref(null)
  const direcDetail = ref(null)
  const actorDetail = ref(null)

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
      headers: accountStore.token ? { Authorization: `Bearer ${accountStore.token}` } : {}
    })
      .then((res) => {
        genreMovies.value = res.data.results
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 유저가 좋아한 랜덤 장르 영화 가져오기
  const getUserLikedGenreMovies = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/user-liked-genre/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      }
    })
      .then((res) => {
        userLikedGenreMovies.value = res.data.results
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 유저가 좋아한 영화 5개 가져오기
  const getUserLikedMovies = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/user-liked-movies/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      }
    })
      .then((res) => {
        userLikedMovies.value = res.data.results
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 유저가 좋아한 랜덤 배우 영화 가져오기
  const getUserLikedActorMovies = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/user-liked-actor/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      }
    })
      .then((res) => {
        userLikedActorMovies.value = res.data.results
        userLikedActor.value = res.data.name
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 유저가 좋아한 랜덤 감독 영화 가져오기
  const getUserLikedDirecMovies = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/user-liked-director/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      }
    })
      .then((res) => {
        userLikedDirecMovies.value = res.data.results
        userLikedDirec.value = res.data.name
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const movieDetailLoading = ref(false)

  // 영화 상세 정보 가져오기
  const getMovieDetail = function (movie_id) {
    axios({
      method: 'get',
      url: `${BASE_URL}/${movie_id}/`,
      headers: accountStore.token ? { Authorization: `Bearer ${accountStore.token}` } : {}
    })
    .then((res) => {
      movieDetail.value = res.data
      movieDetailLoading.value = true
    })
    .catch((err) => {
      console.log(err)
    }).finally(() => {
      movieDetailLoading.value = false
    })
  }

  // 영화 감독 상세 정보 가져오기
  const getDirectorDetail = function (direc_id) {
    axios({
      method: 'get',
      url: `${BASE_URL}/director/${direc_id}/`
    })
      .then((res) => {
        direcDetail.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const getActorDetail = function (actor_id) {
    axios({
      method: 'get',
      url: `${BASE_URL}/actor/${actor_id}/`
    })
      .then((res) => {
        actorDetail.value = res.data
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
    userLikedGenreMovies,
    getUserLikedMovies,
    userLikedMovies,
    getUserLikedActorMovies,
    userLikedActorMovies,
    userLikedActor,
    getUserLikedDirecMovies,
    userLikedDirecMovies,
    userLikedDirec,
    getMovieDetail,
    movieDetail,
    getDirectorDetail,
    direcDetail,
    getActorDetail,
    actorDetail
  }
}, { persist: true })
