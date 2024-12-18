<template>
  <div v-for="person in people" :key="person.id">
    <div class="person">
      {{ person.director_id }}
      <img :src="getImageUrl(person.profile_path)" alt="프로필 이미지" @click="direcDetail(person.id)">
      <p>{{ person.name }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useLikeStore } from '@/stores/like'
import { useAccountStore } from '@/stores/account'

const props = defineProps({
  people: Object,
  userInfo: Object
})
const router = useRouter()
const likeStore = useLikeStore()
const accountStore = useAccountStore()

const defaultImage = "/image/basic_profile.png"
const baseImageUrl = "https://image.tmdb.org/t/p/w200"

const getImageUrl = (profilePath) => {
  return profilePath ? `${baseImageUrl}${profilePath}` : defaultImage;
};

const liked_directors = computed(() => props.userInfo.liked_directors)

const isDirectorLiked = function (director) {
  return liked_directors.value.some((liked_director) => liked_director.director_id === director.id)
}

const direcDetail = function (id) {
  router.push({ name: 'DirecDetailView', params: { direc_id: id }})
}

const direcLike = function (director_id, name, profile_path) {
  const payload = {
    director_id: director_id,
    name: name,
    profile_path: profile_path
  }
  likeStore.direcLike(payload)
}
</script>

<style scoped>
div {
  display: inline-block;
  margin: 10px;
  text-align: center;
}

p {
  margin-top: 10px;
}

.person {
  text-align: center;
  background-color: #2b2b2e;
  padding: 10px;
  border-radius: 10px;
  transition: transform 0.3s, box-shadow 0.3s;
  color: #f4f4f4;
  cursor: pointer;
}

.person:hover {
  transform: translateY(-5px);
  box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.3);
}

img {
  max-width: 200px;
  max-height: 300px;
  border-radius: 10px;
  object-fit: cover;
  cursor: pointer;
}
</style>