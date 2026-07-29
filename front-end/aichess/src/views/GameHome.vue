<template>
  <div class="page-wrap">
    <h1 class="main-title">五子棋对战平台</h1>
    <div class="mode-select-bar">
      <button class="mode-btn" @click="$router.push('/single-game')">人机对决（AI）</button>
      <button class="mode-btn" @click="$router.push('/online-room')">联机对决</button>
    </div>
  </div>
</template>

<script lang="ts" setup>
</script>

<style scoped>
.page-wrap {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* 取消垂直居中，整体向上偏移 */
  justify-content: flex-start;
  padding-top: 80px;
  box-sizing: border-box;
}
.main-title {
  margin: 0 0 24px;
  font-size: 36px;
}
.mode-select-bar {
  display: flex;
  gap: 18px;
}
.mode-btn {
  padding: 12px 26px;
  font-size: 18px;
  cursor: pointer;
  border-radius: 6px;
  border: none;
  background: #409eff;
  color: #fff;
  transition: background 0.2s;
}
.mode-btn:hover {
  background:#3385d6;
}
</style>
