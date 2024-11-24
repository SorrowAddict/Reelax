<template>
  <div v-if="review" class="review-container" data-aos="fade-up">
    <div v-if="!isEditing" class="review-content">
      <div class="review-header">
        <div @click="moveToProfile(review.user.id)" class="user-profile">
          <div class="avatar">{{ review.user.nickname.charAt(0) }}</div>
          <span class="username">{{ review.user.nickname }}</span>
        </div>
        <div class="review-actions" v-if="review.user.id === accountStore.userInfo.id">
          <button @click="startEditingReview" class="btn-action edit">
            <font-awesome-icon :icon="['far', 'pen-to-square']" />
          </button>
          <button @click="deleteReview(movie_id, review.id)" class="btn-action delete">
            <font-awesome-icon :icon="['far', 'trash-can']" />
          </button>
        </div>
      </div>

      <div class="review-text">
        {{ review.content }}
      </div>

      <div class="review-footer">
        <div class="like-section">
          <button 
            @click="likeReview(movie_id, review.id)" 
            :class="['like-button', { 'liked': isReviewLiked }]"
            v-if="accountStore.isLogin"
          >
            <font-awesome-icon :icon="[isReviewLiked ? 'fas' : 'far', 'thumbs-up']" />
            <span class="like-count">{{ review.liked_by_count }}</span>
          </button>
          <div v-else class="like-button disabled">
            <font-awesome-icon :icon="['far', 'thumbs-up']" />
            <span class="like-count">{{ review.liked_by_count }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="edit-mode" data-aos="fade-in">
      <div class="edit-header">
        <div class="user-profile">
          <div class="avatar">{{ review.user.nickname.charAt(0) }}</div>
          <span class="username">{{ review.user.nickname }}</span>
        </div>
      </div>

      <form @submit.prevent="editReview(movie_id, review.id)" class="edit-form">
        <textarea 
          v-model="editContent" 
          class="edit-textarea"
          placeholder="리뷰를 수정하세요..."
        ></textarea>
        <div class="edit-actions">
          <button type="submit" class="btn-save">저장</button>
          <button type="button" @click="cancleEditing" class="btn-cancel">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAccountStore } from '@/stores/account'
import { useRoute, useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/review'
import AOS from 'aos'
import 'aos/dist/aos.css'

const accountStore = useAccountStore()
const reviewStore = useReviewStore()
const route = useRoute()
const router = useRouter()
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

const moveToProfile = function (user_id) {
  router.push({ name: 'MyPageView', params: { id: user_id }})
}

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
  accountStore.getUserInfo(accountStore.userId)
  AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: false,
  })
})

</script>

<style scoped>
.review-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.review-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
}

.username {
  font-weight: 600;
  color: #2d3748;
}

.review-text {
  color: #4a5568;
  line-height: 1.6;
  margin: 1rem 0;
  font-size: 1rem;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.like-button {
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.like-button:hover:not(.disabled) {
  background: #f7fafc;
  transform: scale(1.05);
}

.like-button.liked {
  background: #ebf8ff;
  border-color: #4299e1;
  color: #4299e1;
}

.like-button.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.like-count {
  font-weight: 600;
}

.btn-action {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #718096;
  transition: all 0.2s;
  border-radius: 6px;
}

.btn-action:hover {
  background: #f7fafc;
  color: #2d3748;
}

.btn-action.edit:hover {
  color: #4299e1;
}

.btn-action.delete:hover {
  color: #f56565;
}

.edit-mode {
  background: #f8fafc;
  border-radius: 12px;
  padding: 1.5rem;
}

.edit-form {
  margin-top: 1rem;
}

.edit-textarea {
  width: 100%;
  min-height: 120px;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 1rem;
  resize: vertical;
  transition: border-color 0.2s;
}

.edit-textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

.edit-actions {
  display: flex;
  gap: 0.75rem;
}

.btn-save,
.btn-cancel {
  padding: 0.5rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-save {
  background: #4299e1;
  color: white;
  border: none;
}

.btn-save:hover {
  background: #3182ce;
  transform: translateY(-1px);
}

.btn-cancel {
  background: white;
  color: #718096;
  border: 1px solid #e2e8f0;
}

.btn-cancel:hover {
  background: #f7fafc;
  color: #2d3748;
}

/* 반응형 스타일링 */
@media (max-width: 768px) {
  .review-container {
    padding: 1rem;
  }

  .review-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .review-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .edit-actions {
    flex-direction: column;
  }

  .btn-save,
  .btn-cancel {
    width: 100%;
  }
}

/* 작은 화면에서의 최적화 */
@media (max-width: 480px) {
  .review-container {
    margin-bottom: 1rem;
  }

  .avatar {
    width: 32px;
    height: 32px;
    font-size: 0.875rem;
  }

  .review-text {
    font-size: 0.875rem;
  }
}

/* AOS 애니메이션 커스텀 */
[data-aos] {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>