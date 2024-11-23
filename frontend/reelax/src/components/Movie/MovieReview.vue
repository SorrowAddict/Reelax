<template>
  <div>
    <h3>리뷰</h3>
    <div v-if="accountStore.isLogin">
      <form @submit.prevent="createReview(movie_id)">
        <textarea v-model="content">리뷰를 작성해보세요!</textarea>
        <button type="submit">작성</button>
      </form>
    </div>
    <div v-else>
      리뷰를 작성하려면 로그인 하세요!
    </div>
    <div v-if="reviewStore.movieReview.length === 0">
      아직 작성된 리뷰가 없습니다
    </div>
    <div v-else>
      <ReviewCard
        v-for="review in reviewStore.movieReview"
        :key="review.id"
        :review="review"
      />
    </div>
  </div>
</template>

<script setup>
import ReviewCard from './ReviewCard.vue'
import { useAccountStore } from '@/stores/account'
import { useReviewStore } from '@/stores/review'
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'

const accountStore = useAccountStore()
const reviewStore = useReviewStore()
const route = useRoute()
const content = ref(null)
const movie_id = route.params.id

const createReview = function (movie_id) {
  const payload = {
    content: content.value
  }
  console.log(movie_id)
  reviewStore.createReview(movie_id, payload)
  content.value = null
}

onMounted(() => {
  reviewStore.getMovieReview(movie_id)
})


</script>

<style scoped>

</style>