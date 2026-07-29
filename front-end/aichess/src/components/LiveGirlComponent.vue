<script lang="ts" setup>
import { computed, onMounted, onUnmounted, ref, nextTick, withDefaults, defineProps } from 'vue'
import { liveGirlAction, liveGirlMessage, liveGirlMessageTime, setNewLiveGirlMessage } from '@/hooks/useLiveGirlMessageHook'

interface Props {
  placement?: 'page' | 'board'
  bottomOffset?: number
  rightOffset?: number
}

const props = withDefaults(defineProps<Props>(), {
  placement: 'page',
  bottomOffset: 5,
  rightOffset: 30
})

// 扩展Window全局类型，声明loadlive2d函数，替代any
declare global {
  interface Window {
    loadlive2d: (canvasId: string, modelPath: string) => void
  }
}

let intervalTimer: number | null = null

onMounted(async () => {
  await nextTick()
  setTimeout(() => {
    const canvasDom = document.getElementById('live2d')
    if (!canvasDom) {
      return
    }
    if (!window.loadlive2d) {
      return
    }
    window.loadlive2d('live2d', '/live2d/model/tia/model.json')
  }, 500)
})

const messageHidden = computed(() => liveGirlMessageTime.value === 0)
const timeHidden = ref(0)
const hiddenWrapper = computed(() => timeHidden.value !== 0)
const wrapperClass = computed(() => {
  const classes = ['wrapper', props.placement === 'board' ? 'wrapper--board' : 'wrapper--page']
  if (liveGirlAction.value === 'jump') {
    classes.push('is-jumping')
  } else if (liveGirlAction.value === 'cheer') {
    classes.push('is-cheering')
  }
  return classes.join(' ')
})
const wrapperStyle = computed(() => props.placement === 'board'
  ? { left: '100%', marginLeft: `${props.rightOffset + 24}px`, bottom: `${props.bottomOffset}px`, opacity: hiddenWrapper.value ? 0.3 : 1, pointerEvents: 'auto' }
  : { right: '30px', bottom: '5px', opacity: hiddenWrapper.value ? 0.3 : 1, pointerEvents: 'auto' })

intervalTimer = window.setInterval(() => {
  timeHidden.value = timeHidden.value > 200 ? timeHidden.value - 200 : 0
  liveGirlMessageTime.value = liveGirlMessageTime.value > 200 ? liveGirlMessageTime.value - 200 : 0
}, 200)

onUnmounted(() => intervalTimer && clearInterval(intervalTimer))
const mouseOver = () => setNewLiveGirlMessage('你碰不到我(●ˇ∀ˇ●)', 1000)
</script>

<template>
<div :class="wrapperClass" @mouseover="mouseOver" :style="wrapperStyle">
  <div class="message" v-show="!messageHidden">{{ liveGirlMessage }}</div>
  <canvas id="live2d" width="280" height="250"></canvas>
</div>
</template>
<style scoped>
.wrapper {
  display: inline-block;
  position: absolute;
  z-index: 999;
  transform-origin: center bottom;
}
.wrapper--page {
  position: fixed;
  right: 30px;
  bottom: 5px;
}
.wrapper--board {
  position: absolute;
  left: 100%;
  right: auto;
  bottom: 0;
  transform: none;
  margin-left: 16px;
  display: flex;
  align-items: flex-end;
}
.wrapper.is-jumping {
  animation: jump-celebrate 0.8s ease-in-out 1;
}
.wrapper.is-cheering {
  animation: cheer-celebrate 0.9s ease-out 1;
}
.message {
  position: absolute;
  top: -6px;
  left: 50%;
  transform: translateX(-50%);
  padding: 8px 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.94);
  color: #2c3e50;
  font-size: 13px;
  white-space: nowrap;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.12);
}
@keyframes jump-celebrate {
  0% { transform: translateY(0) scale(1); }
  40% { transform: translateY(-18px) scale(1.04); }
  100% { transform: translateY(0) scale(1); }
}
@keyframes cheer-celebrate {
  0% { transform: scale(1) rotate(0deg); }
  30% { transform: scale(1.06) rotate(-3deg); }
  60% { transform: scale(1.02) rotate(3deg); }
  100% { transform: scale(1) rotate(0deg); }
}
</style>
