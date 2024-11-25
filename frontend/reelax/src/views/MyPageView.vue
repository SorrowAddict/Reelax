<template>
  <div class="container" v-if="currentUserInfo">
    <!-- 프로필 정보 -->
    <div class="profile-section" data-aos="fade-up">
      <div class="profile-header">
        <!-- 프로필 이미지 -->
        <img
          :src="profileImage || defaultProfileImage"
          alt="프로필 이미지"
          class="profile-image"
          @error="onImageError"
          @click="triggerImageUpload"
        />
        <input
          type="file"
          ref="imageInput"
          class="hidden"
          @change="uploadProfileImage"
          accept="image/*"
        />
        <div class="profile-info">
          <div class="user-name">
            <h1>
              <span v-if="!isEditingNickname">{{ currentUserInfo?.nickname || '사용자' }}</span>
              <input
                v-else
                type="text"
                v-model="nickname"
                class="nickname-input"
                @keyup.enter="updateNickname"
                @blur="cancelEditing"
              />
            </h1>
            <span v-if="isOwnProfile" class="edit-icon" @click="editNickname">✎</span>
            <div v-if="Number(route.params.id) !== accountStore.userId">
              <!-- 팔로우 버튼 -->
              <button class="follow-btn" @click="followToggle(route.params.id)" v-if="isFollowing">
                팔로우 취소
              </button>
              <button class="follow-btn" @click="followToggle(route.params.id)" v-else>
                팔로우
              </button>
            </div>
          </div>
          <div class="follow-info">
            <span data-bs-toggle="modal" data-bs-target="#followListModal">
              팔로워 {{ currentUserInfo.followers_count ?? 0 }}
            </span>
            <span data-bs-toggle="modal" data-bs-target="#followingListModal">
              팔로잉 {{ currentUserInfo.followings_count ?? 0 }}
            </span>
          </div>
          <div class="liked_genre">
            <div v-if="currentUserInfo.liked_genres.length === 0">
              
            </div>
            <div v-for="genre in currentUserInfo.liked_genres" :key="genre.genre_id"># {{ genre.name }}</div>
            <div v-if="isOwnProfile" class="add-genre" @click="goToGenreSelection"><font-awesome-icon :icon="['far', 'square-plus']" /></div>
          </div>
          
        </div>
      </div>
    </div>
    
    <div class="main-section">
        <!-- 영화 플레이리스트 -->
      <div class="playlist-section" data-aos="fade-up" data-aos-delay="150">
        
        <div class="content-box">
          <div class="playlist-header">
            <h2>{{ currentUserInfo?.nickname || '사용자' }}님의 영화 플레이리스트</h2>
            <button @click="seeAllPlaylist(route.params.id)" class="see-more">더보기</button>
          </div>
          <div v-if="currentUserInfo.playlists.length !== 0">
            <div class="playlist-box">
              <div v-for="playlist in currentUserInfo.playlists.slice(0, 4)" :key="playlist.id">
                <div class="playlist" @click="seePlaylistDetail(route.params.id, playlist.id)">
                  <ListThumbnail :movies="playlist.movies" />
                  <div class="list-name">
                    <h4>{{ playlist.title }}</h4>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <p v-else>플레이리스트가 비어 있습니다.</p>
        </div>
      </div>

      <!-- 좋아하는 영화 -->
      <div class="movie-section" data-aos="fade-up" data-aos-delay="150">
        <div class="content-box">
          <div class="movie-header">
            <h2>{{ currentUserInfo?.nickname || '사용자' }}님이 좋아한 영화</h2>
            <button @click="seeAllMovies(route.params.id)">더보기</button>
          </div>
          <div v-if="currentUserInfo.liked_movies.length !== 0">
            <div class="movie-box">
              <div v-for="movie in currentUserInfo.liked_movies.slice(0, 4)" :key="movie.movie_id">
                <MovieCard
                  :movie="movie"
                  class="movie"
                />
              </div>
            </div>
          </div>
          <p v-else>좋아하는 영화가 없습니다.</p>
        </div>
      </div>

      <!-- 좋아하는 감독 -->
      <div class="director-section" data-aos="fade-up" data-aos-delay="150">
        
        <div class="content-box">
          <div class="director-header">
            <h2>{{ currentUserInfo?.nickname || '사용자' }}님이 좋아한 감독</h2>
            <button @click="seeAllDirectors(route.params.id)">더보기</button>
          </div>
          <div v-if="currentUserInfo.liked_directors.length !== 0">
            <div class="director-box">
              <div v-for="director in currentUserInfo.liked_directors.slice(0, 4)" :key="director.director_id">
                <div @click="seeDirecDetail(director.director_id)">
                  <img :src="`https://image.tmdb.org/t/p/w200/${director.profile_path}`" alt="감독 프로필" class="director-image">
                  <div class="director-name">
                    <h3>{{ director.name }}</h3>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <p v-else>좋아하는 감독이 없습니다.</p>
        </div>
      </div>

      <!-- 좋아하는 배우 -->
      <div class="actor-section" data-aos="fade-up" data-aos-delay="150">
        
        <div class="content-box">
          <div class="actor-header">
            <h2>{{ currentUserInfo?.nickname || '사용자' }}님이 좋아한 배우</h2>
            <button @click="seeAllActors(route.params.id)">더보기</button>
          </div>
          <div v-if="currentUserInfo.liked_actors.length !== 0">
            <div class="actor-box">
              <div v-for="actor in currentUserInfo.liked_actors.slice(0, 4)" :key="actor.actor_id">
                <div @click="seeActorDetail(actor.actor_id)">
                  <img :src="`https://image.tmdb.org/t/p/w200/${actor.profile_path}`" alt="배우 프로필" class="actor-image">
                  <div class="actor-name">
                    <h3>{{ actor.name }}</h3>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <p v-else>좋아하는 배우가 없습니다.</p>
        </div>
      </div>
    </div>
    

    <!-- 팔로워/팔로잉 모달 -->
    <FollowListModal :users="currentUserInfo.followers" />
    <FollowingListModal :users="currentUserInfo.followings" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useAccountStore } from '@/stores/account'
import axios from 'axios'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { useRoute, useRouter } from 'vue-router'
import ListThumbnail from '@/components/MyPage/ListThumbnail.vue'
import FollowListModal from '@/components/MyPage/FollowListModal.vue'
import FollowingListModal from '@/components/MyPage/FollowingListModal.vue'
import MovieCard from '@/components/Movie/MovieCard.vue'

const accountStore = useAccountStore()
const route = useRoute()
const router = useRouter()
const defaultProfileImage = '/media/profile_images/default_profile.jpg'
const profileImage = ref(null)
const isOwnProfile = ref(null)

// 닉네임 수정 상태
const isEditingNickname = ref(false)
const nickname = ref('')

// 현재 사용자가 자신의 프로필 페이지를 보고 있는지 확인
// const isOwnProfile = computed(() => Number(route.params.id) === accountStore.userId)

// 현재 렌더링해야 할 사용자 데이터
const currentUserInfo = computed(() => {
  return isOwnProfile.value ? accountStore.loggedInUserInfo : accountStore.userInfo
})

// 컴포넌트 로드 시 데이터 가져오기
const loadUserInfo = async () => {
  if (isOwnProfile.value) {
    // 로그인한 사용자의 프로필 로드
    await accountStore.getLoggedInUserInfo()
  } else {
    // 다른 사용자의 프로필 로드
    await accountStore.getUserInfo(route.params.id)
  }

  // 프로필 이미지 설정
  const user = currentUserInfo.value
  profileImage.value = user?.profile_image
    ? `http://localhost:8000${user.profile_image}`
    : defaultProfileImage
}

// 라우트 변경 감지
watch(() => route.params.id, async (newId, oldId) => {
  if (newId !== oldId) {
    isOwnProfile.value = Number(newId) === accountStore.userId;
    await loadUserInfo()
  }
})

// 초기 데이터 로드
onMounted(async () => {
  AOS.init({
    duration: 800,
    easing: 'ease-in-out-quint',
    once: false,
  })
  isOwnProfile.value = Number(route.params.id) === accountStore.userId
  if (isOwnProfile.value !== undefined) {
    await loadUserInfo()
  }
  console.log(currentUserInfo.value)
})

// 프로필 이미지 업로드
const triggerImageUpload = () => {
  if (isOwnProfile) {
    const input = document.querySelector('input[type="file"]')
    input.click()
  }
}

const uploadProfileImage = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('profile_image', file)

  try {
    const response = await axios.put(
      'http://localhost:8000/api/v1/accounts/profile/update-image/',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${accountStore.token}`
        }
      }
    )
    profileImage.value = `http://localhost:8000${response.data.profile_image}`
    accountStore.loggedInUserInfo.profile_image = response.data.profile_image
    alert('프로필 이미지가 성공적으로 업데이트되었습니다.')
  } catch (error) {
    console.error('프로필 이미지를 업로드하는 중 오류가 발생했습니다.', error)
    alert('프로필 이미지를 업로드할 수 없습니다.')
  }
}

// 닉네임 수정
const editNickname = () => {
  if (isOwnProfile) {
    nickname.value = currentUserInfo.value?.nickname || ''
    isEditingNickname.value = true
  }
}

const cancelEditing = () => {
  isEditingNickname.value = false
}

const updateNickname = async () => {
  if (!nickname.value.trim()) return
  try {
    const response = await axios.patch(
      'http://localhost:8000/api/v1/accounts/user/',
      { nickname: nickname.value },
      {
        headers: {
          Authorization: `Bearer ${accountStore.token}`
        }
      }
    )
    accountStore.loggedInUserInfo.nickname = response.data.nickname
    await loadUserInfo()
    isEditingNickname.value = false
    alert('닉네임이 성공적으로 업데이트되었습니다.')
  } catch (error) {
    console.error('닉네임을 업데이트하는 중 오류가 발생했습니다.', error)
    alert('닉네임을 업데이트할 수 없습니다.')
  }
}

// 팔로우 상태 확인
const isFollowing = computed(() => {
  if (isOwnProfile.value) return null // 내 프로필에서는 팔로우 버튼 표시 안 함
  return currentUserInfo.value?.followers?.some(user => user.id === accountStore.userId)
})

const followToggle = async (user_id) => {
  await accountStore.follow(user_id)
  await loadUserInfo() // 팔로우 상태 갱신
}

// 프로필 이미지 로드 실패 시 기본 이미지로 대체
const onImageError = () => {
  profileImage.value = defaultProfileImage
}

// 상세 페이지 이동 함수들
const seeAllPlaylist = (user_id) => router.push({ name: 'MyPlaylistView', params: { id: user_id } })
const seePlaylistDetail = (user_id, playlist_id) => router.push({ name: 'MyPlaylistDetailView', params: { id: user_id, playlist_id } })
const seeAllMovies = (user_id) => router.push({ name: 'MyMovieView', params: { id: user_id } })
const seeMovieDetail = (movie_id) => router.push({ name: 'MovieDetailView', params: { id: movie_id } })
const seeAllDirectors = (user_id) => router.push({ name: 'MyDirectorView', params: { id: user_id } })
const seeDirecDetail = (director_id) => router.push({ name: 'DirecDetailView', params: { direc_id: director_id } })
const seeAllActors = (user_id) => router.push({ name: 'MyActorView', params: { id: user_id } })
const seeActorDetail = (actor_id) => router.push({ name: 'ActorDetailView', params: { actor_id } })
const goToGenreSelection = () => router.push({ name: 'GenreSelectionView', query: { from: "mypage" } })
</script>


<style scoped>
.main-section {
  max-width: 1200px;
  display: flex;
  flex-direction: column;
}
/* 전체 페이지 스타일 */
.hidden {
  display: none;
}

/* 프로필 섹션 */
.profile-section {
  margin-top: 40px;
  margin-bottom: 40px;
  border-bottom: 1px solid #666666;
  padding-bottom: 40px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-info h1 {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user-name {
  display: flex;
  align-items: center;
  gap: 5px;
}

.edit-icon {
  font-size: 24px;
  cursor: pointer;
  color: #ccc;
  transition: color 0.3s ease;
}

.follow-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin-left: 30px;
}

.follow-btn:hover {
  background-color: #5a6268;
  transform: translateY(-2px);
}

.follow-info {
  margin-top: 10px;
  display: flex;
  gap: 20px;
  font-size: 18px;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: #d9d9d9;
  object-fit: cover;
  cursor: pointer;
}

.nickname-input {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px;
  font-size: 18px;
}

.nickname {
  font-size: 24px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.liked_genre {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  margin-top: 20px
}

.add-genre {
  transition: transform 0.3s ease, color 0.3s ease;
}

.add-genre:hover {
  transform: scale(1.1);
}

.playlist-section, .movie-section, .director-section, .actor-section {
  margin-bottom: 40px;
  padding-bottom: 20px;
}
.playlist-box, .movie-box, .actor-box {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  text-align: center;
}

.playlist-header, .movie-header, .director-header, .actor-header {
  display: flex;
  margin-bottom: 20px;
}
.playlist-header button, .movie-header button, .director-header button, .actor-header button {
  all: unset;
  display: inline-block;
  margin-left: 20px;
  margin-bottom: 0px;
  color: #aaaaaa;
}

button:hover {
  color: white
}

.list-description {
  margin-top: 10px;
}

.director-box, .actor-box {
  display: flex;
  flex-wrap: wrap; /* 줄바꿈 활성화 */
  gap: 20px; /* 아이템 간격 */
  justify-content: flex-start; /* 왼쪽 정렬 */
}

.director-item, .actor-item {
  flex: 1 1 calc(25% - 20px); /* 한 줄에 4개 (간격 포함) */
  max-width: calc(25% - 20px); /* 최대 너비 */
  text-align: center; /* 텍스트 중앙 정렬 */
  transition: transform 0.3s ease;
  cursor: pointer;
}

.director-image, .actor-image {
  width: 100%;
  aspect-ratio: 2 / 2.5; /* 세로 비율 */
  border-radius: 16px; /* 둥근 모서리 */
  object-fit: cover; /* 이미지가 영역에 적합하도록 조정 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); /* 그림자 효과 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.director-image:hover, .actor-image:hover {
  transform: scale(1.05); /* 확대 효과 */
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4); /* hover 시 그림자 강화 */
}

.list-name h4 {
  font-size: 16px;
  margin-top: 10px;
  font-weight: bold;
  color: white; /* 텍스트 색상 */
  text-align: center;
}

.director-name h3 {
  font-size: 16px;
  margin-top: 10px;
  font-weight: bold;
  color: white; /* 텍스트 색상 */
  text-align: center;
}

.actor-name h3 {
  font-size: 16px;
  margin-top: 10px;
  font-weight: bold;
  color: white; /* 텍스트 색상 */
}

</style>
