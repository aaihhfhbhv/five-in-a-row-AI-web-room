import { reactive } from 'vue'

export type ChessState = 'noChess' | 'Player1' | 'Player2'
export type ChessRow = ChessState[]
export type Board = ChessRow[]

const useChessBoard = (rowCount: number, colCount: number) => {
  const initBoard = (): Board => {
    const board: Board = []
    for (let i = 0; i < rowCount; i++) {
      const line: ChessRow = []
      for (let j = 0; j < colCount; j++) {
        line.push('noChess')
      }
      board.push(line)
    }
    return reactive(board)
  }

  const board = initBoard()

  const changeChessState = (r: number, c: number, state: ChessState): void => {
    // 边界防护，防止越界赋值
    if (r >= 0 && r < board.length && c >= 0 && c < board[0].length) {
      board[r][c] = state
    }
  }

  return {
    board,
    changeChessState
  }
}

export default useChessBoard
