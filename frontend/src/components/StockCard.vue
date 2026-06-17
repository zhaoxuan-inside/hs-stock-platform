<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { TrendingUp, Building } from 'lucide-vue-next'
import type { StockDetail } from '@/utils/api'

const props = defineProps<{
  stock: StockDetail
}>()

const router = useRouter()

const stockTypeLabel = computed(() => {
  const types: Record<string, string> = {
    'stock': '股票',
    'index': '指数',
    'fund': '基金'
  }
  return types[props.stock.type] || props.stock.type
})

const stockTypeColor = computed(() => {
  const colors: Record<string, string> = {
    'stock': 'bg-blue-100 text-blue-600',
    'index': 'bg-purple-100 text-purple-600',
    'fund': 'bg-green-100 text-green-600'
  }
  return colors[props.stock.type] || 'bg-gray-100 text-gray-600'
})

const goToDetail = () => {
  router.push(/stocks/)
}
</script>

<template>
  <div
    @click="goToDetail"
    class="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-lg hover:border-primary/30 transition-all duration-300 cursor-pointer group"
  >
    <div class="flex items-start justify-between mb-4">
      <div>
        <h3 class="text-lg font-bold text-gray-900 group-hover:text-primary transition-colors">
          {{ stock.name }}
        </h3>
        <p class="text-sm text-gray-500 mt-1">{{ stock.code }}</p>
      </div>
      <span :class="['px-2 py-1 rounded-full text-xs font-medium', stockTypeColor]">
        {{ stockTypeLabel }}
      </span>
    </div>

    <div class="flex items-center gap-4 text-sm text-gray-600">
      <div class="flex items-center gap-1.5">
        <Building class="w-4 h-4 text-gray-400" />
        <span>{{ stock.industry_name || '-' }}</span>
      </div>
      <div class="flex items-center gap-1.5">
        <TrendingUp class="w-4 h-4 text-gray-400" />
        <span>{{ stock.exchange || '-' }}</span>
      </div>
    </div>
  </div>
</template>