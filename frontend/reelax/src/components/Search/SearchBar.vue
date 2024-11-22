<template>
  <div class="search-bar">
    <FontAwesomeIcon icon="search" class="search-icon" />
    <input
      type="text"
      class="form-control"
      v-model="searchQuery"
      placeholder="Search for movies..."
      @keyup.enter="performSearch"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const searchQuery = ref('')
const router = useRouter()

const performSearch = () => {
  if (!searchQuery.value.trim()) {
    alert('Please enter a valid search query!')
    return
  }

  // 라우터를 통해 검색 페이지로 이동
  router.push({ name: 'SearchPageView', query: { q: searchQuery.value } })

  // 검색 후 검색어 초기화
  searchQuery.value = ''
}
</script>

<style scoped>
.search-bar {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 10px;
  color: #bbb;
}

.form-control {
  padding-left: 2rem;
}
</style>
