<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import {
  ElButton,
  ElCard,
  ElEmpty,
  ElTag,
  ElProgress,
  ElTable,
  ElTableColumn,
  ElDescriptions,
  ElDescriptionsItem,
  ElStatistic
} from 'element-plus'
import { predictSectorRotationApi, getSectorFactorsApi } from '@/api/stock/sector'
import * as echarts from 'echarts'

interface Props {
  sectorType?: string
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  sectorType: 'industry',
  loading: false
})

const emit = defineEmits(['refresh'])

const predictionData = ref<any>(null)
const factorData = ref<any[]>([])
const internalLoading = ref(false)

const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

const fetchData = async () => {
  try {
    internalLoading.value = true
    const [predictRes, factorsRes] = await Promise.all([
      predictSectorRotationApi(props.sectorType),
      getSectorFactorsApi(props.sectorType, 20)
    ])
    predictionData.value = predictRes.data || null
    factorData.value = factorsRes.data || []

    if (predictionData.value) {
      await nextTick()
      initChart()
    }
  } catch (error) {
    console.error('获取预测数据失败:', error)
  } finally {
    internalLoading.value = false
  }
}

const initChart = () => {
  if (!chartRef.value || !predictionData.value?.predictions?.length) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  const predictions = predictionData.value.predictions.slice(0, 10).reverse()
  const names = predictions.map((p: any) => p.sector_name)
  const probabilities = predictions.map((p: any) => (p.probability * 100).toFixed(1))
  const confidences = predictions.map((p: any) => (p.confidence * 100).toFixed(1))

  const option = {
    title: {
      text: '下一轮动板块概率预测',
      left: 'center',
      textStyle: { fontSize: 14, fontWeight: 'normal' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params: any) => {
        const data = params[0]
        const idx = predictions.length - 1 - data.dataIndex
        const pred = predictionData.value.predictions[idx]
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 4px;">${pred.sector_name}</div>
            <div style="margin-bottom: 2px;">轮动概率: ${(pred.probability * 100).toFixed(1)}%</div>
            <div style="margin-bottom: 2px;">置信度: ${(pred.confidence * 100).toFixed(1)}%</div>
            <div style="margin-top: 4px; font-size: 12px; color: #909399;">因子得分:</div>
            <div style="font-size: 12px;">资金流: ${
              pred.factors?.fund_flow?.toFixed(0) || '-'
            }</div>
            <div style="font-size: 12px;">情绪: ${pred.factors?.sentiment?.toFixed(0) || '-'}</div>
            <div style="font-size: 12px;">技术: ${pred.factors?.technical?.toFixed(0) || '-'}</div>
            <div style="font-size: 12px;">模式: ${pred.factors?.pattern?.toFixed(0) || '-'}</div>
          </div>
        `
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      max: 100,
      axisLabel: { formatter: '{value}%' }
    },
    yAxis: {
      type: 'category',
      data: names,
      axisLabel: { width: 80, overflow: 'truncate' }
    },
    series: [
      {
        name: '轮动概率',
        type: 'bar',
        data: probabilities,
        itemStyle: {
          color: (params: any) => {
            const value = params.value
            if (value >= 60) return '#67c23a'
            if (value >= 40) return '#409eff'
            if (value >= 20) return '#e6a23c'
            return '#909399'
          }
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}%'
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

const getProbColor = (prob: number) => {
  if (prob >= 0.6) return '#67c23a'
  if (prob >= 0.4) return '#409eff'
  if (prob >= 0.2) return '#e6a23c'
  return '#909399'
}

const getConfidenceLevel = (confidence: number) => {
  const pct = confidence * 100
  if (pct >= 80) return { text: '高', color: '#67c23a' }
  if (pct >= 60) return { text: '中', color: '#409eff' }
  if (pct >= 40) return { text: '低', color: '#e6a23c' }
  return { text: '极低', color: '#f56c6c' }
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
</script>

<template>
  <div class="sector-prediction">
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center gap-4">
        <span class="text-gray-500 text-sm">板块轮动预测</span>
        <ElTag v-if="predictionData" type="info" size="small">
          模型版本: {{ predictionData.model_version }}
        </ElTag>
      </div>
      <ElButton type="primary" size="small" @click="handleRefresh" :loading="internalLoading">
        重新预测
      </ElButton>
    </div>

    <div v-if="predictionData" class="space-y-4">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <ElCard>
          <template #header>
            <span class="font-semibold">预测概览</span>
          </template>
          <div class="space-y-4">
            <div>
              <div class="text-gray-500 text-sm mb-1">预测目标日期</div>
              <div class="text-lg font-semibold">{{ predictionData.target_date }}</div>
            </div>
            <div>
              <div class="text-gray-500 text-sm mb-1">整体置信度</div>
              <div class="flex items-center gap-2">
                <ElProgress
                  :percentage="predictionData.confidence * 100"
                  :stroke-width="10"
                  :color="getConfidenceLevel(predictionData.confidence).color"
                />
                <span :style="{ color: getConfidenceLevel(predictionData.confidence).color }">
                  {{ getConfidenceLevel(predictionData.confidence).text }}
                </span>
              </div>
            </div>
            <div v-if="predictionData.predictions?.length">
              <div class="text-gray-500 text-sm mb-1">最可能轮动板块</div>
              <div class="flex items-center gap-2">
                <ElTag type="success" size="large" effect="dark">
                  {{ predictionData.predictions[0].sector_name }}
                </ElTag>
                <span class="text-sm">
                  概率: {{ (predictionData.predictions[0].probability * 100).toFixed(1) }}%
                </span>
              </div>
            </div>
          </div>
        </ElCard>

        <div class="lg:col-span-2">
          <ElCard class="h-full">
            <template #header>
              <span class="font-semibold">轮动概率分布</span>
            </template>
            <div ref="chartRef" class="h-[280px]"></div>
          </ElCard>
        </div>
      </div>

      <ElCard>
        <template #header>
          <span class="font-semibold">预测详情</span>
        </template>
        <ElTable :data="predictionData.predictions" stripe size="small" max-height="300">
          <ElTableColumn type="index" label="排名" width="60" align="center" />
          <ElTableColumn prop="sector_name" label="板块名称" min-width="100" />
          <ElTableColumn label="轮动概率" width="120" align="center">
            <template #default="{ row }">
              <div class="flex items-center gap-2">
                <ElProgress
                  :percentage="row.probability * 100"
                  :stroke-width="6"
                  :show-text="false"
                  :color="getProbColor(row.probability)"
                />
                <span class="text-sm" :style="{ color: getProbColor(row.probability) }">
                  {{ (row.probability * 100).toFixed(1) }}%
                </span>
              </div>
            </template>
          </ElTableColumn>
          <ElTableColumn label="置信度" width="100" align="center">
            <template #default="{ row }">
              <ElTag
                :type="row.confidence >= 0.7 ? 'success' : row.confidence >= 0.5 ? '' : 'warning'"
                size="small"
              >
                {{ (row.confidence * 100).toFixed(0) }}%
              </ElTag>
            </template>
          </ElTableColumn>
          <ElTableColumn label="资金流" width="80" align="center">
            <template #default="{ row }">
              <span>{{ row.factors?.fund_flow?.toFixed(0) || '-' }}</span>
            </template>
          </ElTableColumn>
          <ElTableColumn label="情绪" width="80" align="center">
            <template #default="{ row }">
              <span>{{ row.factors?.sentiment?.toFixed(0) || '-' }}</span>
            </template>
          </ElTableColumn>
          <ElTableColumn label="技术" width="80" align="center">
            <template #default="{ row }">
              <span>{{ row.factors?.technical?.toFixed(0) || '-' }}</span>
            </template>
          </ElTableColumn>
          <ElTableColumn label="模式" width="80" align="center">
            <template #default="{ row }">
              <span>{{ row.factors?.pattern?.toFixed(0) || '-' }}</span>
            </template>
          </ElTableColumn>
        </ElTable>
      </ElCard>
    </div>

    <ElEmpty v-else-if="!internalLoading" description="点击重新预测生成轮动预测" :image-size="120">
      <ElButton type="primary" @click="handleRefresh">开始预测</ElButton>
    </ElEmpty>

    <div v-if="internalLoading" class="text-center py-20">
      <ElButton loading>预测计算中...</ElButton>
    </div>
  </div>
</template>

<style scoped>
.sector-prediction {
  height: 100%;
  width: 100%;
}
</style>
