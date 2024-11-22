<template>
  <div class="search-bar">
    <FontAwesomeIcon icon="search" class="search-icon" />
    <input
      type="text"
      v-model="searchInput"
      placeholder="Search for movies..."
      class="form-control"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const searchInput = ref('') // 검색 입력 값
let debounceTimer = null // 디바운스 타이머
const router = useRouter()

// 디바운스 처리: 입력 변경 시 일정 시간 후 라우터로 이동
watch(searchInput, (newQuery) => {
  if (debounceTimer) {
    clearTimeout(debounceTimer) // 기존 타이머 취소
  }
  debounceTimer = setTimeout(() => {
    if (newQuery.trim()) {
      router.push({ name: 'SearchPageView', query: { q: newQuery.trim() } }) // 검색 실행
    }
  }, 300) // 300ms 디바운스 시간
})
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
  width: 100%;
}
</style>
