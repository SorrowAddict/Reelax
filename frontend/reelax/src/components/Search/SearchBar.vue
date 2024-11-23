<template>
  <div class="search-bar">
    <FontAwesomeIcon icon="search" class="search-icon" />
    <input
      type="text"
      v-model="searchInput"
      :placeholder="animatedPlaceholder"
      class="form-control"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const searchInput = ref('')
const animatedPlaceholder = ref('')
const placeholderStrings = ['Search for movies...', 'Explore genres...', 'Find your favorites!']

let currentStringIndex = 0
let currentCharIndex = 0
let isDeleting = false
let debounceTimer = null
const router = useRouter()

const updatePlaceholder = () => {
  const currentString = placeholderStrings[currentStringIndex]

  if (!isDeleting) {
    animatedPlaceholder.value = currentString.slice(0, currentCharIndex++)
    if (currentCharIndex > currentString.length) {
      isDeleting = true
      setTimeout(updatePlaceholder, 2000)
      return
    }
  } else {
    animatedPlaceholder.value = currentString.slice(0, currentCharIndex--)
    if (currentCharIndex < 0) {
      isDeleting = false
      currentStringIndex = (currentStringIndex + 1) % placeholderStrings.length
    }
  }

  const delay = isDeleting ? 50 : 100
  setTimeout(updatePlaceholder, delay)
}

watch(searchInput, (newQuery) => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  debounceTimer = setTimeout(() => {
    if (newQuery.trim()) {
      router.push({ name: 'SearchPageView', query: { q: newQuery.trim() } })
    }
  }, 300)
})

onMounted(() => {
  updatePlaceholder()
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
