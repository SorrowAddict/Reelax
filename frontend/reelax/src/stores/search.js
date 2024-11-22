import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useSearchStore = defineStore('search', () => {
  const searchResults = ref(null)
  const searchQuery = ref('')
  const searchError = ref(null)

  const BASE_URL = 'http://127.0.0.1:8000/api/v1/movies'

  // 검색 요청
  const fetchSearchResults = function (query) {
    searchError.value = null // 오류 초기화
    searchQuery.value = query // 검색어 저장

    axios({
      method: 'get',
      url: `${BASE_URL}/search/`,
      params: { query } // 쿼리 파라미터 전달
    })
      .then((res) => {
        searchResults.value = res.data.results // 결과 저장
      })
      .catch((err) => {
        searchError.value = err.response?.data?.error || 'An unexpected error occurred'
        console.error('Error details:', err.response?.data)
      })
  }

  return {
    searchResults,
    searchQuery,
    searchError,
    fetchSearchResults
  }
})
