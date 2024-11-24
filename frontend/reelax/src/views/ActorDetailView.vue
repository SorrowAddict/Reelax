<template>
  <div class="actor-page">
    <div class="container py-5" v-if="movieStore.actorDetail">
      <!-- 상단 프로필 섹션 -->
      <div class="actor-profile mb-5" data-aos="fade-up">
        <div class="row align-items-center">
          <!-- 프로필 이미지 -->
          <div class="col-md-4 mb-4 mb-md-0">
            <div class="profile-image-container">
              <img :src="imageUrl" alt="프로필 이미지" class="profile-image">
            </div>
          </div>
          <!-- 배우 정보 -->
          <div class="col-md-8">
            <div class="actor-info">
              <h3 class="actor-name">{{ movieStore.actorDetail.name }}</h3>
              <p class="actor-role">배우</p>
              <div class="actor-details">
                <p class="birth-year">{{ birth_year }}</p>
                <p class="gender">{{ gender }}</p>
              </div>
              <!-- 좋아요 버튼 -->
              <div class="like-button-container">
                <div v-if="accountStore.isLogin" class="like-button" @click="actorLike(movieStore.actorDetail.id, movieStore.actorDetail.name, movieStore.actorDetail.profile_path)">
                  <div v-if="isActorLiked(movieStore.actorDetail)">
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
        <h2 class="section-title mb-4 text-center">{{ movieStore.actorDetail.name }} 배우가 출연한 영화</h2>
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
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useMovieStore } from '@/stores/movie'
import { useAccountStore } from '@/stores/account'
import { useRoute, useRouter } from 'vue-router'
import MovieCard from '@/components/Movie/MovieCard.vue'
import { useLikeStore } from '@/stores/like';

const movieStore = useMovieStore()
const accountStore = useAccountStore()
const likeStore = useLikeStore()
const route = useRoute()
const router = useRouter()

const actor_id = route.params.actor_id

const defaultImage = "/image/basic_profile.png"
const imageUrl = computed(() => {
  if(movieStore.actorDetail.profile_path) {
    return `https://image.tmdb.org/t/p/w200${movieStore.actorDetail.profile_path}`
  } else {
    return `${defaultImage}`
  }
})

const birth_year = computed(() => {
  return movieStore.actorDetail.birthday.substring(0, 4)
})

const gender = computed(() => {
  if (movieStore.actorDetail.gender === 2) {
    return '남성'
  } else if (movieStore.actorDetail.gender === 1) {
    return '여성'
  } else {
    return '알 수 없음'
  }
})

const liked_actors = computed(() => accountStore.userInfo.liked_actors)

const isActorLiked = function (actor) {
  return liked_actors.value.some((liked_actor) => liked_actor.actor_id === actor.id)
}

const uniqueFilmography = computed(() => {
  const seenIds = new Set();
  return movieStore.actorDetail.filmography.filter((movie) => {
    if (!seenIds.has(movie.id)) {
      seenIds.add(movie.id);
      return true;
    }
    return false;
  });
});

const actorLike = function (actor_id, name, profile_path) {
  const payload = {
    actor_id: actor_id,
    name: name,
    profile_path: profile_path
  }
  likeStore.actorLike(payload)
}

const moveToLogin = function () {
  alert('로그인이 필요한 기능입니다.')
  router.push({ name: 'LoginPageView' })
}

onMounted(() => {
  movieStore.getActorDetail(actor_id)
  if (accountStore.isLogin) {
    accountStore.getUserInfo(accountStore.userId)
  }
})
</script>

<style scoped>
.actor-page {
  background-color: #2d2d2d;
  min-height: 100vh;
  color: white;
}

.actor-profile {
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

.actor-info {
  padding-left: 1rem;
}

.actor-name {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: white;
}

.actor-role {
  font-size: 1.2rem;
  color: #e0e0e0;
  margin-bottom: 1rem;
}

.actor-details {
  margin-bottom: 1.5rem;
}

.actor-details p {
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
  grid-template-columns: repeat(auto-fill, 280px);
  gap: 2rem;
  justify-content: center;
  margin: 0 auto;
  max-width: 1400px;
}

.movie-card-wrapper {
  width: 250px;
  margin: 0 auto;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .actor-info {
    padding-left: 0;
    text-align: center;
    margin-top: 1rem;
  }

  .profile-image-container {
    max-width: 200px;
  }

  .actor-name {
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