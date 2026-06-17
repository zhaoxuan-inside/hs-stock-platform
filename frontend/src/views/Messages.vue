<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Mail, Bell, CheckCircle2, Clock, AlertCircle, ChevronRight } from 'lucide-vue-next'
import { taskApi } from '@/utils/api'
import type { Message } from '@/utils/api'

const messages = ref<Message[]>([])
const loading = ref(false)
const filter = ref<'all' | 'unread' | 'read'>('all')

const fetchMessages = async () => {
  loading.value = true
  try {
    const response = await taskApi.listMessages({
      user_id: '1',
      status: filter.value === 'all' ? undefined : filter.value,
      limit: 50,
    })
    messages.value = response.data
  } catch (e) {
    console.error('Failed to fetch messages:', e)
  } finally {
    loading.value = false
  }
}

const markAsRead = async (id: string) => {
  try {
    await taskApi.updateMessageStatus(id, 'read')
    fetchMessages()
  } catch (e) {
    console.error('Failed to update message status:', e)
  }
}

const markAllAsRead = async () => {
  const unreadMessages = messages.value.filter(m => m.status === 'unread')
  for (const msg of unreadMessages) {
    await markAsRead(msg.id)
  }
}

const getTypeIcon = (type: string) => {
  switch (type) {
    case 'success': return CheckCircle2
    case 'warning': return Clock
    case 'error': return AlertCircle
    default: return Bell
  }
}

const getTypeColor = (type: string) => {
  switch (type) {
    case 'success': return 'text-green-500 bg-green-100'
    case 'warning': return 'text-yellow-500 bg-yellow-100'
    case 'error': return 'text-red-500 bg-red-100'
    default: return 'text-blue-500 bg-blue-100'
  }
}

onMounted(() => {
  fetchMessages()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">消息通知</h1>
        <p class="text-gray-500 mt-1">查看系统消息和任务通知</p>
      </div>
      <button @click="markAllAsRead" class="btn-secondary flex items-center gap-2">
        <CheckCircle2 class="w-4 h-4" /> 全部已读
      </button>
    </div>

    <div class="card">
      <div class="flex items-center gap-4 mb-4">
        <div class="flex items-center gap-2">
          <Mail class="w-5 h-5 text-gray-600" />
          <button
            v-for="f in [{ key: 'all', label: '全部' }, { key: 'unread', label: '未读' }, { key: 'read', label: '已读' }]"
            :key="f.key"
            @click="filter = f.key as 'all' | 'unread' | 'read'; fetchMessages()"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              filter === f.key ? 'bg-primary text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            {{ f.label }}
          </button>
        </div>
        <div class="ml-auto text-sm text-gray-500">
          共 {{ messages.length }} 条消息
        </div>
      </div>

      <div v-if="loading" class="flex justify-center py-12">
        <div class="flex items-center gap-2">
          <div class="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
          <span class="text-gray-500">加载中...</span>
        </div>
      </div>

      <div v-else-if="messages.length === 0" class="text-center py-12">
        <Bell class="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-500">暂无消息</p>
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="[
            'flex items-start gap-4 p-4 rounded-lg border transition-colors cursor-pointer',
            message.status === 'unread' ? 'bg-blue-50 border-blue-200' : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
          ]"
          @click="markAsRead(message.id)"
        >
          <div :class="['w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0', getTypeColor(message.type)]">
            <component :is="getTypeIcon(message.type)" class="w-5 h-5" />
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between mb-1">
              <h3 class="font-medium text-gray-900">{{ message.title }}</h3>
              <span class="text-xs text-gray-500">{{ message.created_at }}</span>
            </div>
            <p class="text-sm text-gray-600 truncate">{{ message.content }}</p>
          </div>
          <ChevronRight class="w-5 h-5 text-gray-400 flex-shrink-0" />
        </div>
      </div>
    </div>
  </div>
</template>