import { defineStore } from 'pinia'
import { ref } from 'vue'
import { stockApi, type Stock, type StockDetail, type KLine } from '@/utils/api'

export const useStockStore = defineStore('stock', () => {
  const stocks = ref<Stock[]>([])
  const currentStock = ref<StockDetail | null>(null)
  const klineData = ref<KLine[]>([])
  const loading = ref(false)

  const fetchStocks = async (params?: { industry_code?: string; type?: string; keyword?: string; page?: number; page_size?: number }) => {
    loading.value = true
    try {
      const response = await stockApi.list(params)
      stocks.value = response.data.data
      return response.data
    } finally {
      loading.value = false
    }
  }

  const fetchStockDetail = async (code: string) => {
    loading.value = true
    try {
      const response = await stockApi.getDetail(code)
      currentStock.value = response.data
      return response.data
    } finally {
      loading.value = false
    }
  }

  const fetchKlineDay = async (code: string, params?: { start_date?: string; end_date?: string; limit?: number }) => {
    const response = await stockApi.getKlineDay(code, params)
    klineData.value = response.data
    return response.data
  }

  return {
    stocks,
    currentStock,
    klineData,
    loading,
    fetchStocks,
    fetchStockDetail,
    fetchKlineDay,
  }
})