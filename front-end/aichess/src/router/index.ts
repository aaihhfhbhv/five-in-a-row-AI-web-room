import { createRouter, createWebHistory } from 'vue-router'
import GameHome from '@/views/GameHome.vue'
import OnlineRoom from '@/views/OnlineRoom.vue'
import OnlineBoard from '@/views/OnlineBoard.vue'
import SingleGame from '@/views/SingleGame.vue'

const routes = [
  {
    path: '/',
    name: 'GameHome',
    component: GameHome
  },
  {
    path: '/single-game',
    name: 'SingleGame',
    component: SingleGame
  },
  {
    path: '/online-room',
    name: 'OnlineRoom',
    component: OnlineRoom
  },
  {
    path: '/online-board',
    name: 'OnlineBoard',
    component: OnlineBoard
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
