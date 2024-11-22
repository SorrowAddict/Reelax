<template>
  <div v-for="person in topPeople" :key="person.id">
    <div @click="actorDetail(person.id)">
      <img :src="getImageUrl(person.profile_path)" alt="프로필 이미지">
      <p>{{ person.name }}</p>
    </div>
    <div @click="actorLike(person.id, person.name, person.profile_path)">
      <div v-if="isActorLiked(person)">
        <font-awesome-icon :icon="['fas', 'heart']" />
      </div>
      <div v-else>
        <font-awesome-icon :icon="['far', 'heart']" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useLikeStore } from '@/stores/like';
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const likeStore = useLikeStore()

const props = defineProps({
  people: Object,
  userInfo: Object
})

console.log(props.people, props.userInfo)

const defaultImage = "/image/basic_profile.png"
const baseImageUrl = "https://image.tmdb.org/t/p/w200"

const getImageUrl = (profilePath) => {
  return profilePath ? `${baseImageUrl}${profilePath}` : defaultImage;
};

const topPeople = computed(() => props.people.slice(0, 10))

const liked_actors = computed(() => props.userInfo.liked_actors)

const isActorLiked = function (actor) {
  return liked_actors.value.some((liked_actor) => liked_actor.actor_id === actor.id)
}

const actorDetail = function (id) {
  router.push({ name: 'ActorDetailView', params: { actor_id: id }})
}

const actorLike = function (actor_id, name, profile_path) {
  const payload = {
    actor_id: actor_id,
    name: name,
    profile_path: profile_path
  }
  likeStore.actorLike(payload)
}
</script>

<style scoped>

</style>