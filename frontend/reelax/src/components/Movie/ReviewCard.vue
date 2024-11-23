<template>
  <div v-if="review">
    <div v-if="!isEditing">
      <div>
        {{ review.user.nickname }}
      </div>
      <div>
        {{ review.content }}
      </div>
      <div class="like-count-edit">
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
        <div @click="startEditingReview" v-if="review.user.id === accountStore.userInfo.id">
          <font-awesome-icon :icon="['far', 'pen-to-square']" />
        </div>
        <div @click="deleteReview(movie_id, review.id)" v-if="review.user.id === accountStore.userInfo.id">
          <font-awesome-icon :icon="['far', 'trash-can']" />
        </div>
      </div>
    </div>
    <div v-else>
      <div>
        {{ review.user.nickname }}
      </div>
      <form @submit.prevent="editReview(movie_id, review.id)">
        <textarea v-model="editContent" class="edit-textarea"></textarea>
        <div class="edit-actions">
          <button type="submit">저장</button>
          <button type="button" @click="cancleEditing">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
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

const isEditing = ref(false)
const editContent = ref('')

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

const startEditingReview = function () {
  isEditing.value = true
  editContent.value = props.review.content
}

const cancleEditing = function () {
  isEditing.value = false
  editContent.value = ''
}

const editReview = function (movie_id, review_id) {
  const payload = {
    content: editContent.value
  }
  reviewStore.editReview(movie_id, review_id, payload)
  isEditing.value = false
}

const deleteReview = function (movie_id, review_id) {
  reviewStore.deleteReview(movie_id, review_id)
}

onMounted(() => {
  accountStore.getUserInfo()
})

</script>

<style scoped>
.like-count-edit {
  display: flex;
  gap: 5px;
}

.edit-textarea {
  width: 100%;
  height: 80px;
  margin-bottom: 10px;
}

.edit-actions {
  display: flex;
  gap: 10px;
}
</style>