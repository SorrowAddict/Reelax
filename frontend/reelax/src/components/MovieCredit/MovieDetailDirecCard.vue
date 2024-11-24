<template>
  <div>
    <h3>감독</h3>
    <DirectorCreditCard
      :people="director"
      :userInfo="userInfo"
    />
  </div>
</template>

<script setup>
import DirectorCreditCard from './DirectorCreditCard.vue';

const props = defineProps({
  director: Object,
  userInfo: Object
})


</script>

<style scoped>

</style>