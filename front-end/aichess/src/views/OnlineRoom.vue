<template>
  <div class="room-page-wrap">
    <h2>联机大厅</h2>
    <div v-if="showMatchTip" class="match-tip">匹配成功，2秒后进入对局</div>
    <div class="operate-block" v-show="!showMatchTip">
      <section class="create-part">
        <h3>创建新房间</h3>
          <div style="display:flex;gap:8px;">
            <button @click="handleCreateRoom">生成 8x8 房间</button>
            <button @click="handleCreate15">生成 15x15 房间</button>
          </div>
        <template v-if="roomId">
          <p>房间编号：<span class="room-code">{{ roomId }}</span></p>
          <div class="tip-wrap">
            <p class="wait-tip">✅ 你已占据玩家1席位，正在等待第二名玩家加入对局</p>
          </div>
        </template>
      </section>
      <section class="join-part">
        <h3>加入已有房间</h3>
        <input v-model="inputRoomId" placeholder="填写房间号">
        <button @click="handleJoinRoom">进入房间</button>
      </section>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import useChessRequest from '@/hooks/useChessRequestHook'
import { getClientId } from '@/utils/clientId'
const router = useRouter()
const clientId = getClientId()
const { createRoom, createRoomWithSize, joinRoom, getRoomState } = useChessRequest([], 'Player2')
const roomId = ref('')
const inputRoomId = ref('')
const showMatchTip = ref(false)
const WAIT_MS = 2000
let pollTimer: number | null = null

const handleCreateRoom = async () => {
  // 默认创建 8x8 房间，并立即进入对局页，等待对手加入
  const res = await createRoom(clientId.value)
  roomId.value = res.roomId
  router.push({ path: '/online-board', query: { roomId: roomId.value } })
}

const handleCreate15 = async () => {
  // 创建 15x15 房间并立即进入对局页
  const res = await createRoomWithSize(clientId.value, 15, 15)
  roomId.value = res.roomId
  router.push({ path: '/online-board', query: { roomId: roomId.value } })
}

const handleJoinRoom = async () => {
  if (!inputRoomId.value) return
  await joinRoom(inputRoomId.value, clientId.value)
  roomId.value = inputRoomId.value
  // 立即进入对局页
  router.push({ path: '/online-board', query: { roomId: roomId.value } })
}

const startPollMatch = () => {
  pollTimer = window.setInterval(async () => {
    try {
      const res = await getRoomState(roomId.value)
      if (res.matchReady === true) {
        if (pollTimer) clearInterval(pollTimer)
        showMatchTip.value = true
        setTimeout(() => {
          router.push({ path: '/online-board', query: { roomId: roomId.value } })
        }, WAIT_MS)
      }
    } catch (e) {
      // 房间轮询失败时保持静默，避免影响交互体验
    }
  }, 500)
}

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<style scoped>
.room-page-wrap {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 36px;
}
.operate-block {
  display: flex;
  gap: 48px;
}
.create-part,.join-part {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}
.tip-wrap {
  width: 100%;
}
.room-code {
  font-size: 24px;
  font-weight: bold;
  letter-spacing: 3px;
  color: #c83c3c;
}
.wait-tip {
  color: #27ae60;
  font-size: 16px;
  text-align: center;
  margin: 0;
}
.match-tip {
  font-size: 26px;
  color:#27ae60;
  font-weight:bold;
}
input {
  padding: 10px 12px;
  width: 240px;
  font-size: 15px;
  border-radius: 6px;
  border: #ddd solid 1px;
}
button {
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 6px;
  border: 0;
  background: #409eff;
  color:#fff;
  transition: background 0.2s;
}
button:hover {
  background:#3385d6;
}
</style>
