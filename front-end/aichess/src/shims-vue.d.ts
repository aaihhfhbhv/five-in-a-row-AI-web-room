/* eslint-disable */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// 新增兜底声明，直接消除 TS7016 编译报错
declare module 'vue-router'
