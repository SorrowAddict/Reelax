<template>
  <div>
    <h3>리뷰</h3>
    <div v-if="accountStore.isLogin">
      <form>
        <textarea id="">리뷰를 작성해보세요!</textarea>
        <button>작성</button>
      </form>
    </div>
    <div v-else>
      리뷰를 작성하려면 로그인 하세요!
    </div>
    <ReviewCard
      v-for="review in movieStore.movieReview"
      :key="review.id"
      :review="review"
    />
  </div>
</template>

<script setup>
import ReviewCard from './ReviewCard.vue'
import { useAccountStore } from '@/stores/account'
import { useMovieStore } from '@/stores/movie'
import { onMounted } from 'vue';
import { useRoute } from 'vue-router'

const accountStore = useAccountStore()
const movieStore = useMovieStore()
const route = useRoute()
const movie_id = route.params.id

onMounted(() => {
  movieStore.getMovieReview(movie_id)
})


</script>

<style scoped>

</style>