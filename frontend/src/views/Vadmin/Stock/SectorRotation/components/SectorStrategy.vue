<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import {
  ElSelect,
  ElOption,
  ElButton,
  ElCard,
  ElEmpty,
  ElTable,
  ElTableColumn,
  ElTag,
  ElProgress,
  ElDatePicker
} from 'element-plus'
import { getSectorRotationHistoryApi, getSectorFactorsApi } from '@/api/stock/sector'
import * as echarts from 'echarts'
import dayjs from 'dayjs'

interface Props {
  sectorType?: string
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  sectorType: 'industry',
  loading: false
})

const emit = defineEmits(['refresh'])

const factorData = ref<any[]>([])
const historyData = ref<any[]>([])
const selectedSector = ref('')
const sectorOptions = ref<{ label: string; value: string }[]>([])
const internalLoading = ref(false)
const dateRange = ref<[string, string]>([
  dayjs().subtract(30, 'day').format('YYYY-MM-DD'),
  dayjs().format('YYYY-MM-DD')
])

const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

const fetchData = async () => {
  try {
    internalLoading.value = true
    const [factorsRes] = await Promise.all([getSectorFactorsApi(props.sectorType, 30)])
    factorData.value = factorsRes.data || []

    const uniqueSectors = new Map<string, string>()
    factorData.value.forEach((item) => {
      if (!uniqueSectors.has(item.sector_code)) {
        uniqueSectors.set(item.sector_code, item.sector_name)
      }
    })
    sectorOptions.value = Array.from(uniqueSectors.entries()).map(([code, name]) => ({
      label: name,
      value: code
    }))

    if (sectorOptions.value.length > 0 && !selectedSector.value) {
      selectedSector.value = sectorOptions.value[0].value
      await fetchHistoryData()
    }
  } catch (error) {
    console.error('获取板块因子数据失败:', error)
  } finally {
    internalLoading.value = false
  }
}

const fetchHistoryData = async () => {
  if (!selectedSector.value) return

  try {
    const res = await getSectorRotationHistoryApi(
      selectedSector.value,
      props.sectorType,
      dateRange.value[0]?.replace(/-/g, ''),
      dateRange.value[1]?.replace(/-/g, '')
    )
    historyData.value = res.data || []
    initChart()
  } catch (error) {
    console.error('获取板块历史数据失败:', error)
  }
}

const initChart = () => {
  if (!chartRef.value || historyData.value.length === 0) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  const dates = historyData.value.map((item) => item.date)
  const closes = historyData.value.map((item) => item.close)
  const volumes = historyData.value.map((item) => item.amount)

  const option = {
    title: {
      text: '板块走势',
      left: 'center',
      textStyle: { fontSize: 14, fontWeight: 'normal' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['价格', '成交额'],
      bottom: 0
    },
    grid: [
      { left: '10%', right: '8%', height: '50%' },
      { left: '10%', right: '8%', top: '70%', height: '20%' }
    ],
    xAxis: [
      { type: 'category', data: dates, gridIndex: 0, boundaryGap: false },
      { type: 'category', data: dates, gridIndex: 1, axisLabel: { show: false } }
    ],
    yAxis: [
      {
        type: 'value',
        name: '价格',
        gridIndex: 0,
        splitLine: { show: true, lineStyle: { type: 'dashed' } }
      },
      { type: 'value', name: '成交额', gridIndex: 1, splitLine: { show: false } }
    ],
    series: [
      {
        name: '价格',
        type: 'line',
        data: closes,
        smooth: true,
        symbol: 'none',
        lineStyle: { width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
            { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
          ])
        }
      },
      {
        name: '成交额',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumes,
        itemStyle: { color: '#91cc75' }
      }
    ]
  }

  chartInstance.setOption(option)
}

const getFactorColor = (score: number) => {
  if (score >= 70) return '#67c23a'
  if (score >= 50) return '#409eff'
  if (score >= 30) return '#e6a23c'
  return '#f56c6c'
}

const handleRefresh = () => {
  fetchData()
  emit('refresh')
}

watch(selectedSector, () => {
  fetchHistoryData()
})

watch(
  () => props.sectorType,
  () => {
    selectedSector.value = ''
    fetchData()
  }
)

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="sector-strategy">
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center gap-4">
        <span class="text-gray-500 text-sm">板块因子分析</span>
        <ElSelect v-model="selectedSector" placeholder="选择板块" size="small" class="w-40">
          <ElOption
            v-for="opt in sectorOptions"
            :key="opt.value"
            :label="opt.label"
            :value="opt.value"
          />
        </ElSelect>
        <ElDatePicker
          v-model="dateRange"
          type="daterange"
          size="small"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="fetchHistoryData"
        />
      </div>
      <ElButton size="small" @click="handleRefresh" :loading="internalLoading">刷新</ElButton>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div class="lg:col-span-2">
        <ElCard>
          <template #header>
            <span class="font-semibold">板块走势图</span>
          </template>
          <div v-if="historyData.length > 0" ref="chartRef" class="h-[300px]"></div>
          <ElEmpty v-else description="选择板块查看走势" :image-size="80" />
        </ElCard>
      </div>

      <div>
        <ElCard class="h-full">
          <template #header>
            <span class="font-semibold">多因子评分</span>
          </template>
          <div v-if="selectedSector" class="space-y-4">
            <div
              v-for="item in factorData.filter((f) => f.sector_code === selectedSector).slice(0, 1)"
              :key="item.sector_code"
            >
              <div class="mb-3">
                <div class="flex justify-between text-sm mb-1">
                  <span>资金流因子</span>
                  <span :style="{ color: getFactorColor(item.fund_flow_score) }">{{
                    item.fund_flow_score?.toFixed(0)
                  }}</span>
                </div>
                <ElProgress
                  :percentage="item.fund_flow_score"
                  :show-text="false"
                  :color="getFactorColor(item.fund_flow_score)"
                  :stroke-width="8"
                />
              </div>
              <div class="mb-3">
                <div class="flex justify-between text-sm mb-1">
                  <span>情绪因子</span>
                  <span :style="{ color: getFactorColor(item.sentiment_score) }">{{
                    item.sentiment_score?.toFixed(0)
                  }}</span>
                </div>
                <ElProgress
                  :percentage="item.sentiment_score"
                  :show-text="false"
                  :color="getFactorColor(item.sentiment_score)"
                  :stroke-width="8"
                />
              </div>
              <div class="mb-3">
                <div class="flex justify-between text-sm mb-1">
                  <span>技术因子</span>
                  <span :style="{ color: getFactorColor(item.technical_score) }">{{
                    item.technical_score?.toFixed(0)
                  }}</span>
                </div>
                <ElProgress
                  :percentage="item.technical_score"
                  :show-text="false"
                  :color="getFactorColor(item.technical_score)"
                  :stroke-width="8"
                />
              </div>
              <div class="mb-3">
                <div class="flex justify-between text-sm mb-1">
                  <span>模式因子</span>
                  <span :style="{ color: getFactorColor(item.pattern_score) }">{{
                    item.pattern_score?.toFixed(0)
                  }}</span>
                </div>
                <ElProgress
                  :percentage="item.pattern_score"
                  :show-text="false"
                  :color="getFactorColor(item.pattern_score)"
                  :stroke-width="8"
                />
              </div>
              <div class="pt-3 border-t">
                <div class="flex justify-between text-sm mb-1">
                  <span class="font-semibold">综合评分</span>
                  <span
                    class="font-bold text-lg"
                    :style="{ color: getFactorColor(item.total_score) }"
                    >{{ item.total_score?.toFixed(0) }}</span
                  >
                </div>
                <ElProgress
                  :percentage="item.total_score"
                  :show-text="false"
                  :color="getFactorColor(item.total_score)"
                  :stroke-width="12"
                />
              </div>
            </div>
            <ElEmpty
              v-if="factorData.filter((f) => f.sector_code === selectedSector).length === 0"
              description="暂无因子数据"
              :image-size="60"
            />
          </div>
          <ElEmpty v-else description="请选择板块" :image-size="80" />
        </ElCard>
      </div>
    </div>

    <ElCard class="mt-4">
      <template #header>
        <span class="font-semibold">板块因子排行</span>
      </template>
      <ElTable :data="factorData" :loading="internalLoading" height="200" stripe size="small">
        <ElTableColumn type="index" label="排名" width="60" align="center" />
        <ElTableColumn prop="sector_name" label="板块" min-width="100" />
        <ElTableColumn label="资金流" width="80" align="center">
          <template #default="{ row }">
            <span :style="{ color: getFactorColor(row.fund_flow_score) }">{{
              row.fund_flow_score?.toFixed(0)
            }}</span>
          </template>
        </ElTableColumn>
        <ElTableColumn label="情绪" width="80" align="center">
          <template #default="{ row }">
            <span :style="{ color: getFactorColor(row.sentiment_score) }">{{
              row.sentiment_score?.toFixed(0)
            }}</span>
          </template>
        </ElTableColumn>
        <ElTableColumn label="技术" width="80" align="center">
          <template #default="{ row }">
            <span :style="{ color: getFactorColor(row.technical_score) }">{{
              row.technical_score?.toFixed(0)
            }}</span>
          </template>
        </ElTableColumn>
        <ElTableColumn label="模式" width="80" align="center">
          <template #default="{ row }">
            <span :style="{ color: getFactorColor(row.pattern_score) }">{{
              row.pattern_score?.toFixed(0)
            }}</span>
          </template>
        </ElTableColumn>
        <ElTableColumn label="综合" width="100" align="center">
          <template #default="{ row }">
            <ElTag
              :type="row.total_score >= 60 ? 'success' : row.total_score >= 40 ? '' : 'warning'"
              size="small"
            >
              {{ row.total_score?.toFixed(0) }}
            </ElTag>
          </template>
        </ElTableColumn>
      </ElTable>
    </ElCard>
  </div>
</template>

<style scoped>
.sector-strategy {
  height: 100%;
  width: 100%;
}
</style>
