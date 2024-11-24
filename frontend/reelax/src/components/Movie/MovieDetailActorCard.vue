<template>
  <div class="actor-credit-card">
    <h3>배우</h3>
    <div class="actor-grid">
      <ActorCreditCard
        v-for="(actor, index) in actors"
        :key="index"
        :people="actor"
        :userInfo="userInfo"
      />
    </div>
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
.actor-credit-card {
  padding: 20px;
  color: #f4f4f4;
}

.actor-credit-card h3 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  text-transform: uppercsase;
  letter-spacing: 1.2px;
}

.actor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>