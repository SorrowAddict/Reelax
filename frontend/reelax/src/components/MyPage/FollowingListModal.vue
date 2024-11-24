<template>
  <div>
    <div class="modal fade" id="followingListModal" tabindex="-1" aria-labelledby="followingListModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="followingListModalLabel">팔로잉 목록</h1>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-for="user in users" :key="user.id">
              <p @click="goToProfile(user.id)">{{ user.nickname }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
defineProps({
  users: Object
})

const goToProfile = function (user_id) {
  router.push({ name: 'MyPageView', params: { id: user_id }})
}
</script>

<style scoped>
.modal-content {
  background-color: #2d2d2d;
}
</style>