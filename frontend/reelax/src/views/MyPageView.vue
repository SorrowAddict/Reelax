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
          v-if="isOwnProfile"
        />
        <div class="profile-info">
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
            <span class="edit-icon" @click="editNickname">✎</span>
          </h1>
          <div class="follow-info">
            <span data-bs-toggle="modal" data-bs-target="#followListModal">
              팔로우 {{ currentUserInfo.followers_count ?? 0 }}
            </span>
            <span data-bs-toggle="modal" data-bs-target="#followingListModal">
              팔로잉 {{ currentUserInfo.followings_count ?? 0 }}
            </span>
          </div>
          <div v-if="isFollowing !== null">
            <!-- 팔로우 버튼 -->
            <div @click="followToggle(route.params.id)" v-if="isFollowing">
              <p>팔로우 취소</p>
            </div>
            <div @click="followToggle(route.params.id)" v-else>
              <p>팔로우</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 영화 플레이리스트 -->
    <div class="playlist-section" data-aos="fade-up" data-aos-delay="150">
      <h2>{{ currentUserInfo?.nickname || '사용자' }}님의 영화 플레이리스트</h2>
      <div class="content-box">
        <div v-if="currentUserInfo.playlists">
          <div class="playlist-box">
            <div v-for="playlist in currentUserInfo.playlists.slice(0, 4)" :key="playlist.id">
              <div @click="seePlaylistDetail(route.params.id, playlist.id)">
                <ListThumbnail :movies="playlist.movies" />
                <h3>{{ playlist.title }}</h3>
                <p>{{ playlist.description }}</p>
              </div>
            </div>
          </div>
          <p @click="seeAllPlaylist(route.params.id)">더보기</p>
        </div>
        <p v-else>플레이리스트가 비어 있습니다.</p>
      </div>
    </div>

    <!-- 좋아하는 영화 -->
    <div class="movie-section" data-aos="fade-up" data-aos-delay="150">
      <h2>{{ currentUserInfo?.nickname || '사용자' }}님이 좋아한 영화</h2>
      <div class="content-box">
        <div v-if="currentUserInfo.liked_movies">
          <div class="movie-box">
            <div v-for="movie in currentUserInfo.liked_movies.slice(0, 4)" :key="movie.movie_id">
              <img @click="seeMovieDetail(movie.movie_id)" :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`" alt="영화 포스터">
            </div>
          </div>
          <p @click="seeAllMovies(route.params.id)">더보기</p>
        </div>
        <p v-else>좋아하는 영화가 없습니다.</p>
      </div>
    </div>

    <!-- 좋아하는 감독 -->
    <div class="director-section" data-aos="fade-up" data-aos-delay="150">
      <h2>{{ currentUserInfo?.nickname || '사용자' }}님이 좋아한 감독</h2>
      <div class="content-box">
        <div v-if="currentUserInfo.liked_directors">
          <div class="director-box">
            <div v-for="director in currentUserInfo.liked_directors.slice(0, 4)" :key="director.director_id">
              <div @click="seeDirecDetail(director.director_id)">
                <img :src="`https://image.tmdb.org/t/p/w200/${director.profile_path}`" alt="감독 프로필">
                <h3>{{ director.name }}</h3>
              </div>
            </div>
          </div>
          <p @click="seeAllDirectors(route.params.id)">더보기</p>
        </div>
        <p v-else>좋아하는 감독이 없습니다.</p>
      </div>
    </div>

    <!-- 좋아하는 배우 -->
    <div class="actor-section" data-aos="fade-up" data-aos-delay="150">
      <h2>{{ currentUserInfo?.nickname || '사용자' }}님이 좋아한 배우</h2>
      <div class="content-box">
        <div v-if="currentUserInfo.liked_actors">
          <div class="actor-box">
            <div v-for="actor in currentUserInfo.liked_actors.slice(0, 4)" :key="actor.actor_id">
              <img @click="seeActorDetail(actor.actor_id)" :src="`https://image.tmdb.org/t/p/w200/${actor.profile_path}`" alt="배우 프로필">
              <h3>{{ actor.name }}</h3>
            </div>
          </div>
          <p @click="seeAllActors(route.params.id)">더보기</p>
        </div>
        <p v-else>좋아하는 배우가 없습니다.</p>
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

const accountStore = useAccountStore()
const route = useRoute()
const router = useRouter()
const defaultProfileImage = '/media/profile_images/default_profile.jpg'
const profileImage = ref(null)

// 닉네임 수정 상태
const isEditingNickname = ref(false)
const nickname = ref('')

// 현재 사용자가 자신의 프로필 페이지를 보고 있는지 확인
const isOwnProfile = computed(() => Number(route.params.id) === accountStore.userId)

// 현재 렌더링해야 할 사용자 데이터
const currentUserInfo = computed(() => {
  return isOwnProfile.value ? accountStore.loggedInUserInfo : accountStore.userInfo
})

// 컴포넌트 로드 시 데이터 가져오기
const loadUserInfo = async () => {
  if (isOwnProfile.value) {
    // 로그인한 사용자의 프로필 로드
    if (!accountStore.loggedInUserInfo) {
      await accountStore.getLoggedInUserInfo()
    }
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
  await loadUserInfo()
  console.log(isOwnProfile.value)
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
          Authorization: `Token ${accountStore.token}`
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
          Authorization: `Token ${accountStore.token}`
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
const seeDirecDetail = (director_id) => router.push({ name: 'DirecDetailView', params: { director_id } })
const seeAllActors = (user_id) => router.push({ name: 'MyActorView', params: { id: user_id } })
const seeActorDetail = (actor_id) => router.push({ name: 'ActorDetailView', params: { actor_id } })
</script>


<style scoped>
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

.profile-info h1 {
  font-size: 36px;
  margin-bottom: 10px;
}

.nickname {
  font-size: 24px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.nickname .edit-icon {
  font-size: 18px;
  cursor: pointer;
  color: #aaaaaa;
  transition: color 0.3s;
}

.nickname .edit-icon:hover {
  color: white;
}

.follow-info {
  margin-top: 10px;
  display: flex;
  gap: 20px;
  font-size: 18px;
}

.playlist-box, .movie-box, .director-box, .actor-box {
  display: flex;
}
</style>
