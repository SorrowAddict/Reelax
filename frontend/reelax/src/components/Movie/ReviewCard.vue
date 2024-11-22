<template>
  <div v-if="review">
    <div>
      {{ review.user.nickname }}
    </div>
    <div>
      {{ review.content }}
    </div>
    <div>
      <div v-if="isReviewLiked">
        <font-awesome-icon :icon="['fas', 'thumbs-up']" />
      </div>
      <div v-else>
        <font-awesome-icon :icon="['far', 'thumbs-up']" />
      </div>
      <div>
        {{ review.liked_by_count }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAccountStore } from '@/stores/account'

const accountStore = useAccountStore()

const props = defineProps({
  review: Object
})

const isReviewLiked = computed(() => {
  if (props.review.liked_by.includes(accountStore.userInfo.id)) {
    return true
  } else {
    return false
  }
})

onMounted(() => {
  accountStore.getUserInfo()
})


</script>

<style scoped>

</style>