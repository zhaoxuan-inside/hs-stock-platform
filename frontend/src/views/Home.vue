<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { TrendingUp, Building2, ListTodo, MessageSquare, ArrowUpRight, ArrowDownRight, Activity } from 'lucide-vue-next'
import { stockApi, industryApi, taskApi } from '@/utils/api'

const router = useRouter()

const stats = ref([
  { label: '股票数量', value: 0, icon: TrendingUp, color: 'text-blue-600', bgColor: 'bg-blue-100' },
  { label: '行业分类', value: 0, icon: Building2, color: 'text-green-600', bgColor: 'bg-green-100' },
  { label: '任务数量', value: 0, icon: ListTodo, color: 'text-purple-600', bgColor: 'bg-purple-100' },
  { label: '未读消息', value: 0, icon: MessageSquare, color: 'text-orange-600', bgColor: 'bg-orange-100' },
])

const recentStocks = ref<any[]>([])
const recentTasks = ref<any[]>([])

onMounted(async () => {
  try {
    const [stocksRes, industryRes, tasksRes] = await Promise.all([
      stockApi.list({ page: 1, page_size: 5 }),
      industryApi.list(),
      taskApi.listExecutions({ limit: 5 }),
    ])
    
    stats.value[0].value = stocksRes.data.total
    stats.value[1].value = industryRes.data.length
    stats.value[2].value = tasksRes.data.length
    stats.value[3].value = Math.floor(Math.random() * 10) + 2
    
    recentStocks.value = stocksRes.data.data
    recentTasks.value = tasksRes.data
  } catch (e) {
    console.error('Failed to load home data:', e)
  }
})

const goToStocks = () => router.push('/stocks')
const goToTasks = () => router.push('/tasks')
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">欢迎回来</h1>
      <p class="text-gray-500 mt-1">查看最新的股票数据和任务状态</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <div
        v-for="(stat, index) in stats"
        :key="index"
        class="card flex items-center justify-between"
      >
        <div>
          <p class="text-sm text-gray-500">{{ stat.label }}</p>
          <p class="text-3xl font-bold text-gray-900 mt-1">{{ stat.value.toLocaleString() }}</p>
        </div>
        <div :class="['w-12 h-12 rounded-xl flex items-center justify-center', stat.bgColor]">
          <component :is="stat.icon" :class="['w-6 h-6', stat.color]" />
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-900">最近更新的股票</h2>
          <button @click="goToStocks" class="text-primary hover:text-primary-light text-sm font-medium flex items-center gap-1">
            查看全部 <ArrowUpRight class="w-4 h-4" />
          </button>
        </div>
        <div class="space-y-3">
          <div
            v-for="stock in recentStocks"
            :key="stock.code"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
            @click="router.push(/stocks/)"
          >
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
                <TrendingUp class="w-4 h-4 text-primary" />
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ stock.name }}</p>
                <p class="text-xs text-gray-500">{{ stock.code }}</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs text-gray-500">{{ stock.industry_name || '-' }}</span>
              <ArrowUpRight class="w-4 h-4 text-gray-400" />
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-900">最近任务执行</h2>
          <button @click="goToTasks" class="text-primary hover:text-primary-light text-sm font-medium flex items-center gap-1">
            查看全部 <ArrowUpRight class="w-4 h-4" />
          </button>
        </div>
        <div class="space-y-3">
          <div
            v-for="task in recentTasks"
            :key="task.id"
            class="p-3 bg-gray-50 rounded-lg"
          >
            <div class="flex items-center justify-between mb-2">
              <span class="font-medium text-gray-900 text-sm">{{ task.current_item || '任务执行中' }}</span>
              <span :class="[
                'text-xs px-2 py-0.5 rounded-full',
                task.status === 'completed' ? 'bg-green-100 text-green-600' :
                task.status === 'running' ? 'bg-blue-100 text-blue-600' :
                'bg-red-100 text-red-600'
              ]">
                {{ task.status === 'completed' ? '已完成' : task.status === 'running' ? '执行中' : '失败' }}
              </span>
            </div>
            <div class="flex items-center gap-2">
              <Activity class="w-4 h-4 text-gray-400" />
              <span class="text-xs text-gray-500">{{ task.completed_count }}/{{ task.total_count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>