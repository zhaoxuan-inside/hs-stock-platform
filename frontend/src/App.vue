<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'
import { RouterView } from 'vue-router'

const authStore = useAuthStore()
</script>

<template>
  <div v-if="authStore.isAuthenticated()" class="flex h-screen bg-gray-50">
    <Sidebar />
    <div class="flex-1 flex flex-col overflow-hidden">
      <Header />
      <main class="flex-1 overflow-y-auto p-6">
        <RouterView />
      </main>
    </div>
  </div>
  <RouterView v-else />
</template>