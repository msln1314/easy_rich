<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { ElEmpty } from 'element-plus'
import * as echarts from 'echarts'
import type { SectorTrendData } from '@/api/stock/sector'

interface Props {
  data: SectorTrendData[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

const processedData = computed(() => {
  if (!props.data || props.data.length === 0) return null

  const dates = props.data.map((item) => item.date)
  const sectorNames = new Set<string>()

  props.data.forEach((item) => {
    Object.keys(item.sectors).forEach((sector) => {
      sectorNames.add(sector)
    })
  })

  const sectors = Array.from(sectorNames).slice(0, 8)

  const inflowSeries = sectors.map((sector) => {
    const values = props.data.map((item) => item.sectors[sector]?.inflow || 0)
    return {
      name: `${sector}流入`,
      type: 'line',
      smooth: true,
      data: values
    }
  })

  const outflowSeries = sectors.map((sector) => {
    const values = props.data.map((item) => item.sectors[sector]?.outflow || 0)
    return {
      name: `${sector}流出`,
      type: 'line',
      smooth: true,
      data: values
    }
  })

  return {
    dates,
    series: [...inflowSeries, ...outflowSeries],
    sectors
  }
})

const initChart = () => {
  if (!chartRef.value) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  if (!processedData.value) return

  const option = {
    title: {
      text: '板块资金流向趋势',
      left: 'center',
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        let result = `${params[0].axisValue}<br/>`
        params.forEach((param: any) => {
          const isPositive = param.value > 0
          const color = isPositive ? '#c23531' : '#2f4554'
          result += `<span style="color:${color}">${param.seriesName}: ${param.value.toFixed(
            2
          )}万</span><br/>`
        })
        return result
      }
    },
    legend: {
      type: 'scroll',
      orient: 'horizontal',
      bottom: 0,
      itemWidth: 10,
      itemHeight: 8,
      textStyle: {
        fontSize: 10
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: processedData.value.dates,
      axisLabel: {
        fontSize: 10,
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        fontSize: 10,
        formatter: (value: number) => {
          if (Math.abs(value) >= 10000) {
            return (value / 10000).toFixed(1) + '亿'
          }
          return value.toFixed(0) + '万'
        }
      },
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: processedData.value.series.map((series, index) => ({
      ...series,
      symbol: 'circle',
      symbolSize: 4,
      lineStyle: {
        width: 2,
        color: index < processedData.value.sectors.length ? '#c23531' : '#2f4554'
      },
      itemStyle: {
        color: index < processedData.value.sectors.length ? '#c23531' : '#2f4554'
      }
    }))
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
  <div class="sector-trend">
    <div v-if="!loading && !processedData" class="flex items-center justify-center h-full">
      <ElEmpty description="暂无趋势数据" :image-size="80" />
    </div>

    <div v-else ref="chartRef" class="chart-container" v-loading="loading"></div>
  </div>
</template>

<style scoped>
.sector-trend {
  height: 100%;
  width: 100%;
}

.chart-container {
  height: 400px;
  width: 100%;
}
</style>
