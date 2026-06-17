import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/stocks',
      name: 'StockList',
      component: () => import('@/views/StockList.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/stocks/:code',
      name: 'StockDetail',
      component: () => import('@/views/StockDetail.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/industries',
      name: 'Industry',
      component: () => import('@/views/Industry.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/tasks',
      name: 'TaskManager',
      component: () => import('@/views/TaskManager.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/messages',
      name: 'Messages',
      component: () => import('@/views/Messages.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated()) {
    return { name: 'Login' }
  }
  if (to.name === 'Login' && authStore.isAuthenticated()) {
    return { name: 'Home' }
  }
})

export default router