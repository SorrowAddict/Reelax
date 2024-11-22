<template>
  <div>
    <h3>배우</h3>
    <ActorCreditCard
      :people="actors"
      :userInfo="userInfo"
    />
  </div>
</template>

<script setup>
import ActorCreditCard from './ActorCreditCard.vue'

const props = defineProps({
  actors: Object,
  userInfo: Object
})
</script>

<style scoped>

</style>