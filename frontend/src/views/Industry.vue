<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Building2, TrendingUp, ArrowRight, ChevronDown, ChevronUp } from 'lucide-vue-next'
import { industryApi, stockApi } from '@/utils/api'
import type { Industry, Stock, StockIndex } from '@/utils/api'

const router = useRouter()

const industries = ref<Industry[]>([])
const indexes = ref<StockIndex[]>([])
const expandedIndustries = ref<Set<string>>(new Set())
const industryStocks = ref<Map<string, Stock[]>>(new Map())

const fetchIndustries = async () => {
  try {
    const response = await industryApi.list()
    industries.value = response.data
  } catch (e) {
    console.error('Failed to fetch industries:', e)
  }
}

const fetchIndexes = async () => {
  try {
    const response = await industryApi.listIndexes()
    indexes.value = response.data
  } catch (e) {
    console.error('Failed to fetch indexes:', e)
  }
}

const fetchIndustryStocks = async (industryCode: string) => {
  if (industryStocks.value.has(industryCode)) return
  
  try {
    const response = await stockApi.list({ industry_code: industryCode, page: 1, page_size: 20 })
    industryStocks.value.set(industryCode, response.data.data)
  } catch (e) {
    console.error('Failed to fetch industry stocks:', e)
  }
}

const toggleIndustry = async (code: string) => {
  if (expandedIndustries.value.has(code)) {
    expandedIndustries.value.delete(code)
  } else {
    expandedIndustries.value.add(code)
    await fetchIndustryStocks(code)
  }
}

const goToStockDetail = (code: string) => {
  router.push(/stocks/)
}

onMounted(() => {
  fetchIndustries()
  fetchIndexes()
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">行业分析</h1>
      <p class="text-gray-500 mt-1">查看行业分类和指数成分股</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <div class="flex items-center gap-2 mb-4">
          <Building2 class="w-5 h-5 text-gray-600" />
          <h2 class="text-lg font-semibold text-gray-900">行业分类</h2>
        </div>
        <div class="space-y-2">
          <div
            v-for="industry in industries"
            :key="industry.code"
            class="border border-gray-200 rounded-lg overflow-hidden"
          >
            <button
              @click="toggleIndustry(industry.code)"
              class="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-center gap-3">
                <Building2 class="w-5 h-5 text-primary" />
                <span class="font-medium text-gray-900">{{ industry.name }}</span>
              </div>
              <ChevronDown v-if="!expandedIndustries.has(industry.code)" class="w-5 h-5 text-gray-400" />
              <ChevronUp v-else class="w-5 h-5 text-gray-400" />
            </button>
            
            <div v-if="expandedIndustries.has(industry.code)" class="border-t border-gray-200 bg-gray-50">
              <div v-if="industryStocks.get(industry.code)?.length === 0" class="p-4 text-center text-gray-500">
                暂无股票数据
              </div>
              <div v-else class="p-2">
                <div
                  v-for="stock in industryStocks.get(industry.code)"
                  :key="stock.code"
                  @click="goToStockDetail(stock.code)"
                  class="flex items-center justify-between p-3 rounded-lg hover:bg-white cursor-pointer transition-colors"
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
                  <ArrowRight class="w-4 h-4 text-gray-400" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center gap-2 mb-4">
          <TrendingUp class="w-5 h-5 text-gray-600" />
          <h2 class="text-lg font-semibold text-gray-900">指数列表</h2>
        </div>
        <div class="space-y-3">
          <div
            v-for="index in indexes"
            :key="index.code"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
          >
            <div>
              <h3 class="font-medium text-gray-900">{{ index.name }}</h3>
              <p class="text-sm text-gray-500">{{ index.code }} · {{ index.type }}</p>
            </div>
            <ArrowRight class="w-5 h-5 text-gray-400" />
          </div>
        </div>
        
        <div v-if="indexes.length === 0" class="text-center py-8">
          <p class="text-gray-500">暂无指数数据</p>
        </div>
      </div>
    </div>
  </div>
</template>