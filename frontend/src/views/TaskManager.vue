<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Trash2, Edit3, Activity, CheckCircle2, AlertCircle } from 'lucide-vue-next'
import { taskApi } from '@/utils/api'
import type { Task, TaskExecution } from '@/utils/api'

const tasks = ref<Task[]>([])
const executions = ref<TaskExecution[]>([])
const loading = ref(false)
const showAddModal = ref(false)
const showEditModal = ref(false)
const showDetailModal = ref(false)

const newTask = ref({ name: '', api_name: '', config_schema: {} as object })
const editingTask = ref<Task | null>(null)
const selectedExecution = ref<TaskExecution | null>(null)

const fetchTasks = async () => {
  loading.value = true
  try {
    const [tasksRes, executionsRes] = await Promise.all([
      taskApi.list(),
      taskApi.listExecutions({ limit: 20 }),
    ])
    tasks.value = tasksRes.data
    executions.value = executionsRes.data
  } catch (e) {
    console.error('Failed to fetch tasks:', e)
  } finally {
    loading.value = false
  }
}

const handleAddTask = async () => {
  if (!newTask.value.name || !newTask.value.api_name) return
  try {
    await taskApi.create(newTask.value)
    showAddModal.value = false
    newTask.value = { name: '', api_name: '', config_schema: {} }
    fetchTasks()
  } catch (e) {
    console.error('Failed to create task:', e)
  }
}

const handleEditTask = async () => {
  if (!editingTask.value) return
  try {
    await taskApi.update(editingTask.value.id, {
      name: editingTask.value.name,
      api_name: editingTask.value.api_name,
      config_schema: editingTask.value.config_schema,
    })
    showEditModal.value = false
    editingTask.value = null
    fetchTasks()
  } catch (e) {
    console.error('Failed to update task:', e)
  }
}

const handleDeleteTask = async (id: string) => {
  if (!confirm('确定要删除这个任务吗？')) return
  try {
    await taskApi.delete(id)
    fetchTasks()
  } catch (e) {
    console.error('Failed to delete task:', e)
  }
}

const openEditModal = (task: Task) => {
  editingTask.value = { ...task }
  showEditModal.value = true
}

const openDetailModal = (execution: TaskExecution) => {
  selectedExecution.value = execution
  showDetailModal.value = true
}

onMounted(() => { fetchTasks() })
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">任务管理</h1>
        <p class="text-gray-500 mt-1">管理数据采集任务和查看执行状态</p>
      </div>
      <button @click="showAddModal = true" class="btn-primary flex items-center gap-2">
        <Plus class="w-4 h-4" /> 新建任务
      </button>
    </div>

    <div v-if="loading" class="card flex justify-center py-12">
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
        <span class="text-gray-500">加载中...</span>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">任务列表</h2>
        <div class="space-y-3">
          <div v-for="task in tasks" :key="task.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100">
            <div>
              <h3 class="font-medium text-gray-900">{{ task.name }}</h3>
              <p class="text-sm text-gray-500">{{ task.api_name }}</p>
            </div>
            <div class="flex items-center gap-2">
              <button @click="openEditModal(task)" class="p-2 hover:bg-white rounded-lg">
                <Edit3 class="w-4 h-4 text-gray-600" />
              </button>
              <button @click="handleDeleteTask(task.id)" class="p-2 hover:bg-red-50 rounded-lg">
                <Trash2 class="w-4 h-4 text-red-500" />
              </button>
            </div>
          </div>
        </div>
        <div v-if="tasks.length === 0" class="text-center py-8">
          <p class="text-gray-500">暂无任务</p>
        </div>
      </div>

      <div class="card">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">执行记录</h2>
        <div class="space-y-3">
          <div v-for="execution in executions" :key="execution.id" class="p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center justify-between mb-3">
              <span class="font-medium text-gray-900 text-sm">{{ execution.current_item || '任务执行' }}</span>
              <span :class="[
                'text-xs px-2 py-1 rounded-full',
                execution.status === 'completed' ? 'bg-green-100 text-green-600' :
                execution.status === 'running' ? 'bg-blue-100 text-blue-600' :
                'bg-red-100 text-red-600'
              ]">
                {{ execution.status === 'completed' ? '已完成' : execution.status === 'running' ? '执行中' : '失败' }}
              </span>
            </div>
            <div class="flex items-center gap-4 mb-3">
              <div class="flex items-center gap-2 text-sm text-gray-600">
                <Activity class="w-4 h-4" />
                <span>{{ execution.completed_count }}/{{ execution.total_count }}</span>
              </div>
              <button @click="openDetailModal(execution)" class="text-sm text-primary hover:underline">查看详情</button>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div :class="[
                'h-2 rounded-full transition-all',
                execution.status === 'completed' ? 'bg-green-500' :
                execution.status === 'running' ? 'bg-blue-500' : 'bg-red-500'
              ]" :style="{ width: ${execution.progress || 0}% }"></div>
            </div>
          </div>
        </div>
        <div v-if="executions.length === 0" class="text-center py-8">
          <p class="text-gray-500">暂无执行记录</p>
        </div>
      </div>
    </div>

    <div v-if="showAddModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">新建任务</h3>
        <div class="space-y-4">
          <div><label class="form-label">任务名称</label><input v-model="newTask.name" type="text" placeholder="请输入任务名称" class="form-input" /></div>
          <div><label class="form-label">API名称</label><input v-model="newTask.api_name" type="text" placeholder="请输入API名称" class="form-input" /></div>
        </div>
        <div class="flex items-center justify-end gap-3 mt-6">
          <button @click="showAddModal = false" class="btn-secondary">取消</button>
          <button @click="handleAddTask" class="btn-primary">创建</button>
        </div>
      </div>
    </div>

    <div v-if="showEditModal && editingTask" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">编辑任务</h3>
        <div class="space-y-4">
          <div><label class="form-label">任务名称</label><input v-model="editingTask.name" type="text" class="form-input" /></div>
          <div><label class="form-label">API名称</label><input v-model="editingTask.api_name" type="text" class="form-input" /></div>
        </div>
        <div class="flex items-center justify-end gap-3 mt-6">
          <button @click="showEditModal = false" class="btn-secondary">取消</button>
          <button @click="handleEditTask" class="btn-primary">保存</button>
        </div>
      </div>
    </div>

    <div v-if="showDetailModal && selectedExecution" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-lg">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">执行详情</h3>
          <button @click="showDetailModal = false" class="text-gray-400 hover:text-gray-600">×</button>
        </div>
        <div class="space-y-4">
          <div class="flex items-center gap-3">
            <CheckCircle2 v-if="selectedExecution.status === 'completed'" class="w-5 h-5 text-green-500" />
            <Activity v-else-if="selectedExecution.status === 'running'" class="w-5 h-5 text-blue-500" />
            <AlertCircle v-else class="w-5 h-5 text-red-500" />
            <span class="font-medium">{{ selectedExecution.status === 'completed' ? '已完成' : selectedExecution.status === 'running' ? '执行中' : '失败' }}</span>
          </div>
          <div><p class="text-sm text-gray-500">进度</p><p class="font-medium">{{ selectedExecution.completed_count }}/{{ selectedExecution.total_count }}</p></div>
          <div><p class="text-sm text-gray-500">当前处理</p><p class="font-medium">{{ selectedExecution.current_item || '-' }}</p></div>
          <div><p class="text-sm text-gray-500">开始时间</p><p class="font-medium">{{ selectedExecution.start_time }}</p></div>
          <div><p class="text-sm text-gray-500">结束时间</p><p class="font-medium">{{ selectedExecution.end_time || '-' }}</p></div>
          <div v-if="selectedExecution.error_message"><p class="text-sm text-gray-500">错误信息</p><p class="text-red-500">{{ selectedExecution.error_message }}</p></div>
        </div>
        <button @click="showDetailModal = false" class="btn-primary w-full mt-6">关闭</button>
      </div>
    </div>
  </div>
</template>