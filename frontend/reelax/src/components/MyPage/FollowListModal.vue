<template>
  <div>
    <div class="modal fade" id="followListModal" tabindex="-1" aria-labelledby="followListModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="followListModalLabel">팔로워 목록</h1>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="users && users.length" class="user-grid">
              <div v-for="user in users" :key="user.id" class="user-item" @click="goToProfile(user.id)" data-bs-dismiss="modal">
                {{ user.nickname }}
              </div>
            </div>
            <div v-else class="no-users">
              <p>팔로워가 없습니다.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
defineProps({
  users: Array
});

const goToProfile = function (user_id) {
  router.push({ name: 'MyPageView', params: { id: user_id } });
};
</script>

<style scoped>
.modal-content {
  background-color: #2d2d2d;
  color: white;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
  padding: 20px;
}

/* 사용자 그리드 스타일 */
.user-grid {
  display: flex;
  flex-wrap: wrap; /* 줄바꿈 활성화 */
  gap: 10px; /* 사용자 간 간격 */
  justify-content: flex-start; /* 왼쪽 정렬 */
}

/* 사용자 아이템 스타일 */
.user-item {
  padding: 8px 12px;
  background-color: #3a3a3a;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  color: white;
  text-align: center;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.user-item:hover {
  background-color: #555555;
  transform: translateY(-3px);
}

/* 팔로워 목록 없을 때 */
.no-users {
  text-align: center;
  font-size: 16px;
  color: #aaa;
  padding: 20px 0;
}
</style>
