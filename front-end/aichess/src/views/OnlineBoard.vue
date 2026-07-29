<template>
  <div class="online-board-wrap">
    <h3>联机对局 | 房间号：{{ roomId }}</h3>
    <p class="self-color">我方棋子：{{ selfChessColor }}</p>
    <p class="tip">{{ tipText }}</p>
    <div class="action-row">
      <button class="surrender-btn" @click="handleSurrender" :disabled="controlsDisabled">认输/退出</button>
      <button class="undo-btn" @click="handleUndoRequest" :disabled="controlsDisabled || !canRequestUndo">请求悔棋</button>
      <button class="auto-btn" @click="handleToggleAutoPlay" :disabled="controlsDisabled || myPlayerNumber === 0">
        {{ autoPlayEnabled ? '取消托管' : '开启托管' }}
      </button>
    </div>
    <div class="board-area">
      <BoardComponent
        :is-online="true"
        :board="board"
        :player1-color="p1Color"
        :player2-color="p2Color"
        :board-height="roomHeight"
        :board-width="roomWidth"
        :last-move="lastMove"
        @click-cell="handleClickCell"
      />
      <LiveGirlComponent placement="board" :bottom-offset="liveGirlBottomOffset" />
      <div v-if="showEndMask" class="game-end-mask">
        <div class="mask-content">{{ tipText }}</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BoardComponent from '@/components/BoardComponent.vue'
import LiveGirlComponent from '@/components/LiveGirlComponent.vue'
import useChessRequest from '@/hooks/useChessRequestHook'
import useChessBoard from '@/hooks/useChessBoardHook'
import { setLiveGirlAction, setNewLiveGirlMessage } from '@/hooks/useLiveGirlMessageHook'
import { getClientId } from '@/utils/clientId'

const route = useRoute()
const router = useRouter()
const roomId = ref(route.query.roomId as string)
const clientId = getClientId()
const tipText = ref('等待同步棋盘...')
const p1ClientId = ref('')
const p2ClientId = ref('')
const p1Color = ref(1)
const p2Color = ref(2)
const lastMove = ref(-1)

let board: any
let changeChessState: any
const roomWidth = ref(8)
const roomHeight = ref(8)
const { getRoomState, roomMove, surrenderRoom, undoRequest, undoReply, toggleAutoPlay } = useChessRequest([], 'Player2')

let pollTimer: number | null = null
let autoPlayTimer: number | null = null // AI延时落子定时器
const currentPlayerNum = ref(1)
const gameOver = ref(false)
const pendingUndoRequester = ref('')
const redirectPending = ref(false)
const autoPlayEnabled = ref(false)
const isAutoCalculating = ref(false) // 前端防重复请求锁

const ownMoveCount = computed(() => {
  if (!board) return 0
  const myNumber = myPlayerNumber.value
  if (myNumber === 0) return 0
  let count = 0
  for (let i = 0; i < board.length; i++) {
    for (let j = 0; j < board[0].length; j++) {
      const val = board[i][j]
      if ((myNumber === 1 && val === 'Player1') || (myNumber === 2 && val === 'Player2')) {
        count++
      }
    }
  }
  return count
})

const canRequestUndo = computed(() => {
  return !gameOver.value && !pendingUndoRequester.value && myPlayerNumber.value !== 0 && ownMoveCount.value > 0
})

onMounted(() => {
  gameOver.value = false
  currentPlayerNum.value = 1
  if (roomId.value) {
    pollRoomState()
    pollTimer = window.setInterval(pollRoomState, 2000)
  }
})

const myPlayerNumber = computed(() => {
  const localId = clientId.value.trim()
  const p1 = p1ClientId.value.trim()
  const p2 = p2ClientId.value.trim()
  if (!localId) return 0
  if (localId === p1) return 1
  if (localId === p2) return 2
  return 0
})

const selfChessColor = computed(() => {
  if (myPlayerNumber.value === 0) return '未知'
  const colorValue = myPlayerNumber.value === 1 ? p1Color.value : p2Color.value
  return colorValue === 1 ? '黑棋' : '白棋'
})

const opponentChessColor = computed(() => {
  if (myPlayerNumber.value === 0) return '对方'
  const colorValue = myPlayerNumber.value === 1 ? p2Color.value : p1Color.value
  return colorValue === 1 ? '黑棋' : '白棋'
})

let endRedirectTimer: number | null = null
let gameOverHandled = false
const controlsDisabled = computed(() => gameOver.value || redirectPending.value)
const showEndMask = computed(() => gameOver.value && gameOverHandled)
const liveGirlBottomOffset = computed(() => roomHeight.value <= 8 ? 24 : 0)
let lastAnnouncedMove = -1
let lastAnnouncedPlayer = 0

const scheduleGameEndRedirect = () => {
  // 对局结束清空未执行的AI延时落子
  if (autoPlayTimer) {
    clearTimeout(autoPlayTimer)
    autoPlayTimer = null
  }
  if (endRedirectTimer) clearTimeout(endRedirectTimer)
  redirectPending.value = true
  endRedirectTimer = window.setTimeout(() => {
    router.replace('/online-room')
  }, 3000)
}

const pollRoomState = async () => {
  try {
    const res = await getRoomState(roomId.value)
    const justGameOver = res.gameOver && !gameOver.value
    currentPlayerNum.value = res.currentPlayer
    gameOver.value = res.gameOver
    p1ClientId.value = res.player1
    p2ClientId.value = res.player2
    p1Color.value = res.player1Color
    p2Color.value = res.player2Color
    pendingUndoRequester.value = res.undoRequester
    lastMove.value = res.lastMove ?? -1

    // 同步后端托管开关状态
    const myClient = clientId.value.trim()
    if (res.autoPlay && typeof res.autoPlay === 'object') {
      autoPlayEnabled.value = !!res.autoPlay[myClient]
    }

    if (res.lastMove !== undefined && res.lastMove !== null && res.lastMove >= 0 && res.lastMovePlayer && res.lastMovePlayer !== myPlayerNumber.value && (res.lastMove !== lastAnnouncedMove || res.lastMovePlayer !== lastAnnouncedPlayer)) {
      const row = Math.floor(res.lastMove / roomWidth.value)
      const col = res.lastMove % roomWidth.value
      setNewLiveGirlMessage(`对方下在 ${row}, ${col}`, 2600)
      lastAnnouncedMove = res.lastMove
      lastAnnouncedPlayer = res.lastMovePlayer
    }

    if (res.lastMove !== undefined && res.lastMove !== null && res.lastMove >= 0 && res.lastMovePlayer) {
      const threat = checkThreat(res.lastMove, res.lastMovePlayer, res.states)
      if (threat) {
        setLiveGirlAction(threat === '冲四' ? 'jump' : 'cheer', 900)
      }
    }

    roomWidth.value = res.width || 8
    roomHeight.value = res.height || 8
    if (!changeChessState) {
      const created = useChessBoard(roomHeight.value, roomWidth.value)
      board = created.board
      changeChessState = created.changeChessState
    }

    // 清空棋盘
    for (let i = 0; i < roomHeight.value; i++) {
      for (let j = 0; j < roomWidth.value; j++) {
        changeChessState(i, j, 'noChess')
      }
    }

    const states = res.states
    for (const moveStr of Object.keys(states)) {
      const move = Number(moveStr)
      const playerVal = states[moveStr]
      const row = Math.floor(move / roomWidth.value)
      const col = move % roomWidth.value
      if (playerVal === 1) {
        changeChessState(row, col, 'Player1')
      } else if (playerVal === 2) {
        changeChessState(row, col, 'Player2')
      }
    }

    if (res.gameOver) {
      if (justGameOver && !gameOverHandled) {
        gameOverHandled = true
        if (res.endedBySurrender) {
          tipText.value = res.winner === myPlayerNumber.value ? '你赢了' : '你输了'
        } else if (res.winner === myPlayerNumber.value) {
          tipText.value = '你赢了'
        } else if (res.winner === -1 || res.winner === 0) {
          tipText.value = '平局结束'
        } else {
          tipText.value = '你输了'
        }
        scheduleGameEndRedirect()
      }
    } else if (pendingUndoRequester.value && pendingUndoRequester.value !== clientId.value) {
      tipText.value = '对方请求悔棋，请处理'
    } else if (myPlayerNumber.value === 0) {
      tipText.value = '等待对手加入房间...'
    } else if (res.currentPlayer === myPlayerNumber.value) {
      tipText.value = `轮到你下棋（${selfChessColor.value}）`
    } else {
      tipText.value = `轮到对方下棋（${opponentChessColor.value}）`
    }
  } catch (err) {
    tipText.value = '棋盘同步失败，正在重试...'
  }
}

const checkThreat = (moveIndex: number, player: number, states: Record<number, number>) => {
  const width = roomWidth.value
  const height = roomHeight.value
  const row = Math.floor(moveIndex / width)
  const col = moveIndex % width
  const directions = [[0, 1], [1, 0], [1, 1], [1, -1]] as const

  for (const [dr, dc] of directions) {
    let count = 1
    let openEnds = 0
    const walk = (step: number) => {
      const nr = row + dr * step
      const nc = col + dc * step
      if (nr < 0 || nr >= height || nc < 0 || nc >= width) return 0
      const value = states[nr * width + nc]
      if (value === player) {
        count += 1
        return 1
      }
      if (value === undefined || value === 0) {
        openEnds += 1
        return 0
      }
      return 0
    }
    for (let step = 1; step <= 4; step++) if (!walk(step)) break
    for (let step = -1; step >= -4; step--) {
      const nr = row + dr * step
      const nc = col + dc * step
      if (nr < 0 || nr >= height || nc < 0 || nc >= width) continue
      const value = states[nr * width + nc]
      if (value === player) count += 1
      else if (value === undefined || value === 0) openEnds += 1
    }
    if (count >= 4 && openEnds >= 1) return '冲四'
    if (count >= 3 && openEnds >= 1) return '活三'
  }
  return false
}

const handleToggleAutoPlay = async () => {
  try {
    const res = await toggleAutoPlay(roomId.value, clientId.value)
    if (res.data.code === 200) {
      autoPlayEnabled.value = res.data.enabled
      tipText.value = res.data.enabled ? '托管已开启' : '托管已关闭'
    }
  } catch (e) {
    tipText.value = '托管设置失败'
  }
}

// AI托管落子：0.5s延时，双重锁防并发堵塞
const handleAutoMove = async () => {
  // 多重拦截条件
  if (!roomId.value || gameOver.value || myPlayerNumber.value === 0) return
  if (currentPlayerNum.value !== myPlayerNumber.value) return
  if (!autoPlayEnabled.value) return
  if (isAutoCalculating.value) return

  isAutoCalculating.value = true
  try {
    const res = await fetch('/room/auto-play-move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ room_id: roomId.value, client_id: clientId.value })
    })
    const moveRes = await res.json()
    if (moveRes.code !== 200 || moveRes.move === undefined) {
      tipText.value = moveRes.msg || 'AI思考失败'
      return
    }
    const targetMove = moveRes.move
    // 延时500ms模拟AI思考，错开双人请求时序防止通信堵塞
    autoPlayTimer = window.setTimeout(async () => {
      await roomMove(roomId.value, clientId.value, targetMove)
      await pollRoomState()
      autoPlayTimer = null
    }, 500)
  } catch (e) {
    tipText.value = '托管请求网络异常'
  } finally {
    isAutoCalculating.value = false
  }
}

const handleClickCell = async (row: number, col: number) => {
  if (gameOver.value) return
  const localId = clientId.value.trim()
  const p1 = p1ClientId.value.trim()
  const p2 = p2ClientId.value.trim()
  const myTurn = (currentPlayerNum.value === 1 && localId === p1) || (currentPlayerNum.value === 2 && localId === p2)
  if (!myTurn) {
    tipText.value = '落子失败，请等待对方操作'
    return
  }
  const moveIndex = row * roomWidth.value + col
  try {
    await roomMove(roomId.value, clientId.value, moveIndex)
    pollRoomState()
  } catch (err) {
    tipText.value = '落子失败，请等待对方操作'
  }
}

const handleSurrender = async () => {
  // 认输清空AI延时落子
  if (autoPlayTimer) {
    clearTimeout(autoPlayTimer)
    autoPlayTimer = null
  }
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
  if (endRedirectTimer) {
    clearTimeout(endRedirectTimer)
    endRedirectTimer = null
  }
  try {
    await surrenderRoom(roomId.value, clientId.value)
  } catch (e) {}
  tipText.value = '你已认输，返回大厅'
  gameOver.value = true
  scheduleGameEndRedirect()
}

const handleUndoRequest = async () => {
  if (pendingUndoRequester.value) {
    tipText.value = '已有待处理的悔棋申请'
    return
  }
  if (!canRequestUndo.value) {
    tipText.value = ownMoveCount.value === 0 ? '你还没有下过棋，无法请求悔棋' : '当前无法请求悔棋'
    return
  }
  try {
    await undoRequest(roomId.value, clientId.value)
    tipText.value = '已发送悔棋申请，等待对方回应'
  } catch (e) {
    tipText.value = '悔棋申请发送失败'
  }
}

const handleUndoReply = async (accept: boolean) => {
  try {
    const res = await undoReply(roomId.value, clientId.value, accept)
    pendingUndoRequester.value = ''
    if (accept && res.states) {
      // 清空棋盘
      for (let i = 0; i < roomHeight.value; i++) {
        for (let j = 0; j < roomWidth.value; j++) {
          changeChessState(i, j, 'noChess')
        }
      }
      // 重绘所有棋子
      Object.entries(res.states).forEach(([k, v]) => {
        const move = Number(k)
        const row = Math.floor(move / roomWidth.value)
        const col = move % roomWidth.value
        if (v === 1) changeChessState(row, col, 'Player1')
        if (v === 2) changeChessState(row, col, 'Player2')
      })
      // 立即用后端返回的最新lastMove刷新高光，无需等待轮询
      lastMove.value = res.lastMove ?? -1
      currentPlayerNum.value = res.currentPlayer ?? currentPlayerNum.value
      gameOver.value = res.gameOver ?? false
      tipText.value = '对方已同意悔棋，棋子已回退'
    } else {
      tipText.value = '对方拒绝了你的悔棋请求'
    }
  } catch (e) {
    tipText.value = '处理悔棋请求失败'
  }
}

// 监听悔棋弹窗
watch(() => pendingUndoRequester.value, async (newVal, oldVal) => {
  if (newVal && newVal !== clientId.value && !oldVal) {
    const agree = window.confirm('对方请求悔棋，是否同意？')
    await handleUndoReply(agree)
  }
})

// 回合切换/托管开关变更，自动执行AI思考落子
watch([currentPlayerNum, myPlayerNumber, autoPlayEnabled], async () => {
  if (currentPlayerNum.value === myPlayerNumber.value && autoPlayEnabled.value && myPlayerNumber.value !== 0) {
    await handleAutoMove()
  }
})

onUnmounted(() => {
  // 页面销毁清理所有定时器，防止残留延时落子
  if (pollTimer) clearInterval(pollTimer)
  if (endRedirectTimer) clearTimeout(endRedirectTimer)
  if (autoPlayTimer) clearTimeout(autoPlayTimer)
})
</script>

<style scoped>
.online-board-wrap {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding-top: 24px;
  gap: 10px;
}
.board-area {
  position: relative;
}
.action-row {
  display: flex;
  gap: 10px;
}
.surrender-btn,
.undo-btn,
.auto-btn {
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  font-size: 14px;
}
.surrender-btn {
  background: #e74c3c;
}
.surrender-btn:hover:not(:disabled) {
  background: #c0392b;
}
.undo-btn {
  background: #409eff;
}
.undo-btn:hover:not(:disabled) {
  background: #3385d6;
}
.auto-btn {
  background: #f39c12;
}
.auto-btn:hover:not(:disabled) {
  background: #d8890d;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.self-color {
  font-size: 16px;
  font-weight: bold;
  color: #c83c3c;
}
.tip {
  font-size: 14px;
  color: #27ae60;
}
.game-end-mask {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.18);
  pointer-events: none;
  animation: fadeInMask 0.25s ease-out;
}
.mask-content {
  padding: 14px 20px;
  max-width: 320px;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 18px;
  color: #333;
  font-size: 18px;
  font-weight: 700;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.16);
  text-align: center;
  transform: translateY(-8px);
  animation: fadeInLayer 0.28s ease-out;
}
@keyframes fadeInMask {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes fadeInLayer {
  from { opacity: 0; transform: translateY(-14px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
