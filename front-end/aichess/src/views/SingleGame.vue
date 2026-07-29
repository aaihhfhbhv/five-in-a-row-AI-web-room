<template>
  <div class="single-page">
    <h2>人机AI对局</h2>
    <div style="margin-bottom:12px;">
      <label>棋盘尺寸: </label>
      <label style="margin-left:8px">
        <input type="radio" name="size" value="8" v-model="size" /> 8x8
      </label>
      <label style="margin-left:8px">
        <input type="radio" name="size" value="15" v-model="size" /> 15x15
      </label>
    </div>
    <div class="board-stage">
      <BoardComponent :key="size" :board-height="Number(size)" :board-width="Number(size)" />
      <LiveGirlComponent placement="board" :bottom-offset="Number(size) <= 8 ? 24 : 0" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import BoardComponent from '@/components/BoardComponent.vue'
import LiveGirlComponent from '@/components/LiveGirlComponent.vue'

const size = ref('8')
</script>

<style scoped>
.single-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}
.board-stage {
  position: relative;
  display: inline-block;
}
h2 {
  margin: 0;
}
</style>
