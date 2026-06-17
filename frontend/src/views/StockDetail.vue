<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Building2, TrendingUp, Calendar, DollarSign, BarChart3, PieChart } from 'lucide-vue-next'
import * as echarts from 'echarts'
import { stockApi, financeApi } from '@/utils/api'
import type { StockDetail, KLine, FinanceProfit } from '@/utils/api'

const route = useRoute()
const router = useRouter()

const stock = ref<StockDetail | null>(null)
const klineData = ref<KLine[]>([])
const financeData = ref<FinanceProfit[]>([])
const loading = ref(false)
const klineType = ref<'day' | 'week' | 'month'>('day')
const chartRef = ref<HTMLDivElement | null>(null)
let chartInstance: echarts.ECharts | null = null

const stockCode = computed(() => route.params.code as string)

const fetchStockDetail = async () => {
  loading.value = true
  try {
    const [stockRes, klineRes, financeRes] = await Promise.all([
      stockApi.getDetail(stockCode.value),
      stockApi.getKlineDay(stockCode.value, { limit: 60 }),
      financeApi.getProfit(stockCode.value, { limit: 8 }),
    ])
    stock.value = stockRes.data
    klineData.value = klineRes.data
    financeData.value = financeRes.data
  } catch (e) {
    console.error('Failed to fetch stock detail:', e)
  } finally {
    loading.value = false
  }
}

const fetchKline = async (type: 'day' | 'week' | 'month') => {
  try {
    let res
    switch (type) {
      case 'day':
        res = await stockApi.getKlineDay(stockCode.value, { limit: 60 })
        break
      case 'week':
        res = await stockApi.getKlineWeek(stockCode.value, { limit: 52 })
        break
      case 'month':
        res = await stockApi.getKlineMonth(stockCode.value, { limit: 36 })
        break
    }
    klineData.value = res.data
  } catch (e) {
    console.error('Failed to fetch kline data:', e)
  }
}

const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chartInstance || klineData.value.length === 0) return

  const dates = klineData.value.map(item => item.date)
  const values = klineData.value.map(item => [item.open, item.close, item.low, item.high])
  const volumes = klineData.value.map(item => item.volume)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      formatter: (params: any) => {
        const data = params[0]
        if (!data) return ''
        const values = data.data
        return 
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 8px;"></div>
            <div>开盘: <span style="color: "></span></div>
            <div>收盘: <span style="color: "></span></div>
            <div>最低: <span style="color: #10b981"></span></div>
            <div>最高: <span style="color: #ef4444"></span></div>
          </div>
        
      }
    },
    grid: [
      { left: '10%', right: '5%', top: '5%', height: '55%' },
      { left: '10%', right: '5%', top: '70%', height: '20%' }
    ],
    xAxis: [
      { type: 'category', data: dates, axisLine: { lineStyle: { color: '#d1d5db' } } },
      { type: 'category', data: dates, gridIndex: 1, axisLine: { lineStyle: { color: '#d1d5db' } } }
    ],
    yAxis: [
      { type: 'value', scale: true, axisLine: { lineStyle: { color: '#d1d5db' } } },
      { type: 'value', scale: true, gridIndex: 1, axisLine: { lineStyle: { color: '#d1d5db' } } }
    ],
    dataZoom: [
      { type: 'inside', xAxisIndex: [0, 1], start: 50, end: 100 },
      { show: true, xAxisIndex: [0, 1], start: 50, end: 100 }
    ],
    series: [
      {
        type: 'candlestick',
        data: values,
        itemStyle: {
          color: '#ef4444',
          color0: '#10b981',
          borderColor: '#ef4444',
          borderColor0: '#10b981'
        }
      },
      {
        type: 'bar',
        data: volumes,
        xAxisIndex: 1,
        yAxisIndex: 1,
        itemStyle: {
          color: (params: any) => {
            const idx = params.dataIndex
            const kline = values[idx]
            return kline[1] >= kline[0] ? '#ef4444' : '#10b981'
          }
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

watch(klineData, () => {
  updateChart()
}, { deep: true })

watch(klineType, (newType) => {
  fetchKline(newType)
})

onMounted(() => {
  fetchStockDetail()
  setTimeout(() => {
    initChart()
  }, 100)

  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center gap-4">
      <button @click="router.back()" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <ArrowLeft class="w-5 h-5" />
      </button>
      <div>
        <h1 class="text-2xl font-bold text-gray-900">{{ stock?.name || '-' }}</h1>
        <p class="text-gray-500">{{ stock?.code || '-' }} · {{ stock?.industry_name || '-' }}</p>
      </div>
    </div>

    <div v-if="loading" class="card flex justify-center py-12">
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
        <span class="text-gray-500">加载中...</span>
      </div>
    </div>

    <div v-else-if="stock" class="space-y-6">
      <div class="card">
        <div class="flex items-center gap-4 mb-4">
          <button
            v-for="type in [{ key: 'day', label: '日线' }, { key: 'week', label: '周线' }, { key: 'month', label: '月线' }]"
            :key="type.key"
            @click="klineType = type.key as 'day' | 'week' | 'month'"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              klineType === type.key ? 'bg-primary text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            {{ type.label }}
          </button>
        </div>
        <div ref="chartRef" class="w-full h-80"></div>
      </div>

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="card flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">最新价格</p>
            <p class="text-xl font-bold text-gray-900">{{ klineData[klineData.length - 1]?.close?.toFixed(2) || '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <DollarSign class="w-5 h-5 text-blue-600" />
          </div>
        </div>
        <div class="card flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">涨跌幅</p>
            <p :class="[
              'text-xl font-bold',
              (klineData[klineData.length - 1]?.pct_chg || 0) >= 0 ? 'text-red-500' : 'text-green-500'
            ]">
              {{ (klineData[klineData.length - 1]?.pct_chg || 0).toFixed(2) }}%
            </p>
          </div>
          <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
            <TrendingUp class="w-5 h-5 text-red-600" />
          </div>
        </div>
        <div class="card flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">市盈率</p>
            <p class="text-xl font-bold text-gray-900">{{ klineData[klineData.length - 1]?.pe_ttm?.toFixed(2) || '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
            <BarChart3 class="w-5 h-5 text-purple-600" />
          </div>
        </div>
        <div class="card flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">市净率</p>
            <p class="text-xl font-bold text-gray-900">{{ klineData[klineData.length - 1]?.pb_mrq?.toFixed(2) || '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <PieChart class="w-5 h-5 text-green-600" />
          </div>
        </div>
      </div>

      <div class="card">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">股票信息</h2>
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <p class="text-sm text-gray-500">交易所</p>
            <p class="font-medium text-gray-900">{{ stock.exchange || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">股票类型</p>
            <p :class="[
              'font-medium',
              stock.type === 'stock' ? 'text-blue-600' : stock.type === 'index' ? 'text-purple-600' : 'text-green-600'
            ]">
              {{ stock.type === 'stock' ? '股票' : stock.type === 'index' ? '指数' : '基金' }}
            </p>
          </div>
          <div>
            <p class="text-sm text-gray-500">行业</p>
            <p class="font-medium text-gray-900 flex items-center gap-1">
              <Building2 class="w-4 h-4 text-gray-400" />
              {{ stock.industry_name || '-' }}
            </p>
          </div>
          <div>
            <p class="text-sm text-gray-500">更新时间</p>
            <p class="font-medium text-gray-900 flex items-center gap-1">
              <Calendar class="w-4 h-4 text-gray-400" />
              {{ stock.updated_at?.split('T')[0] || '-' }}
            </p>
          </div>
        </div>
      </div>

      <div class="card">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">财务数据</h2>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">报告期</th>
                <th class="text-right py-3 px-4 text-sm font-medium text-gray-500">ROE</th>
                <th class="text-right py-3 px-4 text-sm font-medium text-gray-500">ROA</th>
                <th class="text-right py-3 px-4 text-sm font-medium text-gray-500">毛利率</th>
                <th class="text-right py-3 px-4 text-sm font-medium text-gray-500">净利率</th>
                <th class="text-right py-3 px-4 text-sm font-medium text-gray-500">EPS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in financeData" :key="item.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4 text-sm font-medium text-gray-900">
                  {{ item.year }}年Q{{ item.quarter }}
                </td>
                <td class="text-right py-3 px-4 text-sm text-gray-600">{{ item.roe?.toFixed(2) || '-' }}</td>
                <td class="text-right py-3 px-4 text-sm text-gray-600">{{ item.roa?.toFixed(2) || '-' }}</td>
                <td class="text-right py-3 px-4 text-sm text-gray-600">{{ item.gross_profit_rate?.toFixed(2) || '-' }}</td>
                <td class="text-right py-3 px-4 text-sm text-gray-600">{{ item.net_profit_rate?.toFixed(2) || '-' }}</td>
                <td class="text-right py-3 px-4 text-sm text-gray-600">{{ item.eps?.toFixed(2) || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>