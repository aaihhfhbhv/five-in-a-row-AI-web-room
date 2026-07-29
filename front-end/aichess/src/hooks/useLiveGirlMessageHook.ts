import { ref } from 'vue'

type LiveGirlAction = 'idle' | 'cheer' | 'jump'

const liveGirlMessage = ref('')
const liveGirlMessageTime = ref(0)
const liveGirlAction = ref<LiveGirlAction>('idle')

const setNewLiveGirlMessage = (message: string, time = 3000) => {
  liveGirlMessage.value = message
  liveGirlMessageTime.value = time
}

const setLiveGirlAction = (action: LiveGirlAction = 'idle', time = 1200) => {
  liveGirlAction.value = action
  if (time > 0) {
    window.setTimeout(() => {
      liveGirlAction.value = 'idle'
    }, time)
  }
}

export {
  liveGirlMessage,
  liveGirlMessageTime,
  liveGirlAction,
  setNewLiveGirlMessage,
  setLiveGirlAction
}
