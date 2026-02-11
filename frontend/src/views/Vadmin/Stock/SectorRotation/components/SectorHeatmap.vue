<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { ElEmpty } from 'element-plus'
import * as echarts from 'echarts'
import type { SectorHeatmapItem } from '@/api/stock/sector'

interface Props {
  data: SectorHeatmapItem[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

const processedData = computed(() => {
  if (!props.data || props.data.length === 0) return null

  const heatmapData = props.data.map((item, index) => {
    const x = index % 10
    const y = Math.floor(index / 10)
    return [
      x,
      y,
      item.change_rate,
      item.sector_name,
      item.sector_code,
      item.volume,
      item.turnover_rate
    ]
  })

  const sectors = props.data.map((item) => item.sector_name)

  return {
    heatmapData,
    sectors
  }
})

const getHeatmapColor = (value: number) => {
  if (value > 7) return '#c23531'
  if (value > 3) return '#d48265'
  if (value > 0) return '#61a0a8'
  if (value > -3) return '#91cc75'
  if (value > -7) return '#fac858'
  return '#ee6666'
}

const initChart = () => {
  if (!chartRef.value) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  if (!processedData.value) return

  const option = {
    title: {
      text: '板块热度分布',
      left: 'center',
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      position: 'top',
      formatter: (params: any) => {
        const [x, y, changeRate, sectorName, sectorCode, volume, turnoverRate] = params.data
        const color = changeRate >= 0 ? '#c23531' : '#2f4554'
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 4px;">${sectorName}</div>
            <div style="color: ${color}; font-size: 12px;">涨跌幅: ${
              changeRate >= 0 ? '+' : ''
            }${changeRate.toFixed(2)}%</div>
            <div style="font-size: 12px;">成交额: ${(volume / 100000000).toFixed(2)}亿</div>
            <div style="font-size: 12px;">换手率: ${turnoverRate.toFixed(2)}%</div>
          </div>
        `
      }
    },
    grid: {
      height: '50%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: Array.from({ length: 10 }, (_, i) => i),
      splitArea: {
        show: true,
        areaStyle: {
          color: ['#f5f5f5', '#fff']
        }
      },
      axisLabel: {
        show: false
      }
    },
    yAxis: {
      type: 'category',
      data: Array.from({ length: 10 }, (_, i) => i),
      splitArea: {
        show: true,
        areaStyle: {
          color: ['#f5f5f5', '#fff']
        }
      },
      axisLabel: {
        show: false
      }
    },
    visualMap: {
      min: -10,
      max: 10,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '5%',
      inRange: {
        color: ['#2f4554', '#61a0a8', '#c23531']
      },
      pieces: [
        { min: 7, max: 10, label: '大涨(>7%)', color: '#c23531' },
        { min: 3, max: 7, label: '上涨(3-7%)', color: '#d48265' },
        { min: 0, max: 3, label: '微涨(0-3%)', color: '#61a0a8' },
        { min: -3, max: 0, label: '微跌(-3-0%)', color: '#91cc75' },
        { min: -7, max: -3, label: '下跌(-7--3%)', color: '#fac858' },
        { min: -10, max: -7, label: '大跌(<-7%)', color: '#ee6666' }
      ]
    },
    series: [
      {
        name: '板块热度',
        type: 'heatmap',
        data: processedData.value.heatmapData,
        label: {
          show: false
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

const resizeChart = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

watch(
  () => props.data,
  () => {
    nextTick(() => {
      initChart()
    })
  },
  { deep: true }
)

watch(
  () => props.loading,
  (loading) => {
    if (!loading && chartRef.value) {
      nextTick(() => {
        initChart()
      })
    }
  }
)

defineExpose({
  resizeChart
})
</script>

<template>
  <div class="sector-heatmap">
    <div v-if="!loading && !processedData" class="flex items-center justify-center h-full">
      <ElEmpty description="暂无热力图数据" :image-size="80" />
    </div>

    <div v-else ref="chartRef" class="chart-container" v-loading="loading"></div>
  </div>
</template>

<style scoped>
.sector-heatmap {
  height: 100%;
  width: 100%;
}

.chart-container {
  height: 400px;
  width: 100%;
}
</style>
