import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './account'
import { useRouter } from 'vue-router'

export const useReviewStore = defineStore('review', () => {
  const BASE_URL = 'http://43.203.255.151:8000/api/v1/movies'
  const accountStore = useAccountStore()
  const router = useRouter()
  const movieReview = ref({})

  // 특정 영화 리뷰 가져오기
  const getMovieReview = function (movie_id) {
    axios({
      method: 'get',
      url: `${BASE_URL}/${movie_id}/reviews/`,
    })
      .then((res) => {
        movieReview.value = res.data.results
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 영화 리뷰 작성
  const createReview = function (movie_id, payload) {
    const { content } = payload
    axios({
      method: 'post',
      url: `${BASE_URL}/${movie_id}/reviews/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      },
      data: {
        content
      }
    })
      .then((res) => {
        console.log('리뷰 작성 성공!')
        getMovieReview(movie_id)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 영화 리뷰 좋아요
  const likeReview = function (movie_id, review_id) {
    axios({
      method: 'post',
      url: `${BASE_URL}/${movie_id}/reviews/${review_id}/like/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      }
    })
      .then((res) => {
        console.log('리뷰 좋아요 성공!')
        getMovieReview(movie_id)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 리뷰 수정
  const editReview = function (movie_id, review_id, payload) {
    const { content } = payload
    axios({
      method: 'put',
      url: `${BASE_URL}/${movie_id}/reviews/${review_id}/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      },
      data: {
        content
      }
    })
      .then((res) => {
        console.log('리뷰 수정 성공!')
        getMovieReview(movie_id)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 리뷰 삭제
  const deleteReview = function (movie_id, review_id) {
    axios({
      method: 'delete',
      url: `${BASE_URL}/${movie_id}/reviews/${review_id}/`,
      headers: {
        Authorization: `Bearer ${accountStore.token}`
      },
    })
      .then((res) => {
        console.log('리뷰 삭제 성공!')
        getMovieReview(movie_id)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {
    getMovieReview,
    movieReview,
    createReview,
    likeReview,
    editReview,
    deleteReview
  }
}, { persist: true })
