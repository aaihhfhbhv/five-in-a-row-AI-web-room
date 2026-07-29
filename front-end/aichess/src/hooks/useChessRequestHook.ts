import axios from 'axios'
import { ref } from 'vue'
import { Board } from './useChessBoardHook'
import { Player } from './useChessGameHook'
import { setNewLiveGirlMessage } from './useLiveGirlMessageHook'

axios.defaults.baseURL = ''

// ==================== 类型定义（全部改为驼峰，消除lint报错） ====================
// 单机AI接口返回结构
interface AiResponse {
  move: number
}

// 创建房间返回
interface CreateRoomRes {
  code: number
  roomId: string
  msg: string
}

// 加入房间返回
interface JoinRoomRes {
  code: number
  msg: string
  roomId: string
}

// 联机落子返回
interface RoomMoveRes {
  code: number
  states: Record<number, number>
  currentPlayer: number
  gameOver: boolean
  winner: number
}

interface UndoReplyRes {
  code: number
  msg: string
  states?: Record<number, number>
  currentPlayer?: number
  gameOver?: boolean
  winner?: number
}

// 获取房间状态返回
interface RoomStateRes {
  code: number
  states: Record<number, number>
  currentPlayer: number
  gameOver: boolean
  winner: number
  player1: string
  player2: string
  player1Color: number
  player2Color: number
  matchReady: boolean
  undoRequester: string
  width: number
  height: number
  endedBySurrender: boolean
  lastMove: number
  lastMovePlayer: number
}

// 通用post返回包装
type ApiPromise<T> = Promise<{ data: T }>

// ==================== 请求hook ====================
const useChessRequest = (board: Board, aiPlayer: Player) => {
  const chessRequestingLock = ref<boolean>(false)

  const lock = () => {
    chessRequestingLock.value = true
  }
  const unlock = () => {
    chessRequestingLock.value = false
  }

  // 格式化棋盘数据（单机AI专用）
  const reformData = (lastMove: number) => {
    const states: Record<number, number> = {}
    for (let i = 0; i < board.length; i++) {
      for (let j = 0; j < board[0].length; j++) {
        if (board[i][j] !== 'noChess') {
          states[i * board[0].length + j] = board[i][j] === 'Player1' ? 1 : 2
        }
      }
    }
    return {
      states,
      last_move: lastMove,
      player: aiPlayer === 'Player1' ? 1 : 2,
      width: board[0].length,
      height: board.length
    }
  }

  // 通用POST请求封装
  const post = <T>(url: string, data = {}): ApiPromise<T> => {
    return new Promise<{ data: T }>((resolve, reject) => {
      // 后端端口5001，局域网/本机统一地址
      const currentHost = window.location.host.split(':')[0]
      axios.post(url, data, {
        baseURL: `http://${currentHost}:5001`,
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 80000
      }).then((response) => {
        resolve(response as { data: T })
      }, err => {
        reject(err)
      })
    })
  }

  // ==================== 单机AI对战接口 ====================
  const requestAi = async (lastMove: number | undefined) => {
    lock()
    try {
      const safeLastMove = typeof lastMove === 'number' ? lastMove : -1
      const response = await post<AiResponse>('/aichess', reformData(safeLastMove))
      return response.data.move
    } catch (e) {
      setNewLiveGirlMessage('(⊙x⊙;) AI服务故障，请检查后端', 5000)
      throw Error('requestAi post error')
    } finally {
      unlock()
    }
  }

  // ==================== 联机房间接口新增 ====================
  /**
   * 创建联机房间
   * @param clientId 客户端唯一标识（本机随机uuid）
   */
  const createRoom = async (clientId: string): Promise<CreateRoomRes> => {
    try {
      const res = await post<CreateRoomRes>('/room/create', { client_id: clientId })
      return res.data
    } catch (e) {
      setNewLiveGirlMessage('创建房间失败，后端未启动', 4000)
      throw e
    }
  }

  const createRoomWithSize = async (clientId: string, width: number, height: number): Promise<CreateRoomRes> => {
    try {
      const res = await post<CreateRoomRes>('/room/create', { client_id: clientId, width, height })
      return res.data
    } catch (e) {
      setNewLiveGirlMessage('创建房间失败，后端未启动', 4000)
      throw e
    }
  }

  /**
   * 加入已有房间
   * @param roomId 6位房间号
   * @param clientId 客户端标识
   */
  const joinRoom = async (roomId: string, clientId: string): Promise<JoinRoomRes> => {
    try {
      const res = await post<JoinRoomRes>('/room/join', { room_id: roomId, client_id: clientId })
      return res.data
    } catch (e) {
      setNewLiveGirlMessage('加入房间失败，房间不存在/已满', 4000)
      throw e
    }
  }

  /**
   * 联机双人落子提交
   * @param roomId 房间号
   * @param clientId 当前玩家标识
   * @param move 一维坐标索引
   */
  const roomMove = async (roomId: string, clientId: string, move: number): Promise<RoomMoveRes> => {
    try {
      const res = await post<RoomMoveRes>('/room/move', {
        room_id: roomId,
        client_id: clientId,
        move
      })
      return res.data
    } catch (e) {
      setNewLiveGirlMessage('落子失败，请等待对方操作', 3000)
      throw e
    }
  }

  const surrenderRoom = async (roomId: string, clientId: string): Promise<{code:number; msg:string}> => {
    const res = await post<{code:number; msg:string}>('/room/surrender', {
      room_id: roomId,
      client_id: clientId
    })
    return res.data
  }

  const undoRequest = async (roomId: string, clientId: string): Promise<{code:number; msg:string}> => {
    const res = await post<{code:number; msg:string}>('/room/undo/request', {
      room_id: roomId,
      client_id: clientId
    })
    return res.data
  }

  const undoReply = async (roomId: string, clientId: string, accept: boolean): Promise<UndoReplyRes> => {
    const res = await post<UndoReplyRes>('/room/undo/reply', {
      room_id: roomId,
      client_id: clientId,
      accept
    })
    return res.data
  }

  /**
   * 轮询拉取房间最新棋盘状态（前端定时调用同步画面）
   * @param roomId 房间号
   */
  const getRoomState = async (roomId: string): Promise<RoomStateRes> => {
    try {
      const res = await post<RoomStateRes>('/room/state', { room_id: roomId })
      return res.data
    } catch (e) {
      setNewLiveGirlMessage('同步棋盘失败', 2000)
      throw e
    }
  }

  const toggleAutoPlay = async (roomId: string, clientId: string) => {
    return post<{code:number; enabled:boolean; player:number}>('/room/auto-play', {
      room_id: roomId,
      client_id: clientId
    })
  }

  return {
    // 单机AI原有
    chessRequestingLock,
    lock,
    unlock,
    requestAi,
    // 联机新增全部方法
    createRoom,
    createRoomWithSize,
    joinRoom,
    roomMove,
    surrenderRoom,
    undoRequest,
    undoReply,
    getRoomState,
    toggleAutoPlay
  }
}

export default useChessRequest
