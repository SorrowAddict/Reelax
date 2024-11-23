<template>
  <div class="genre-selection">
    <h1>선호 장르를 선택해주세요</h1>
    <ul class="genre-list">
      <li 
        v-for="genre in genres" 
        :key="genre.genre_id" 
        :class="{ selected: selectedGenres.some(g => g.genre_id === genre.genre_id) }"
        @click="toggleGenre(genre)"
        data-aos="fade-up"
      >
        {{ genre.name }}
      </li>
    </ul>
    <button @click="saveGenres" class="btn-save">저장하기</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { useAccountStore } from "@/stores/account"
import { useRouter } from "vue-router"
import AOS from 'aos'
import 'aos/dist/aos.css'

onMounted(() => {
  AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: false,
  })
})

const store = useAccountStore()
const router = useRouter()

const BASE_URL = store.BASE_URL
const genres = ref([]) // 모든 장르
const selectedGenres = ref([]) // 사용자가 좋아요한 장르

// 모든 장르 목록 가져오기
const fetchGenres = async () => {
  try {
    const res = await axios.get(`${BASE_URL}/movies/genres/`) // 장르 리스트 API 호출
    genres.value = res.data
  } catch (err) {
    console.error(err)
  }
}

// 사용자가 좋아요한 장르 가져오기
const fetchLikedGenres = async () => {
  try {
    const res = await axios.get(`${BASE_URL}/movies/like-genre/`, {
      headers: {
        Authorization: `Token ${store.token}`,
      },
    })
    selectedGenres.value = res.data // 초기 좋아요 데이터 설정
  } catch (err) {
    console.error(err)
  }
}

// 장르 선택/해제 토글
const toggleGenre = (genre) => {
  const index = selectedGenres.value.findIndex((g) => g.genre_id === genre.genre_id)
  if (index === -1) {
    selectedGenres.value.push({ genre_id: genre.genre_id, name: genre.name }) // 선택
  } else {
    selectedGenres.value.splice(index, 1) // 해제
  }
}

// 선택된 장르 저장
const saveGenres = async () => {
  try {
    await axios.post(
      `${BASE_URL}/movies/like-genre/`, // 요청 URL
      { genres: selectedGenres.value }, // 전송 데이터
      {
        headers: {
          Authorization: `Token ${store.token}`, // 인증 토큰
        },
      }
    )
    console.log("선호 장르가 저장되었습니다.")
    router.push({ name: "MainPageView" }) // 저장 후 메인 페이지로 이동
  } catch (err) {
    console.error(err)
  }
}


// 컴포넌트 초기화 시 실행
fetchGenres()
fetchLikedGenres()
</script>

<style scoped>
.genre-selection {
  text-align: center;
  padding: 20px;
}

.genre-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  list-style: none;
  padding: 0;
}

.genre-list li {
  margin: 10px;
  padding: 10px 20px;
  background: #252525;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.genre-list li.selected {
  background: #007bff;
}

.btn-save {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 1rem;
  color: white;
  background: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
