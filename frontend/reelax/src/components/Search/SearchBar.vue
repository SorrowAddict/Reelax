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
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const searchInput = ref('')
const animatedPlaceholder = ref('')
const placeholderStrings = ['Search for movies...', 'Search for people...', 'Search for TV shows!']

const props = defineProps({
  selectedSearchType: {
    type: String,
    required: true
  }
})

const router = useRouter()
let debounceTimer = null

watch([searchInput, () => props.selectedSearchType], ([query, type]) => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    if (query.trim()) {
      router.push({ name: 'SearchPageView', query: { q: query.trim(), type } })
    }
  }, 300)
})

onMounted(() => {
  let currentStringIndex = 0
  let currentCharIndex = 0
  let isDeleting = false

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

    setTimeout(updatePlaceholder, isDeleting ? 50 : 100)
  }

  updatePlaceholder()
})
</script>


<style scoped>
.search-bar {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #bbb;
}

.form-control {
  width: 100%;
  padding: 8px 10px;
  padding-left: 30px; /* 아이콘 간격 */
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-control:focus {
  outline: none;
}
</style>