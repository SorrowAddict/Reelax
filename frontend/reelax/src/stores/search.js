import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useSearchStore = defineStore('search', () => {
  const searchResults = ref(null)
  const searchQuery = ref('')
  const searchError = ref(null)
  const searchType = ref('movies')

  const BASE_URL = 'http://43.203.255.151/api/v1/movies'

  // 검색 요청
  const fetchSearchResults = function (query, type = 'movies') {
    searchError.value = null
    searchQuery.value = query
    searchType.value = type

    axios({
      method: 'get',
      url: `${BASE_URL}/search/${type}/`,
      params: { query }
    })
      .then((res) => {
        searchResults.value = res.data.results
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
    searchType,
    fetchSearchResults
  }
})
