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
  console.log(reviewStore.movieReview)
})


</script>

<style scoped>
h3 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 15px;
  text-transform: uppercase;
  letter-spacing: 1.2px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #1c1c1e;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
}

textarea {
  resize: none;
  padding: 15px;
  font-size: 1rem;
  border-radius: 5px;
  border: none;
  outline: none;
  background: #2b2b2e;
  color: #ffffff;
  font-family: 'Inter', sans-serif;
}

textarea::placeholder {
  color: #999;
}

button {
  align-self: flex-start;
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  background-color: #1e90ff;
  color: #ffffff;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

button:hover {
  background-color: #00bfff;
  transform: translateY(-2px);
}

div {
  margin-top: 20px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
}

.ReviewCard {
  margin-top: 20px;
  padding: 20px;
  background-color: #2b2b2e;
  border-radius: 10px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.ReviewCard:hover {
  transform: translateY(-5px);
  box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.3);
}
</style>
