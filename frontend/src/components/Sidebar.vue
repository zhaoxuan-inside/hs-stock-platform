<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { LayoutDashboard, TrendingUp, Building2, ListTodo, MessageSquare, LogOut } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const collapsed = ref(false)

const menuItems = [
  { name: '首页', path: '/', icon: LayoutDashboard },
  { name: '股票列表', path: '/stocks', icon: TrendingUp },
  { name: '行业分析', path: '/industries', icon: Building2 },
  { name: '任务管理', path: '/tasks', icon: ListTodo },
  { name: '消息通知', path: '/messages', icon: MessageSquare },
]

const activeItem = (path: string) => route.path === path

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <aside
    :class="[
      'bg-white border-r border-gray-200 flex flex-col transition-all duration-300',
      collapsed ? 'w-16' : 'w-60'
    ]"
  >
    <div class="flex items-center h-16 px-4 border-b border-gray-200">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
          <TrendingUp class="w-5 h-5 text-white" />
        </div>
        <span v-if="!collapsed" class="font-bold text-lg text-primary">HS Stock</span>
      </div>
      <button
        @click="collapsed = !collapsed"
        class="ml-auto p-1 hover:bg-gray-100 rounded"
      >
        <span class="text-gray-500">
          {{ collapsed ? '>>' : '<<' }}
        </span>
      </button>
    </div>

    <nav class="flex-1 py-4">
      <ul class="space-y-1 px-3">
        <li v-for="item in menuItems" :key="item.path">
          <router-link
            :to="item.path"
            :class="[
              'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200',
              activeItem(item.path)
                ? 'bg-primary text-white'
                : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
            ]"
          >
            <component :is="item.icon" class="w-5 h-5 flex-shrink-0" />
            <span v-if="!collapsed" class="font-medium">{{ item.name }}</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <div class="p-3 border-t border-gray-200">
      <button
        @click="logout"
        :class="[
          'flex items-center gap-3 w-full px-3 py-2.5 rounded-lg transition-all duration-200',
          'text-gray-600 hover:bg-red-50 hover:text-red-600'
        ]"
      >
        <LogOut class="w-5 h-5 flex-shrink-0" />
        <span v-if="!collapsed" class="font-medium">退出登录</span>
      </button>
    </div>
  </aside>
</template>