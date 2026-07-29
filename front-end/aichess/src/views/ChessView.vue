<script lang="ts" setup>
import BoardComponent from '../components/BoardComponent.vue'
import LiveGirlComponent from '../components/LiveGirlComponent.vue'
</script>

<template>
  <div class="chess-view">
    <BoardComponent :board-width="8" :board-height="8" />
    <LiveGirlComponent />
  </div>
</template>

<style scoped>
.chess-view {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f3f3f3;
  overflow: visible;
}
</style>
