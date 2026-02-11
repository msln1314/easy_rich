<script setup lang="ts">
import { computed } from 'vue'
import { ElTable, ElTableColumn, ElTag, ElProgress, ElEmpty } from 'element-plus'
import type { SectorRankingItem } from '@/api/stock/sector'

interface Props {
  data: SectorRankingItem[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const displayData = computed(() => {
  return props.data.slice(0, 10)
})

const getRankColor = (rank: number) => {
  if (rank === 1) return '#FFD700'
  if (rank === 2) return '#C0C0C0'
  if (rank === 3) return '#CD7F32'
  return '#909399'
}

const getChangeRateType = (rate: number) => {
  if (rate > 0) return 'success'
  if (rate < 0) return 'danger'
  return 'info'
}

const formatNumber = (num: number) => {
  if (num >= 100000000) {
    return (num / 100000000).toFixed(2) + '亿'
  } else if (num >= 10000) {
    return (num / 10000).toFixed(2) + '万'
  }
  return num.toFixed(2)
}

const getProgressColor = (rate: number) => {
  if (rate > 5) return '#67c23a'
  if (rate > 0) return '#409eff'
  if (rate > -5) return '#e6a23c'
  return '#f56c6c'
}
</script>

<template>
  <div class="sector-ranking">
    <ElTable :data="displayData" :loading="loading" height="400" stripe class="w-full">
      <ElTableColumn prop="rank" label="排名" width="60" align="center">
        <template #default="{ row }">
          <div class="font-bold text-lg" :style="{ color: getRankColor(row.rank) }">
            {{ row.rank }}
          </div>
        </template>
      </ElTableColumn>

      <ElTableColumn prop="sector_name" label="板块名称" min-width="100">
        <template #default="{ row }">
          <div class="font-medium truncate" :title="row.sector_name">
            {{ row.sector_name }}
          </div>
        </template>
      </ElTableColumn>

      <ElTableColumn prop="change_rate" label="涨跌幅" width="80" align="right">
        <template #default="{ row }">
          <ElTag :type="getChangeRateType(row.change_rate)" size="small" effect="dark">
            {{ row.change_rate >= 0 ? '+' : '' }}{{ row.change_rate.toFixed(2) }}%
          </ElTag>
        </template>
      </ElTableColumn>

      <ElTableColumn label="涨跌幅" width="80">
        <template #default="{ row }">
          <ElProgress
            :percentage="Math.abs(row.change_rate)"
            :stroke-width="6"
            :show-text="false"
            :color="getProgressColor(row.change_rate)"
          />
        </template>
      </ElTableColumn>

      <ElTableColumn prop="volume" label="成交额" width="80" align="right">
        <template #default="{ row }">
          <div class="text-xs">
            {{ formatNumber(row.volume) }}
          </div>
        </template>
      </ElTableColumn>

      <ElTableColumn prop="turnover_rate" label="换手率" width="70" align="right">
        <template #default="{ row }">
          <div class="text-xs"> {{ row.turnover_rate.toFixed(2) }}% </div>
        </template>
      </ElTableColumn>

      <ElTableColumn prop="stock_count" label="个股数" width="60" align="center">
        <template #default="{ row }">
          <div class="text-xs">
            {{ row.stock_count }}
          </div>
        </template>
      </ElTableColumn>
    </ElTable>

    <ElEmpty v-if="!loading && displayData.length === 0" description="暂无数据" :image-size="100" />
  </div>
</template>

<style scoped>
.sector-ranking {
  height: 100%;
}

:deep(.el-table__body-wrapper) {
  overflow-y: auto;
}

:deep(.el-progress-bar__outer) {
  background-color: #f0f0f0;
}
</style>
