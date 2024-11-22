<template>
  <div class="container">
    <!-- 캐러셀 영역 -->
    <div class="carousel-wrapper">
      <div id="carouselExample" class="carousel slide" data-bs-ride="carousel" data-bs-interval="4000">
        <div class="carousel-inner">
          <div
            v-for="(image, index) in carouselImages"
            :key="index"
            :class="['carousel-item', { active: index === 0 }]"
          >
            <img :src="image" class="d-block w-100" alt="영화 이미지" />
          </div>
        </div>
        <!-- 캐러셀 이전/다음 버튼 -->
        <button
          class="carousel-control-prev"
          type="button"
          data-bs-target="#carouselExample"
          data-bs-slide="prev"
        >
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button
          class="carousel-control-next"
          type="button"
          data-bs-target="#carouselExample"
          data-bs-slide="next"
        >
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </div>

    <!-- 로그인 한 상태일 때만 보여지는 영화 리스트들 -->
    <div v-if="accountStore.token !== null">
      <!-- 사용자가 좋아한 장르의 영화 -->
      <div v-if="movieStore.userLikedGenreMovies && Object.keys(movieStore.userLikedGenreMovies).length > 0" class="movie">
        <div v-for="(movies, genre) in movieStore.userLikedGenreMovies" :key="genre">
          <h3>사용자가 좋아한 {{ genre }} 영화</h3>
          <MainCarouselSection
            carousel-id="likedGenreCarousel"
            :movies="movies"
          />
        </div>
      </div>
      <div v-else class="movie">
        <h1>아직 좋아한 장르가 없습니다!</h1>
      </div>

      <!-- 사용자가 좋아한 최근 영화 -->
      <div v-if="movieStore.userLikedMovies && Object.keys(movieStore.userLikedMovies).length > 0" class="movie">
        <h3>사용자가 최근 좋아한 영화</h3>
        <MainCarouselSection
          carousel-id="likedMovieCarousel"
          :movies="movieStore.userLikedMovies"
        />
      </div>
      <div v-else class="movie">
        <h1>아직 좋아한 영화가 없습니다!</h1>
      </div>

      <!-- 유저가 좋아한 배우 중 랜덤으로 하나 뽑아서 필모 5개 표시 -->
      <div v-if="movieStore.userLikedActorMovies && Object.keys(movieStore.userLikedActorMovies).length > 0" class="movie">
        <h3>사용자가 좋아한 배우 {{ movieStore.userLikedActor }}의 영화</h3>
        <MainCarouselSection
          carousel-id="likedActorCarousel"
          :movies="movieStore.userLikedActorMovies"
        />
      </div>
      <div v-else class="movie">
        <h1>아직 좋아한 배우가 없습니다!</h1>
      </div>

      <!-- 유저가 좋아한 감독 중 랜덤으로 하나 뽑아서 필모 5개 표시 -->
      <div v-if="movieStore.userLikedDirecMovies && Object.keys(movieStore.userLikedDirecMovies).length > 0" class="movie">
        <h3>사용자가 좋아한 감독 {{ movieStore.userLikedDirec }}의 영화</h3>
        <MainCarouselSection
          carousel-id="likedDirecCarousel"
          :movies="movieStore.userLikedDirecMovies"
        />
      </div>
      <div v-else class="movie">
        <h1>아직 좋아한 감독이 없습니다!</h1>
      </div>
    </div>
    
    <!-- Top rated movie -->
    <div v-if="movieStore.topRatedMovies" class="movie">
      <h3>좋은 평가를 받은 영화 TOP 10</h3>
      <MainCarouselSection
        carousel-id="topRatedCarousel"
        :movies="movieStore.topRatedMovies"
      />
    </div>

    <div v-if="movieStore.boxOfficeMovies" class="movie">
      <h3>박스 오피스 TOP 10</h3>
      <MainCarouselSection
        carousel-id="boxOfficeCarousel"
        :movies="movieStore.boxOfficeMovies"
      />
    </div>

    <div v-if="movieStore.recentlyReleasedMovies" class="movie">
      <h3>최근 개봉한 영화</h3>
      <MainCarouselSection
        carousel-id="recentlyReleasedCarousel"
        :movies="movieStore.recentlyReleasedMovies"
      />
    </div>

    <div v-if="accountStore.token !== null && movieStore.genreMovies">
      <!-- 로그인 되어있는 상태 -->
      <div v-for="(movies, genre) in movieStore.genreMovies" :key="genre" class="movie">
        <h3>이런 영화는 어떠세요?</h3>
        <MainCarouselSection
          carousel-id="genreCarousel"
          :movies="movies"
        />
      </div>
    </div>
    <div v-else-if="accountStore.token === null && movieStore.genreMovies">
      <!-- 로그인 되어있지 않은 상태 -->
      <div v-for="(movies, genre) in movieStore.genreMovies" :key="genre" class="movie">
        <h3>당신이 좋아할만한 {{ genre }} 영화</h3>
        <MainCarouselSection
          carousel-id="genreCarousel"
          :movies="movies"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import MainCarouselSection from "@/components/Movie/MainCarouselSection.vue"
import { useAccountStore } from "@/stores/account"
import { useMovieStore } from '@/stores/movie'
import { onMounted, ref } from 'vue'

const movieStore = useMovieStore()
const accountStore = useAccountStore()

const carouselImages = ref([
  '/image/1.jpg',
  '/image/1.jpg',
  '/image/1.jpg',
  '/image/1.jpg',
])

onMounted(() => {
  movieStore.getTopRatedMovies()
  movieStore.getBoxOfficeMovies()
  movieStore.getRecentlyReleasedMovies()
  movieStore.getGenreMovies()
  if (accountStore.isLogin) {
    // 로그인 되어있을 경우
    movieStore.getUserLikedGenreMovies()
    movieStore.getUserLikedMovies()
    movieStore.getUserLikedActorMovies()
    movieStore.getUserLikedDirecMovies()
  }
  
})
</script>

<style scoped>
.carousel-inner img {
  width: auto; /* 이미지 너비를 자동으로 설정 */
  height: auto; /* 이미지 높이를 자동으로 설정 */
  max-width: 100%; /* 이미지가 캐러셀 너비를 넘지 않도록 제한 */
  margin: 0 auto; /* 이미지를 중앙 정렬 */
  display: block; /* 블록 요소로 설정 */
  border-radius: 15px;
}

.carousel {
  margin: 0; /* 좌우 여백 제거 */
  width: 100%; /* 화면 전체 너비 */
}

.carousel-wrapper {
  margin-left: -15px;
  margin-right: -15px;
  width: calc(100% + 30px); /* 여백만큼 확장 */
}

.carousel-control-prev,
.carousel-control-next {
  width: auto; /* 버튼 크기를 조정할 수 있도록 */
  transform: translateX(-30px); /* 이전 버튼을 왼쪽으로 이동 */
}

.carousel-control-next {
  transform: translateX(30px); /* 다음 버튼을 오른쪽으로 이동 */
}

.movie {
  margin: 100px 0px;
}

.movie-list {
  margin: 20px 0px;
}

.genre-movie {
  margin: 100px 0px;
}
</style>