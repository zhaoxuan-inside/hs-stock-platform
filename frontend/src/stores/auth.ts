import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi, type User, type LoginResponse } from '@/utils/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))

  const isAuthenticated = () => !!token.value

  const login = async (username: string, password: string) => {
    const response = await authApi.login({ username, password })
    token.value = response.data.access_token
    localStorage.setItem('access_token', response.data.access_token)
    return response.data
  }

  const register = async (username: string, password: string) => {
    const response = await authApi.register({ username, password })
    return response.data
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
  }
})