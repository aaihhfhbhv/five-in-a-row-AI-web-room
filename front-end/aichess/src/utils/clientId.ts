import { ref, Ref } from 'vue'

// 兼容低版本浏览器手动生成UUID，替代 crypto.randomUUID
function generateUUID (): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

export function getClientId (): Ref<string> {
  const storageKey = 'chess_client_uuid'
  // 读取本地存储，默认空字符串消除null类型
  let uuid: string = localStorage.getItem(storageKey) || ''
  if (!uuid) {
    uuid = generateUUID()
    localStorage.setItem(storageKey, uuid)
  }
  return ref(uuid)
}
