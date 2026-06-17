import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = Bearer 
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export interface User {
  id: string
  username: string
  role: string
  created_at: string
  updated_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface Stock {
  code: string
  name: string
  industry_code: string | null
  exchange: string | null
  type: string
  created_at: string
  updated_at: string
}

export interface StockDetail extends Stock {
  industry_name: string | null
}

export interface KLine {
  id: number
  stock_code: string
  date: string
  open: number
  close: number
  high: number
  low: number
  volume: number
  amount: number | null
  pct_chg: number | null
  pe_ttm: number | null
  pb_mrq: number | null
  is_st: boolean
  created_at: string
}

export interface PagedResult<T> {
  data: T[]
  total: number
  page: number
  page_size: number
}

export interface FinanceProfit {
  id: number
  stock_code: string
  year: number
  quarter: number
  roe: number | null
  roa: number | null
  gross_profit_rate: number | null
  net_profit_rate: number | null
  eps: number | null
  total_share: number | null
  liqa_share: number | null
  created_at: string
}

export interface FinanceSummary {
  profit: FinanceProfit | null
  operation: any | null
  growth: any | null
  balance: any | null
  cashflow: any | null
  dupont: any | null
}

export interface Task {
  id: string
  name: string
  api_name: string
  config_schema: object
  created_at: string
  updated_at: string
}

export interface TaskExecution {
  id: string
  task_id: string
  status: string
  progress: number
  completed_count: number
  total_count: number
  current_item: string | null
  start_time: string
  end_time: string | null
  error_message: string | null
  result: object | null
  progress_data: object | null
}

export interface Message {
  id: string
  user_id: string
  title: string
  content: string
  type: string
  related_task_id: string | null
  status: string
  created_at: string
}

export interface Industry {
  code: string
  name: string
  parent_code: string | null
  created_at: string
}

export interface StockIndex {
  code: string
  name: string
  type: string
  created_at: string
}

export const authApi = {
  register: (data: { username: string; password: string }) =>
    api.post<User>('/auth/register', data),
  login: (data: { username: string; password: string }) =>
    api.post<LoginResponse>('/auth/login', data),
  getMe: (token: string) =>
    api.get<User>('/auth/me', { params: { token } }),
}

export const stockApi = {
  list: (params?: { industry_code?: string; type?: string; keyword?: string; page?: number; page_size?: number }) =>
    api.get<PagedResult<Stock>>('/stocks', { params }),
  get: (code: string) => api.get<Stock>(/stocks/),
  getDetail: (code: string) => api.get<StockDetail>(/stocks//detail),
  getKlineDay: (code: string, params?: { start_date?: string; end_date?: string; limit?: number }) =>
    api.get<KLine[]>(/stocks//kline/day, { params }),
  getKlineWeek: (code: string, params?: { start_date?: string; end_date?: string; limit?: number }) =>
    api.get<KLine[]>(/stocks//kline/week, { params }),
  getKlineMonth: (code: string, params?: { start_date?: string; end_date?: string; limit?: number }) =>
    api.get<KLine[]>(/stocks//kline/month, { params }),
}

export const financeApi = {
  getSummary: (stock_code: string, params: { year: number; quarter: number }) =>
    api.get<FinanceSummary>(/finance//summary, { params }),
  getProfit: (stock_code: string, params?: { limit?: number }) =>
    api.get<FinanceProfit[]>(/finance//profit, { params }),
  getForecast: (stock_code: string, params?: { limit?: number }) =>
    api.get<any[]>(/finance//report/forecast, { params }),
  getExpress: (stock_code: string, params?: { limit?: number }) =>
    api.get<any[]>(/finance//report/express, { params }),
  getDividend: (stock_code: string, params?: { limit?: number }) =>
    api.get<any[]>(/finance//dividend, { params }),
}

export const industryApi = {
  list: () => api.get<Industry[]>('/stocks/industries/list'),
  listIndexes: () => api.get<StockIndex[]>('/stocks/indexes/list'),
  getConstituents: (index_code: string) => api.get<any[]>(/stocks/indexes//constituents),
}

export const taskApi = {
  list: () => api.get<Task[]>('/tasks'),
  create: (data: { name: string; api_name: string; config_schema: object }) =>
    api.post<Task>('/tasks', data),
  get: (id: string) => api.get<Task>(/tasks/),
  update: (id: string, data: { name: string; api_name: string; config_schema: object }) =>
    api.put<Task>(/tasks/, data),
  delete: (id: string) => api.delete(/tasks/),
  listExecutions: (params?: { task_id?: string; limit?: number }) =>
    api.get<TaskExecution[]>('/tasks/executions', { params }),
  updateExecution: (id: string, data: Partial<TaskExecution>) =>
    api.put<TaskExecution>(/tasks/executions/, data),
  listSchedulers: () => api.get<any[]>('/tasks/schedulers'),
  listMessages: (params: { user_id: string; status?: string; limit?: number }) =>
    api.get<Message[]>('/tasks/messages', { params }),
  updateMessageStatus: (id: string, status: string) =>
    api.put(/tasks/messages//status, { status }),
}

export default api