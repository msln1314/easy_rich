<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import {
  ElRow,
  ElCol,
  ElCard,
  ElSelect,
  ElOption,
  ElDatePicker,
  ElButton,
  ElMessage
} from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import SectorRanking from './components/SectorRanking.vue'
import SectorTrend from './components/SectorTrend.vue'
import SectorHeatmap from './components/SectorHeatmap.vue'
import { getSectorRankingApi, getSectorTrendApi, getSectorHeatmapApi } from '@/api/stock/sector'
import dayjs from 'dayjs'

defineOptions({
  name: 'SectorRotation'
})

const loading = ref(false)
const dateRange = ref<[string, string]>([
  dayjs().subtract(30, 'day').format('YYYY-MM-DD'),
  dayjs().format('YYYY-MM-DD')
])
const sectorType = ref('all')

const rankingData = ref([])
const trendData = ref([])
const heatmapData = ref([])

const fetchSectorData = async () => {
  try {
    loading.value = true
    const [startDate, endDate] = dateRange.value || []

    const [rankingRes, trendRes, heatmapRes] = await Promise.all([
      getSectorRankingApi({
        start_date: startDate,
        end_date: endDate,
        sector_type: sectorType.value === 'all' ? undefined : sectorType.value
      }),
      getSectorTrendApi({
        start_date: startDate,
        end_date: endDate,
        sector_type: sectorType.value === 'all' ? undefined : sectorType.value
      }),
      getSectorHeatmapApi({
        start_date: startDate,
        end_date: endDate,
        sector_type: sectorType.value === 'all' ? undefined : sectorType.value
      })
    ])

    rankingData.value = rankingRes.data || []
    trendData.value = trendRes.data || []
    heatmapData.value = heatmapRes.data || []
  } catch (error) {
    console.error('获取板块数据失败:', error)
    ElMessage.error('获取板块数据失败')
  } finally {
    loading.value = false
  }
}

const handleRefresh = () => {
  fetchSectorData()
}

const isDataAvailable = computed(() => {
  return rankingData.value.length > 0 || trendData.value.length > 0 || heatmapData.value.length > 0
})

onMounted(() => {
  fetchSectorData()
})
</script>

<template>
  <ContentWrap>
    <ElRow :gutter="20" class="mb-4">
      <ElCol :span="6">
        <ElDatePicker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          style="width: 100%"
          @change="handleRefresh"
        />
      </ElCol>
      <ElCol :span="4">
        <ElSelect
          v-model="sectorType"
          placeholder="板块类型"
          style="width: 100%"
          @change="handleRefresh"
        >
          <ElOption label="全部板块" value="all" />
          <ElOption label="行业板块" value="industry" />
          <ElOption label="概念板块" value="concept" />
          <ElOption label="地域板块" value="region" />
        </ElSelect>
      </ElCol>
      <ElCol :span="2">
        <ElButton type="primary" :loading="loading" @click="handleRefresh"> 刷新 </ElButton>
      </ElCol>
    </ElRow>

    <ElRow :gutter="20" v-if="isDataAvailable">
      <ElCol :span="8">
        <ElCard class="h-full">
          <template #header>
            <div class="flex justify-between items-center">
              <span class="font-semibold">今日板块排行TOP10</span>
            </div>
          </template>
          <SectorRanking :data="rankingData" :loading="loading" />
        </ElCard>
      </ElCol>

      <ElCol :span="8">
        <ElCard class="h-full">
          <template #header>
            <div class="flex justify-between items-center">
              <span class="font-semibold">板块资金趋势图</span>
            </div>
          </template>
          <SectorTrend :data="trendData" :loading="loading" />
        </ElCard>
      </ElCol>

      <ElCol :span="8">
        <ElCard class="h-full">
          <template #header>
            <div class="flex justify-between items-center">
              <span class="font-semibold">板块热力图</span>
            </div>
          </template>
          <SectorHeatmap :data="heatmapData" :loading="loading" />
        </ElCard>
      </ElCol>
    </ElRow>

    <div v-else-if="!loading" class="text-center py-20 text-gray-500">
      暂无数据，请调整筛选条件后重试
    </div>

    <div v-if="loading" class="text-center py-20">
      <ElButton loading>加载中...</ElButton>
    </div>
  </ContentWrap>
</template>

<style scoped>
.h-full {
  height: calc(100vh - 280px);
  min-height: 500px;
}
</style>
