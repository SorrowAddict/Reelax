<template>
  <div class="genre-selection container">
    <h3 class="text-center mb-4 display-5" data-aos="fade-up">선호 장르를 선택해주세요</h3>
    <div class="row g-3">
      <div
        v-for="genre in genres"
        :key="genre.genre_id"
        class="col-6 col-sm-4 col-md-3"
        data-aos="zoom-in"
        data-aos-delay="250"
      >
        <div
          class="genre-item text-center p-3"
          :class="{ selected: selectedGenres.some((g) => g.genre_id === genre.genre_id) }"
          @click="toggleGenre(genre)"
        >
          {{ genre.name }}
        </div>
      </div>
    </div>
    <div class="text-center mt-4">
      <button @click="saveGenres" class="btn btn-primary btn-lg" data-aos="fade-down" data-aos-delay="0">
        저장하기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useAccountStore } from "@/stores/account";
import { useRouter } from "vue-router";
import AOS from "aos";
import "aos/dist/aos.css";

const store = useAccountStore();
const router = useRouter();

onMounted(async () => {
  AOS.init({
    duration: 400,
    easing: "ease-in-out",
    once: false,
  })
  await store.getUserId()
  await store.getLoggedInUserInfo()
});

const BASE_URL = store.BASE_URL;
const genres = ref([]); // 모든 장르
const selectedGenres = ref([]); // 사용자가 좋아요한 장르

const fetchGenres = async () => {
  try {
    const res = await axios.get(`${BASE_URL}/movies/genres/`); // 장르 리스트 API 호출
    genres.value = res.data;
  } catch (err) {
    console.error(err);
  }
};

const fetchLikedGenres = async () => {
  try {
    const res = await axios.get(`${BASE_URL}/movies/like-genre/`, {
      headers: {
        Authorization: `Bearer ${store.token}`,
      },
    });
    selectedGenres.value = res.data; // 초기 좋아요 데이터 설정
  } catch (err) {
    console.error(err);
  }
};

const toggleGenre = (genre) => {
  const index = selectedGenres.value.findIndex(
    (g) => g.genre_id === genre.genre_id
  );
  if (index === -1) {
    selectedGenres.value.push({ genre_id: genre.genre_id, name: genre.name }); // 선택
  } else {
    selectedGenres.value.splice(index, 1); // 해제
  }
};

const saveGenres = async () => {
  try {
    await axios.post(
      `${BASE_URL}/movies/like-genre/`, // 요청 URL
      { genres: selectedGenres.value }, // 전송 데이터
      {
        headers: {
          Authorization: `Bearer ${store.token}`, // 인증 토큰
        },
      }
    );
    console.log("선호 장르가 저장되었습니다.");
    router.push({ name: "MainPageView" }); // 저장 후 메인 페이지로 이동
  } catch (err) {
    console.error(err);
  }
};

fetchGenres();
fetchLikedGenres();
</script>

<style scoped>
.genre-selection {
  text-align: center;
  padding: 20px;
}

.genre-item {
  background: #252525;
  color: white;
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
  cursor: pointer;
  user-select: none;
}

.genre-item:hover {
  transform: scale(1.05);
  background: #007bff;
  color: white;
}

.genre-item.selected {
  background: #007bff;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 123, 255, 0.5);
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

@media (min-width: 768px) {
  .genre-selection {
    padding: 40px;
  }

  .genre-item {
    padding: 20px;
  }

  .btn-primary {
    padding: 15px 30px;
    font-size: 1.2rem;
  }
}
</style>
