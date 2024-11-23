<template>
  <div v-if="review">
    <div>
      {{ review.user.nickname }}
    </div>
    <div>
      <div>
        {{ review.content }}
      </div>
      <div>
        <font-awesome-icon :icon="['far', 'pen-to-square']" />
      </div>
    </div>
    
    <div>
      <div v-if="accountStore.isLogin">
        <div @click="likeReview(movie_id, review.id)">
          <div v-if="isReviewLiked">
            <font-awesome-icon :icon="['fas', 'thumbs-up']" />
          </div>
          <div v-else>
            <font-awesome-icon :icon="['far', 'thumbs-up']" />
          </div>
        </div>
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
import { useRoute } from 'vue-router'
import { useReviewStore } from '@/stores/review'

const accountStore = useAccountStore()
const reviewStore = useReviewStore()
const route = useRoute()
const movie_id = route.params.id

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

const likeReview = function (movie_id, review_id) {
  reviewStore.likeReview(movie_id, review_id)
}

onMounted(() => {
  accountStore.getUserInfo()
})


</script>

<style scoped>

</style>