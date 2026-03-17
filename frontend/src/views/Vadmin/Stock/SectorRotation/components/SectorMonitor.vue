<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import {
  ElTable,
  ElTableColumn,
  ElTag,
  ElEmpty,
  ElButton,
  ElSwitch,
  ElInputNumber,
  ElSelect,
  ElOption,
  ElDialog,
  ElForm,
  ElFormItem,
  ElMessage
} from 'element-plus'
import { getSectorRealtimeStatusApi } from '@/api/stock/sector'
import type { SectorRealtimeStatus } from '@/api/stock/sector'

interface Props {
  sectorType?: string
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  sectorType: 'industry',
  loading: false
})

const emit = defineEmits(['refresh'])

const realtimeData = ref<SectorRealtimeStatus[]>([])
const internalLoading = ref(false)
const autoRefresh = ref(false)
const refreshInterval = ref(30)
const thresholdUp = ref(3)
const thresholdDown = ref(-3)

let timer: ReturnType<typeof setInterval> | null = null

const alertList = ref<{ sector: SectorRealtimeStatus; type: 'up' | 'down'; time: string }[]>([])

const filteredAlerts = ref<SectorRealtimeStatus[]>([])

const fetchData = async () => {
  try {
    internalLoading.value = true
    const res = await getSectorRealtimeStatusApi(props.sectorType)
    realtimeData.value = res.data || []
    checkAlerts()
  } catch (error) {
    console.error('获取板块实时状态失败:', error)
    realtimeData.value = []
  } finally {
    internalLoading.value = false
  }
}

const checkAlerts = () => {
  realtimeData.value.forEach((sector) => {
    if (sector.change_percent >= thresholdUp.value) {
      const existing = alertList.value.find(
        (a) => a.sector.sector_code === sector.sector_code && a.type === 'up'
      )
      if (!existing) {
        alertList.value.unshift({
          sector,
          type: 'up',
          time: new Date().toLocaleTimeString()
        })
      }
    } else if (sector.change_percent <= thresholdDown.value) {
      const existing = alertList.value.find(
        (a) => a.sector.sector_code === sector.sector_code && a.type === 'down'
      )
      if (!existing) {
        alertList.value.unshift({
          sector,
          type: 'down',
          time: new Date().toLocaleTimeString()
        })
      }
    }
  })
  if (alertList.value.length > 50) {
    alertList.value = alertList.value.slice(0, 50)
  }
}

const getStatusClass = (changePercent: number) => {
  if (changePercent >= thresholdUp.value) return 'alert-up'
  if (changePercent <= thresholdDown.value) return 'alert-down'
  return ''
}

const getChangeType = (rate: number) => {
  if (rate > 0) return 'success'
  if (rate < 0) return 'danger'
  return 'info'
}

const handleRefresh = () => {
  fetchData()
  emit('refresh')
}

const clearAlerts = () => {
  alertList.value = []
  ElMessage.success('告警记录已清除')
}

const toggleAutoRefresh = (val: boolean) => {
  if (val) {
    timer = setInterval(fetchData, refreshInterval.value * 1000)
    ElMessage.success(`已开启自动刷新，间隔 ${refreshInterval.value} 秒`)
  } else {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
    ElMessage.info('已关闭自动刷新')
  }
}

const monitorSectors = ref<string[]>([])
const showAddMonitor = ref(false)
const selectedSector = ref('')

const addMonitor = () => {
  if (selectedSector.value && !monitorSectors.value.includes(selectedSector.value)) {
    monitorSectors.value.push(selectedSector.value)
    ElMessage.success(`已添加 ${selectedSector.value} 到监控`)
  }
  showAddMonitor.value = false
}

const removeMonitor = (sector: string) => {
  monitorSectors.value = monitorSectors.value.filter((s) => s !== sector)
}

onMounted(() => {
  fetchData()
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<template>
  <div class="sector-monitor">
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center gap-4">
        <span class="text-gray-500 text-sm">监控 {{ realtimeData.length }} 个板块</span>
        <div class="flex items-center gap-2">
          <span class="text-sm text-gray-500">自动刷新</span>
          <ElSwitch v-model="autoRefresh" @change="toggleAutoRefresh" />
          <ElInputNumber
            v-if="autoRefresh"
            v-model="refreshInterval"
            :min="5"
            :max="300"
            :step="5"
            size="small"
            class="w-20"
          />
          <span v-if="autoRefresh" class="text-xs text-gray-400">秒</span>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <ElButton size="small" @click="handleRefresh" :loading="internalLoading">刷新</ElButton>
        <ElButton size="small" type="danger" plain @click="clearAlerts">清除告警</ElButton>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div class="border rounded-lg p-4">
        <div class="flex justify-between items-center mb-3">
          <span class="font-semibold text-gray-700">实时监控状态</span>
          <div class="flex items-center gap-2 text-sm">
            <span class="text-gray-500">上涨阈值:</span>
            <ElInputNumber
              v-model="thresholdUp"
              :min="0"
              :max="10"
              :step="0.5"
              size="small"
              class="w-20"
            />
            <span class="text-gray-500">下跌阈值:</span>
            <ElInputNumber
              v-model="thresholdDown"
              :min="-10"
              :max="0"
              :step="0.5"
              size="small"
              class="w-20"
            />
          </div>
        </div>
        <ElTable
          :data="realtimeData.slice(0, 20)"
          :loading="loading || internalLoading"
          height="350"
          stripe
          size="small"
          :row-class-name="({ row }) => getStatusClass(row.change_percent)"
        >
          <ElTableColumn prop="sector_name" label="板块" min-width="100">
            <template #default="{ row }">
              <div class="flex items-center gap-1">
                <span
                  class="w-2 h-2 rounded-full"
                  :class="
                    row.change_percent >= thresholdUp
                      ? 'bg-red-500'
                      : row.change_percent <= thresholdDown
                      ? 'bg-green-500'
                      : 'bg-gray-400'
                  "
                ></span>
                <span>{{ row.sector_name }}</span>
              </div>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="change_percent" label="涨跌幅" width="90" align="right">
            <template #default="{ row }">
              <ElTag :type="getChangeType(row.change_percent)" size="small">
                {{ row.change_percent >= 0 ? '+' : '' }}{{ row.change_percent?.toFixed(2) }}%
              </ElTag>
            </template>
          </ElTableColumn>
          <ElTableColumn label="领涨股" min-width="100">
            <template #default="{ row }">
              <div v-if="row.leading_stock" class="flex items-center gap-1">
                <span class="text-blue-600">{{ row.leading_stock }}</span>
                <span
                  :class="row.leading_stock_change_percent >= 0 ? 'text-red-500' : 'text-green-500'"
                  class="text-xs"
                >
                  {{ row.leading_stock_change_percent >= 0 ? '+' : ''
                  }}{{ row.leading_stock_change_percent?.toFixed(2) }}%
                </span>
              </div>
              <span v-else class="text-gray-400">-</span>
            </template>
          </ElTableColumn>
          <ElTableColumn label="涨/跌" width="70" align="center">
            <template #default="{ row }">
              <span class="text-red-500">{{ row.up_count }}</span>
              <span class="text-gray-400">/</span>
              <span class="text-green-500">{{ row.down_count }}</span>
            </template>
          </ElTableColumn>
        </ElTable>
      </div>

      <div class="border rounded-lg p-4">
        <div class="flex justify-between items-center mb-3">
          <span class="font-semibold text-gray-700">告警记录</span>
          <span class="text-xs text-gray-400">最近 {{ alertList.length }} 条</span>
        </div>
        <div class="alert-list h-[350px] overflow-y-auto">
          <div
            v-if="alertList.length === 0"
            class="flex items-center justify-center h-full text-gray-400"
          >
            暂无告警记录
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="(alert, index) in alertList"
              :key="index"
              class="flex items-center justify-between p-2 rounded"
              :class="alert.type === 'up' ? 'bg-red-50' : 'bg-green-50'"
            >
              <div class="flex items-center gap-2">
                <span
                  class="w-6 h-6 rounded-full flex items-center justify-center text-white text-xs"
                  :class="alert.type === 'up' ? 'bg-red-500' : 'bg-green-500'"
                >
                  {{ alert.type === 'up' ? '↑' : '↓' }}
                </span>
                <div>
                  <div class="font-medium">{{ alert.sector.sector_name }}</div>
                  <div class="text-xs text-gray-500">
                    {{ alert.type === 'up' ? '上涨超过' : '下跌超过' }}
                    {{ alert.type === 'up' ? thresholdUp : Math.abs(thresholdDown) }}%
                  </div>
                </div>
              </div>
              <div class="text-right">
                <div
                  :class="alert.sector.change_percent >= 0 ? 'text-red-500' : 'text-green-500'"
                  class="font-medium"
                >
                  {{ alert.sector.change_percent >= 0 ? '+' : ''
                  }}{{ alert.sector.change_percent?.toFixed(2) }}%
                </div>
                <div class="text-xs text-gray-400">{{ alert.time }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <ElEmpty
      v-if="!loading && !internalLoading && realtimeData.length === 0"
      description="暂无监控数据"
      :image-size="100"
    />
  </div>
</template>

<style scoped>
.sector-monitor {
  height: 100%;
  width: 100%;
}

.alert-up {
  background-color: #fef0f0;
}

.alert-down {
  background-color: #f0f9eb;
}

.alert-list {
  scrollbar-width: thin;
}

.alert-list::-webkit-scrollbar {
  width: 6px;
}

.alert-list::-webkit-scrollbar-thumb {
  background-color: #dcdfe6;
  border-radius: 3px;
}
</style>
