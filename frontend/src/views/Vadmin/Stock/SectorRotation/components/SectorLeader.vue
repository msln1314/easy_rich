<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import {
  ElTable,
  ElTableColumn,
  ElTag,
  ElProgress,
  ElEmpty,
  ElButton,
  ElTooltip
} from 'element-plus'
import { getSectorLeadersApi } from '@/api/stock/sector'
import type { SectorLeader } from '@/api/stock/sector'

interface Props {
  sectorType?: string
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  sectorType: 'industry',
  loading: false
})

const emit = defineEmits(['refresh'])

const tableData = ref<SectorLeader[]>([])
const internalLoading = ref(false)

const fetchData = async () => {
  try {
    internalLoading.value = true
    const res = await getSectorLeadersApi(props.sectorType, 50)
    tableData.value = res.data || []
  } catch (error) {
    console.error('获取板块龙头股失败:', error)
    tableData.value = []
  } finally {
    internalLoading.value = false
  }
}

const getChangeType = (rate: number) => {
  if (rate > 0) return 'success'
  if (rate < 0) return 'danger'
  return 'info'
}

const getActivityLevel = (score: number) => {
  if (score >= 80) return { text: '极高', color: '#f56c6c' }
  if (score >= 60) return { text: '高', color: '#e6a23c' }
  if (score >= 40) return { text: '中', color: '#409eff' }
  if (score >= 20) return { text: '低', color: '#909399' }
  return { text: '极低', color: '#c0c4cc' }
}

const formatAmount = (amount: number) => {
  if (amount >= 100000000) {
    return (amount / 100000000).toFixed(2) + '亿'
  } else if (amount >= 10000) {
    return (amount / 10000).toFixed(2) + '万'
  }
  return amount.toFixed(2)
}

const handleRefresh = () => {
  fetchData()
  emit('refresh')
}

watch(
  () => props.sectorType,
  () => {
    fetchData()
  }
)

onMounted(() => {
  fetchData()
})

defineExpose({ fetchData })
</script>

<template>
  <div class="sector-leader">
    <div class="flex justify-between items-center mb-4">
      <span class="text-gray-500 text-sm">共 {{ tableData.length }} 个板块</span>
      <ElButton size="small" @click="handleRefresh" :loading="internalLoading">刷新</ElButton>
    </div>

    <ElTable
      :data="tableData"
      :loading="loading || internalLoading"
      height="450"
      stripe
      class="w-full"
    >
      <ElTableColumn type="index" label="排名" width="60" align="center" />

      <ElTableColumn prop="sector_name" label="板块名称" min-width="100">
        <template #default="{ row }">
          <div class="font-medium">{{ row.sector_name }}</div>
        </template>
      </ElTableColumn>

      <ElTableColumn label="龙头股" min-width="120">
        <template #default="{ row }">
          <div v-if="row.leader_stock" class="flex flex-col">
            <div class="flex items-center gap-1">
              <span class="font-medium text-blue-600">{{ row.leader_stock.name }}</span>
              <ElTag v-if="row.leader_stock.is_limit_up" type="danger" size="small" effect="dark">
                涨停
              </ElTag>
            </div>
            <div class="text-xs text-gray-500">{{ row.leader_stock.code }}</div>
          </div>
          <span v-else class="text-gray-400">-</span>
        </template>
      </ElTableColumn>

      <ElTableColumn label="龙头涨幅" width="90" align="right">
        <template #default="{ row }">
          <ElTag
            v-if="row.leader_stock"
            :type="getChangeType(row.leader_stock.change_percent)"
            size="small"
            effect="dark"
          >
            {{ row.leader_stock.change_percent >= 0 ? '+' : ''
            }}{{ row.leader_stock.change_percent?.toFixed(2) }}%
          </ElTag>
          <span v-else class="text-gray-400">-</span>
        </template>
      </ElTableColumn>

      <ElTableColumn label="龙头评分" width="100" align="center">
        <template #default="{ row }">
          <div v-if="row.leader_stock" class="flex items-center gap-1">
            <ElProgress
              :percentage="row.leader_stock.score"
              :stroke-width="6"
              :show-text="false"
              :color="
                row.leader_stock.score >= 80
                  ? '#67c23a'
                  : row.leader_stock.score >= 50
                  ? '#409eff'
                  : '#e6a23c'
              "
            />
            <span class="text-xs font-medium">{{ row.leader_stock.score?.toFixed(0) }}</span>
          </div>
          <span v-else class="text-gray-400">-</span>
        </template>
      </ElTableColumn>

      <ElTableColumn label="二龙头" width="80" align="center">
        <template #default="{ row }">
          <ElTooltip
            v-if="row.second_leader"
            :content="`${row.second_leader.name} ${
              row.second_leader.change_percent >= 0 ? '+' : ''
            }${row.second_leader.change_percent?.toFixed(2)}%`"
            placement="top"
          >
            <span class="text-blue-500 cursor-pointer">{{ row.second_leader.name }}</span>
          </ElTooltip>
          <span v-else class="text-gray-400">-</span>
        </template>
      </ElTableColumn>

      <ElTableColumn prop="change_percent" label="板块涨幅" width="90" align="right">
        <template #default="{ row }">
          <ElTag :type="getChangeType(row.change_percent)" size="small">
            {{ row.change_percent >= 0 ? '+' : '' }}{{ row.change_percent?.toFixed(2) }}%
          </ElTag>
        </template>
      </ElTableColumn>

      <ElTableColumn label="涨停/跌停" width="80" align="center">
        <template #default="{ row }">
          <span class="text-red-500">{{ row.limit_up_count }}</span>
          <span class="text-gray-400">/</span>
          <span class="text-green-500">{{ row.limit_down_count }}</span>
        </template>
      </ElTableColumn>

      <ElTableColumn label="活跃度" width="100" align="center">
        <template #default="{ row }">
          <div class="flex items-center justify-center gap-1">
            <span
              class="w-2 h-2 rounded-full"
              :style="{ backgroundColor: getActivityLevel(row.activity_score).color }"
            ></span>
            <span class="text-xs">{{ getActivityLevel(row.activity_score).text }}</span>
            <span class="text-xs text-gray-400">({{ row.activity_score?.toFixed(0) }})</span>
          </div>
        </template>
      </ElTableColumn>

      <ElTableColumn label="成交额" width="80" align="right">
        <template #default="{ row }">
          <span class="text-xs">{{ formatAmount(row.total_amount) }}</span>
        </template>
      </ElTableColumn>
    </ElTable>

    <ElEmpty
      v-if="!loading && !internalLoading && tableData.length === 0"
      description="暂无龙头股数据"
      :image-size="100"
    />
  </div>
</template>

<style scoped>
.sector-leader {
  height: 100%;
  width: 100%;
}

:deep(.el-table__body-wrapper) {
  overflow-y: auto;
}

:deep(.el-progress-bar__outer) {
  background-color: #f0f0f0;
}
</style>
