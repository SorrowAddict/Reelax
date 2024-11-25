<template>
  <div class="director-page" >
    <div v-if="isLoading" class="spinner-container">
      <div class="spinner"></div>
    </div>
    <div v-else>
      <div class="container py-5" v-if="movieStore.direcDetail">
        <!-- 상단 프로필 섹션 -->
        <div class="director-profile mb-5" data-aos="fade-up">
          <div class="row align-items-center">
            <!-- 프로필 이미지 -->
            <div class="col-md-4 mb-4 mb-md-0">
              <div class="profile-image-container">
                <img :src="imageUrl" alt="프로필 이미지" class="profile-image">
              </div>
            </div>
            <!-- 감독 정보 -->
            <div class="col-md-8">
              <div class="director-info">
                <h3 class="director-name">{{ movieStore.direcDetail.name }}</h3>
                <p class="director-role">감독</p>
                <div class="director-details">
                  <p class="birth-year">{{ movieStore.direcDetail?.birthday }}</p>
                  <p class="gender">{{ movieStore.direcDetail?.gender === 2 ? '남성' : movieStore.direcDetail?.gender === 1 ? '여성' : '정보 없음' }}</p>
                </div>
                <!-- 좋아요 버튼 -->
                <div class="like-button-container">
                  <div v-if="accountStore.isLogin" class="like-button" @click="direcLike(movieStore.direcDetail.id, movieStore.direcDetail.name, movieStore.direcDetail.profile_path)">
                    <div v-if="isDirectorLiked(movieStore.direcDetail)">
                      <font-awesome-icon :icon="['fas', 'heart']" class="heart-icon liked" />
                    </div>
                    <div v-else>
                      <font-awesome-icon :icon="['far', 'heart']" class="heart-icon" />
                    </div>
                  </div>
                  <div v-else class="like-button" @click="moveToLogin">
                    <font-awesome-icon :icon="['far', 'heart']" class="heart-icon" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 필모그래피 섹션 -->
        <div class="filmography-section" data-aos="fade-up" data-aos-delay="200">
          <h2 class="section-title mb-4 text-center">{{ movieStore.direcDetail.name }} 감독이 연출한 영화</h2>
          <div class="filmography-container">
            <div class="movies-grid">
              <MovieCard
                v-for="movie in uniqueFilmography"
                :key="movie.id"
                :movie="movie"
                class="movie-card-wrapper"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { useMovieStore } from '@/stores/movie'
import { useAccountStore } from '@/stores/account'
import { useRoute, useRouter } from 'vue-router'
import MovieCard from '@/components/Movie/MovieCard.vue'
import { useLikeStore } from '@/stores/like'

const movieStore = useMovieStore()
const accountStore = useAccountStore()
const likeStore = useLikeStore()
const route = useRoute()
const router = useRouter()
const isLoading = ref(true); // 로딩 상태 초기화

watch(
  () => movieStore.direcDetail, // movieStore.direcDetail 변화를 감시
  (newValue) => {
    if (newValue) {
      isLoading.value = false; // 데이터가 로드되면 로딩 상태를 false로 변경
    }
  }
);


const direc_id = route.params.direc_id

const defaultImage = "/image/basic_profile.png"
const imageUrl = computed(() => {
  if(movieStore.direcDetail.profile_path) {
    return `https://image.tmdb.org/t/p/w200${movieStore.direcDetail.profile_path}`
  } else {
    return `${defaultImage}`
  }
})

const birth_year = computed(() => {
  return movieStore.direcDetail.birthday.substring(0, 4)
})

const gender = computed(() => {
  if (movieStore.direcDetail.gender === 2) {
    return '남성'
  } else if (movieStore.direcDetail.gender === 1) {
    return '여성'
  } else {
    return '알 수 없음'
  }
})

const liked_directors = computed(() => accountStore.userInfo.liked_directors)

const isDirectorLiked = function (director) {
  return liked_directors.value.some((liked_director) => liked_director.director_id === director.id)
}

const uniqueFilmography = computed(() => {
  const seenIds = new Set();
  return movieStore.direcDetail.filmography.filter((movie) => {
    if (!seenIds.has(movie.id)) {
      seenIds.add(movie.id);
      return true;
    }
    return false;
  });
});

const direcLike = function (director_id, name, profile_path) {
  const payload = {
    director_id: director_id,
    name: name,
    profile_path: profile_path
  }
  likeStore.direcLike(payload)
}

const moveToLogin = function () {
  alert('로그인이 필요한 기능입니다.')
  router.push({ name: 'LoginPageView' })
}

onMounted(() => {
  movieStore.getDirectorDetail(direc_id)
  console.log(movieStore.direcDetail)
  if (accountStore.isLogin) {
    accountStore.getUserInfo(accountStore.userId)
  }
})

</script>

<style scoped>
.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

/* 스피너 애니메이션 */
.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #ccc; /* 회색 테두리 */
  border-top: 5px solid #007bff; /* 파란색 테두리 */
  border-radius: 50%; /* 원 모양 */
  animation: spin 1s linear infinite;
}

/* 애니메이션 키프레임 */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.director-page {
  background-color: #2d2d2d;
  min-height: 100vh;
  color: white;
}

.director-profile {
  background-color: #383838;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.profile-image-container {
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

.profile-image {
  width: 100%;
  height: auto;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.profile-image:hover {
  transform: scale(1.02);
}

.director-info {
  padding-left: 1rem;
}

.director-name {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: white;
}

.director-role {
  font-size: 1.2rem;
  color: #e0e0e0;
  margin-bottom: 1rem;
}

.director-details {
  margin-bottom: 1.5rem;
}

.director-details p {
  font-size: 1.1rem;
  color: #e0e0e0;
  margin-bottom: 0.5rem;
}

.like-button {
  display: inline-block;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.like-button:hover {
  transform: scale(1.1);
}

.heart-icon {
  font-size: 1.5rem;
  color: #dc3545;
}

.heart-icon.liked {
  color: #dc3545;
  animation: heartBeat 0.3s ease-in-out;
}

.section-title {
  font-size: 2rem;
  font-weight: 600;
  color: white;
  margin-top: 2rem;
}

.filmography-section {
  background-color: #383838;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.filmography-container {
  padding: 0 1rem;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 280px); /* MovieCard width + margin */
  gap: 2rem;
  justify-content: center;
  margin: 0 auto;
  max-width: 1400px; /* Prevent too wide layout */
}

.movie-card-wrapper {
  width: 250px; /* Match MovieCard width */
  margin: 0 auto;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .director-info {
    padding-left: 0;
    text-align: center;
    margin-top: 1rem;
  }

  .profile-image-container {
    max-width: 200px;
  }

  .director-name {
    font-size: 2rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .movies-grid {
    grid-template-columns: repeat(auto-fill, 260px);
    gap: 1.5rem;
  }
}

/* 작은 화면에서의 그리드 조정 */
@media (max-width: 576px) {
  .movies-grid {
    grid-template-columns: repeat(auto-fill, 250px);
    gap: 1rem;
  }

  .filmography-container {
    padding: 0 0.5rem;
  }
}
</style>