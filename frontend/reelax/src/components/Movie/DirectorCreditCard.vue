<template>
  <div v-for="person in people" :key="person.id">
    <div @click="direcDetail(person.id)">
      {{ person.director_id }}
      <img :src="getImageUrl(person.profile_path)" alt="프로필 이미지">
      <p>{{ person.name }}</p>
    </div>
    <div v-if="accountStore.isLogin">
      <div @click="direcLike(person.id, person.name, person.profile_path)">
        <div v-if="isDirectorLiked(person)">
          <font-awesome-icon :icon="['fas', 'heart']" />
        </div>
        <div v-else>
          <font-awesome-icon :icon="['far', 'heart']" />
        </div>
      </div>
    </div>
    <div v-else>
      <font-awesome-icon :icon="['far', 'heart']" />
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

</style>