<script lang="ts" setup>
import { toRefs, defineProps, defineEmits, withDefaults } from 'vue'
import type { ChessState } from '../hooks/useChessBoardHook'

interface Props {
  rowIndex: number
  colIndex: number
  state: ChessState
  player1Color: number
  player2Color: number
  highlight?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  highlight: false
})
const { state, player1Color, player2Color, highlight } = toRefs(props)
const emit = defineEmits<{ click: [] }>()

const getChessClass = (): string => {
  if (state.value === 'Player1') {
    return player1Color.value === 1 ? 'chess-state--player-1' : 'chess-state--player-2'
  }
  if (state.value === 'Player2') {
    return player2Color.value === 1 ? 'chess-state--player-1' : 'chess-state--player-2'
  }
  return 'chess-state--no-chess'
}
</script>

<template>
  <div class="cell" @click="emit('click')">
    <div v-if="state === 'noChess'" class="cell-hover-tip"></div>
    <div v-if="highlight" class="last-move-dot"></div>
    <div class="chess" :class="getChessClass()"></div>
  </div>
</template>

<style scoped>
.cell {
  width: 100%;
  height: 100%;
  position: relative;
  cursor: pointer;
}

.cell-hover-tip {
  position: absolute;
  width: 60%;
  height: 60%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.08);
  opacity: 0;
  transition: opacity 0.2s;
}
.cell:hover .cell-hover-tip {
  opacity: 1;
}

.chess {
  position: absolute;
  width: 65%;
  height: 65%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.15s ease;
}

.chess-state--player-1:hover,
.chess-state--player-2:hover {
  transform: translate(-50%, -50%) scale(1.05);
}

.chess-state--no-chess {
  background: transparent;
  pointer-events: none;
}
.chess-state--player-1 {
  background: #1a1a1a;
}
.chess-state--player-2 {
  background: #fff;
  border: 1px solid #ddd;
}
.last-move-dot {
  position: absolute;
  width: 12px;
  height: 12px;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: #2ecc71;
  box-shadow: 0 0 0 3px rgba(46, 204, 113, 0.25);
  z-index: 2;
  pointer-events: none;
}
</style>
