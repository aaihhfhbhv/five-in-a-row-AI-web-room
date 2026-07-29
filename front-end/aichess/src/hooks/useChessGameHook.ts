import { computed, ref } from 'vue'
import { ChessState, Board } from './useChessBoardHook'
import { setNewLiveGirlMessage } from './useLiveGirlMessageHook'

type Player = 'Player1' | 'Player2'

const useChessGame = (
  board: Board,
  changeChessState: (row: number, col: number, state: ChessState | Player) => void
) => {
  const currentPlayer = ref<Player>('Player1')
  const oppositePlayer = computed(() => currentPlayer.value === 'Player1' ? 'Player2' : 'Player1')

  const changeCurrentPlayerTo = (player: Player) => {
    currentPlayer.value = player
  }

  const nextPlayerTurn = () => {
    currentPlayer.value = currentPlayer.value === 'Player1' ? 'Player2' : 'Player1'
  }

  const initGame = () => {
    for (let i = 0; i < board.length; i++) {
      for (let j = 0; j < board[0].length; j++) {
        changeChessState(i, j, 'noChess')
      }
    }
    changeCurrentPlayerTo('Player1')
    setNewLiveGirlMessage('请君先手（￣︶￣）↗', 3000)
  }

  const putChess = (row: number, col: number) => {
    if (board[row][col] !== 'noChess') {
      setNewLiveGirlMessage('这里已经有棋子啦，换个位置~', 3000)
      return
    }
    changeChessState(row, col, currentPlayer.value)
    nextPlayerTurn()
  }

  // 完整五子连珠胜负判断
  const getWinner = (move: number): Player | false => {
    // AI特殊返回码
    if (move === -2) return 'Player2'
    if (move === -1) return 'Player1'

    const width = board[0].length
    const r = Math.floor(move / width)
    const c = move % width
    const player = board[r][c]

    if (player === 'noChess') return false

    // 四个判定方向：横、竖、左上-右下、右上-左下
    const directions = [[0, 1], [1, 0], [1, 1], [1, -1]]
    for (const [dr, dc] of directions) {
      let count = 1
      // 正向延伸
      for (let step = 1; ; step++) {
        const nr = r + dr * step
        const nc = c + dc * step
        if (nr < 0 || nr >= board.length || nc < 0 || nc >= width || board[nr][nc] !== player) break
        count++
      }
      // 反向延伸
      for (let step = 1; ; step++) {
        const nr = r - dr * step
        const nc = c - dc * step
        if (nr < 0 || nr >= board.length || nc < 0 || nc >= width || board[nr][nc] !== player) break
        count++
      }
      if (count >= 5) return player
    }
    return false
  }

  return {
    currentPlayer,
    oppositePlayer,
    changeCurrentPlayerTo,
    nextPlayerTurn,
    initGame,
    putChess,
    getWinner
  }
}

export default useChessGame
export { Player }
