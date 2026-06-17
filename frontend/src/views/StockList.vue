<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Filter, RefreshCw, ChevronLeft, ChevronRight, Grid3X3, List } from 'lucide-vue-next'
import { stockApi, industryApi, type Stock } from '@/utils/api'

const router = useRouter()

const stocks = ref<Stock[]>([])
const industries = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchKeyword = ref('')
const selectedIndustry = ref('')
const selectedType = ref('')
const loading = ref(false)
const viewMode = ref<'grid' | 'list'>('grid')

const stockTypes = [
  { value: '', label: '全部类型' },
  { value: 'stock', label: '股票' },
  { value: 'index', label: '指数' },
  { value: 'fund', label: '基金' },
]

const fetchStocks = async () => {
  loading.value = true
  try {
    const response = await stockApi.list({
      keyword: searchKeyword.value || undefined,
      industry_code: selectedIndustry.value || undefined,
      type: selectedType.value || undefined,
      page: page.value,
      page_size: pageSize.value,
    })
    stocks.value = response.data.data
    total.value = response.data.total
  } catch (e) {
    console.error('Failed to fetch stocks:', e)
  } finally {
    loading.value = false
  }
}

const fetchIndustries = async () => {
  try {
    const response = await industryApi.list()
    industries.value = [{ code: '', name: '全部行业' }, ...response.data]
  } catch (e) {
    console.error('Failed to fetch industries:', e)
  }
}

const goToDetail = (code: string) => {
  router.push(/stocks/)
}

const handleSearch = () => {
  page.value = 1
  fetchStocks()
}

const handlePageChange = (newPage: number) => {
  if (newPage >= 1 && newPage <= Math.ceil(total.value / pageSize.value)) {
    page.value = newPage
    fetchStocks()
  }
}

const resetFilters = () => {
  searchKeyword.value = ''
  selectedIndustry.value = ''
  selectedType.value = ''
  page.value = 1
  fetchStocks()
}

onMounted(() => {
  fetchIndustries()
  fetchStocks()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">股票列表</h1>
        <p class="text-gray-500 mt-1">共 {{ total.toLocaleString() }} 只股票</p>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click="viewMode = 'grid'"
          :class="[
            'p-2 rounded-lg transition-colors',
            viewMode === 'grid' ? 'bg-primary text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          ]"
        >
          <Grid3X3 class="w-5 h-5" />
        </button>
        <button
          @click="viewMode = 'list'"
          :class="[
            'p-2 rounded-lg transition-colors',
            viewMode === 'list' ? 'bg-primary text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          ]"
        >
          <List class="w-5 h-5" />
        </button>
      </div>
    </div>

    <div class="card">
      <div class="flex flex-col lg:flex-row gap-4">
        <div class="flex-1 relative">
          <Search class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索股票代码或名称..."
            class="form-input pl-10"
            @keyup.enter="handleSearch"
          />
        </div>

        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            <Filter class="w-4 h-4 text-gray-400" />
            <select v-model="selectedIndustry" class="form-input w-32">
              <option v-for="industry in industries" :key="industry.code" :value="industry.code">
                {{ industry.name }}
              </option>
            </select>
            <select v-model="selectedType" class="form-input w-28">
              <option v-for="type in stockTypes" :key="type.value" :value="type.value">
                {{ type.label }}
              </option>
            </select>
          </div>

          <button @click="handleSearch" class="btn-primary flex items-center gap-2">
            <Search class="w-4 h-4" />
            搜索
          </button>
          <button @click="resetFilters" class="btn-secondary">重置</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-12">
      <RefreshCw class="w-8 h-8 text-primary animate-spin" />
    </div>

    <div v-else-if="stocks.length === 0" class="card text-center py-12">
      <p class="text-gray-500">暂无股票数据</p>
    </div>

    <div v-else :class="[
      'grid gap-6',
      viewMode === 'grid' ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' : 'grid-cols-1'
    ]">
      <div
        v-for="stock in stocks"
        :key="stock.code"
        :class="[
          'bg-white rounded-xl border border-gray-200 p-5 hover:shadow-lg hover:border-primary/30 transition-all duration-300 cursor-pointer',
          viewMode === 'list' ? 'flex items-center justify-between' : ''
        ]"
        @click="goToDetail(stock.code)"
      >
        <div :class="viewMode === 'list' ? 'flex items-center gap-4' : ''">
          <div class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
            <span class="text-primary font-bold">{{ stock.name.charAt(0) }}</span>
          </div>
          <div>
            <h3 class="font-bold text-gray-900 hover:text-primary transition-colors">{{ stock.name }}</h3>
            <p class="text-sm text-gray-500">{{ stock.code }}</p>
          </div>
        </div>

        <div :class="['flex items-center gap-4 text-sm text-gray-600', viewMode === 'list' ? 'flex-shrink-0' : 'mt-4']">
          <span>{{ stock.industry_name || '-' }}</span>
          <span :class="[
            'px-2 py-0.5 rounded-full text-xs font-medium',
            stock.type === 'stock' ? 'bg-blue-100 text-blue-600' :
            stock.type === 'index' ? 'bg-purple-100 text-purple-600' :
            'bg-green-100 text-green-600'
          ]">
            {{ stock.type === 'stock' ? '股票' : stock.type === 'index' ? '指数' : '基金' }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="total > pageSize" class="flex items-center justify-between">
      <p class="text-sm text-gray-500">
        显示 {{ (page - 1) * pageSize + 1 }} - {{ Math.min(page * pageSize, total) }} 条，共 {{ total.toLocaleString() }} 条
      </p>
      <div class="flex items-center gap-2">
        <button
          @click="handlePageChange(page - 1)"
          :disabled="page <= 1"
          class="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ChevronLeft class="w-5 h-5" />
        </button>
        <span class="px-3 py-2 bg-gray-100 rounded-lg text-sm font-medium">{{ page }}</span>
        <button
          @click="handlePageChange(page + 1)"
          :disabled="page >= Math.ceil(total / pageSize)"
          class="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ChevronRight class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>