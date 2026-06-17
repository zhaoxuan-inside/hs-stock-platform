<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Bell, Search, Calendar } from 'lucide-vue-next'

const currentTime = ref(new Date())
let timer: ReturnType<typeof setInterval>

onMounted(() => {
  timer = setInterval(() => {
    currentTime.value = new Date()
  }, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})

const formatDate = (date: Date) => {
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    weekday: 'short'
  })
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>

<template>
  <header class="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
    <div class="flex items-center gap-4">
      <div class="relative">
        <Search class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="搜索股票代码或名称..."
          class="pl-9 pr-4 py-2 w-64 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
        />
      </div>
    </div>

    <div class="flex items-center gap-6">
      <div class="flex items-center gap-2 text-gray-600">
        <Calendar class="w-4 h-4" />
        <span class="text-sm">{{ formatDate(currentTime) }}</span>
        <span class="font-mono text-primary font-medium">{{ formatTime(currentTime) }}</span>
      </div>

      <button class="relative p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <Bell class="w-5 h-5 text-gray-600" />
        <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
      </button>

      <div class="flex items-center gap-3 pl-4 border-l border-gray-200">
        <div class="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
          <span class="text-primary font-medium">U</span>
        </div>
        <div class="hidden sm:block">
          <p class="text-sm font-medium text-gray-900">管理员</p>
          <p class="text-xs text-gray-500">admin@example.com</p>
        </div>
      </div>
    </div>
  </header>
</template>