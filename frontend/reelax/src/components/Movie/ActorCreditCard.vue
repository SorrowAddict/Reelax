<template>
  <div>
    <div @click="actorDetail(people.id)">
      <img :src="getImageUrl(people.profile_path)" alt="프로필 이미지">
      <p>{{ people.name }}</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  people: Object,
  userInfo: Object
})

const router = useRouter()

const defaultImage = "/image/basic_profile.png"
const baseImageUrl = "https://image.tmdb.org/t/p/w200"

const getImageUrl = (profilePath) => {
  return profilePath ? `${baseImageUrl}${profilePath}` : defaultImage
}

const actorDetail = function (id) {
  router.push({ name: 'ActorDetailView', params: { actor_id: id } })
}
</script>

<style scoped>
div {
  text-align: center;
  background-color: #2b2b2e;
  padding: 10px;
  border-radius: 10px;
  transition: transform 0.3s, box-shadow 0.3s;
  color: #f4f4f4;
  cursor: pointer;
}

div:hover {
  transform: translateY(-5px);
  box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.3);
}

img {
  width: 100%;
  height: auto;
  max-width: 120px;
  border-radius: 35%;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}

p {
  margin-top: 10px;
  text-transform: capitalize;
}
</style>
