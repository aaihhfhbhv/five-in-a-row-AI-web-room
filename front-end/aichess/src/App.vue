<template>
  <nav>
    <router-link to="/" class="nav-home-link">AI Chess</router-link>
  </nav>
  <router-view/>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

onMounted(() => {
  const navEntries = performance.getEntriesByType('navigation') as PerformanceNavigationTiming[]
  if (navEntries[0]?.type === 'reload') {
    if (route.path !== '/') {
      router.replace('/')
    }
  }
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #27ae60; /* 绿色文字 */
  text-decoration: none; /* 取消下划线 */
  font-size: 20px;
}
nav a.router-link-exact-active {
  color: #27ae60;
  text-decoration: none;
}
</style>
