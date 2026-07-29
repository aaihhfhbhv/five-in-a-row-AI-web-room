<script lang="ts" setup>
import { defineProps, defineEmits, toRefs, withDefaults, computed, watch } from 'vue'
import ChessComponent from './ChessComponent.vue'
import useChessBoard, { type Board } from '../hooks/useChessBoardHook'
import useChessGame from '../hooks/useChessGameHook'
import useChessRequest from '@/hooks/useChessRequestHook'
import { setNewLiveGirlMessage } from '@/hooks/useLiveGirlMessageHook'

interface Props {
  boardHeight?: number
  boardWidth?: number
  // 新增：是否联机模式
  isOnline?: boolean
  board?: Board
  player1Color?: number
  player2Color?: number
  lastMove?: number
}
const props = withDefaults(defineProps<Props>(), {
  boardHeight: 8,
  boardWidth: 8,
  isOnline: false,
  board: undefined,
  player1Color: 1,
  player2Color: 2,
  lastMove: -1
})
const emit = defineEmits(['click-cell'])

const CELL_SIZE = 44
const { boardHeight, boardWidth, isOnline, board: externalBoard, player1Color, player2Color, lastMove } = toRefs(props)
const rowRule = computed(() => `repeat(${boardHeight.value}, ${CELL_SIZE}px)`)
const colRule = computed(() => `repeat(${boardWidth.value}, ${CELL_SIZE}px)`)
const bgSize = computed(() => `${CELL_SIZE}px ${CELL_SIZE}px`)
const bgPos = computed(() => `${CELL_SIZE / 2}px ${CELL_SIZE / 2}px`)

let { board: localBoard, changeChessState: changeLocalChessState } = useChessBoard(boardHeight.value, boardWidth.value)
const activeBoard = computed(() => externalBoard.value ?? localBoard)
watch([boardHeight, boardWidth], ([newHeight, newWidth]) => {
  if (newHeight <= 0 || newWidth <= 0) return
  const created = useChessBoard(newHeight, newWidth)
  localBoard.splice(0, localBoard.length, ...created.board)
  changeLocalChessState = created.changeChessState
})
const changeBoardState = (row: number, col: number, state: string) => {
  if (externalBoard.value) {
    externalBoard.value[row][col] = state
  } else {
    changeLocalChessState(row, col, state)
  }
}
const { initGame, putChess, getWinner } = useChessGame(activeBoard.value, changeBoardState)
const { requestAi, chessRequestingLock } = useChessRequest(activeBoard.value, 'Player2')

if (!isOnline.value) {
  initGame()
}

// 统一点击处理
const click = async (rowIndex: number, colIndex: number) => {
  if (rowIndex >= boardHeight.value || colIndex >= boardWidth.value) return

  // 联机模式：仅抛出坐标，不执行AI逻辑
  if (isOnline.value) {
    emit('click-cell', rowIndex, colIndex)
    return
  }

  // 单机AI原有逻辑保持不变
  if (chessRequestingLock.value) {
    setNewLiveGirlMessage('等下(￣ ‘i ￣;) 人家还没想完', 50000)
    return
  }
  putChess(rowIndex, colIndex)
  setNewLiveGirlMessage('让我想想ヾ(≧▽≦*)', 50000)
  const move = await requestAi(rowIndex * activeBoard.value[0].length + colIndex)
  const winner = getWinner(move)
  if (!winner) {
    const x = Math.floor(move / activeBoard.value[0].length)
    const y = move % activeBoard.value[0].length
    setNewLiveGirlMessage(`我要下在 ${x}, ${y} !`, 99999999)
    putChess(x, y)
  } else {
    if (winner === 'Player1') {
      setNewLiveGirlMessage('不可能的(⊙_⊙)', 50000)
    } else if (winner === 'Player2') {
      setNewLiveGirlMessage('正常正常~下次再战 ( •̀ .̫ •́ )✧', 50000)
    }
  }
}
</script>

<template>
  <div class="board" :style="{gridTemplateRows: rowRule, gridTemplateColumns: colRule, backgroundSize: bgSize, backgroundPosition: bgPos}">
    <template v-for="(rowData, i) in activeBoard" :key="`row-${i}`">
      <ChessComponent
        v-for="(cellState, j) in rowData"
        :key="`cell-${i}-${j}`"
        :row-index="i"
        :col-index="j"
        :state="activeBoard[i][j]"
        :player1-color="player1Color"
        :player2-color="player2Color"
        :highlight="lastMove === i * boardWidth + j"
        @click="click(i, j)"
      />
    </template>
  </div>
</template>

<style scoped>
.board {
  display: grid;
  width: fit-content;
  height: fit-content;
  background-color: #e6c99a;
  border: 2px solid #9c7c4a;
  background-image:
    linear-gradient(#9c7c4a 1px, transparent 1px),
    linear-gradient(90deg, #9c7c4a 1px, transparent 1px);
}
</style>
