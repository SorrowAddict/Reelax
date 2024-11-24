<template>
  <div v-if="accountStore.userInfo" class="container">
    <h1 class="title">{{ accountStore.userInfo?.nickname || '사용자' }}님이 좋아한 감독</h1>
    <div class="directors-grid">
      <div class="director-item" v-for="director in accountStore.userInfo.liked_directors" :key="director.director_id">
        <img
          @click="seeDirectorDetail(director.director_id)"
          :src="`https://image.tmdb.org/t/p/w200/${director.profile_path}`"
          alt="감독 사진"
          class="director-image"
        />
        <p class="director-name">{{ director.name }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account'
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const user_id = route.params.id
const accountStore = useAccountStore()

const seeDirectorDetail = function (direc_id) {
  router.push({ name: 'DirecDetailView', params: { direc_id: direc_id }})
}

onMounted(() => {
  accountStore.getUserInfo(user_id)
})
</script>

<style scoped>
/* 제목 스타일 */
.title {
  margin: 20px 0;
  color: white;
}

/* 감독 리스트 그리드 */
.directors-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 20px;
  padding: 20px;
}

/* 각 감독 카드 스타일 */
.director-item {
  flex: 1 1 calc(20% - 20px); /* 한 줄에 5개 */
  max-width: calc(20% - 20px); /* 최대 너비 제한 */
  text-align: center;
  color: white;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.director-item:hover {
  transform: scale(1.05);
}

/* 감독 이미지 스타일 */
.director-image {
  width: 100%;
  aspect-ratio: 2 / 2.5; /* 세로 비율을 더 크게 설정 */
  border-radius: 16px; /* 둥글게 */
  object-fit: cover; /* 이미지가 영역에 적합하도록 조정 */
  cursor: pointer;
  transition: transform 0.3s ease;
}

.director-image:hover {
  transform: scale(1.05);
}

/* 감독 이름 스타일 */
.director-name {
  margin-top: 10px;
  font-size: 14px;
  font-weight: bold;
  color: white;
}

/* 반응형 스타일 */
@media (max-width: 992px) {
  .director-item {
    flex: 1 1 calc(25% - 20px); /* 한 줄에 4개 */
    max-width: calc(25% - 20px);
  }
}

@media (max-width: 768px) {
  .director-item {
    flex: 1 1 calc(33.33% - 20px); /* 한 줄에 3개 */
    max-width: calc(33.33% - 20px);
  }
}

@media (max-width: 576px) {
  .director-item {
    flex: 1 1 calc(50% - 20px); /* 한 줄에 2개 */
    max-width: calc(50% - 20px);
  }
}
</style>
