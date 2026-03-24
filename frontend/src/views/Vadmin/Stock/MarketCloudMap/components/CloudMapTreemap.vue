<template>
  <div ref="chartRef" class="treemap-chart"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import type { CloudMapIndustry, CloudMapStock } from '/@/api/stock/stockIndex'

const props = defineProps<{
  data: CloudMapIndustry[]
  metric: string
}>()

const emit = defineEmits<{
  (e: 'stock-click', stock: CloudMapStock): void
}>()

const chartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null

function getMetricValue(stock: CloudMapStock): number {
  switch (props.metric) {
    case 'pe':
      return stock.pe || 0
    case 'pb':
      return stock.pb || 0
    case 'amount':
      return stock.amount
    default:
      return stock.change
  }
}

function getMetricLabel(): string {
  switch (props.metric) {
    case 'pe':
      return 'PE'
    case 'pb':
      return 'PB'
    case 'amount':
      return '成交额(亿)'
    default:
      return '涨跌幅%'
  }
}

function getColor(value: number): string {
  if (props.metric === 'change') {
    if (value >= 9.9) return '#dc2626'
    if (value >= 5) return '#ef4444'
    if (value >= 2) return '#f87171'
    if (value > 0) return '#fca5a5'
    if (value === 0) return '#64748b'
    if (value > -2) return '#86efac'
    if (value > -5) return '#4ade80'
    if (value > -9.9) return '#22c55e'
    return '#16a34a'
  }
  // PE/PB 用渐变色
  if (value <= 0) return '#64748b'
  if (value < 15) return '#22c55e'
  if (value < 30) return '#eab308'
  if (value < 50) return '#f97316'
  return '#ef4444'
}

function transformData() {
  return props.data.map((industry) => ({
    name: industry.name,
    value: industry.value,
    itemStyle: {
      color: getColor(industry.change),
      borderColor: '#1a1f2e',
      borderWidth: 2
    },
    label: {
      show: true,
      formatter: `{b}\n{c}亿`,
      fontSize: 12,
      color: '#fff'
    },
    children: industry.children.slice(0, 50).map((stock) => ({
      name: stock.name,
      value: stock.value,
      stock: stock,
      itemStyle: {
        color: getColor(getMetricValue(stock)),
        borderColor: '#1a1f2e',
        borderWidth: 1
      },
      label: {
        show: true,
        formatter: (params: { data: { stock: CloudMapStock } }) => {
          const s = params.data.stock
          const metricValue = getMetricValue(s)
          return `${s.name}\n${metricValue.toFixed(2)}`
        },
        fontSize: 10,
        color: '#fff'
      }
    }))
  }))
}

function initChart() {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: (params: { data: { name?: string; value?: number; stock?: CloudMapStock } }) => {
        const data = params.data
        if (data.stock) {
          const s = data.stock
          return `
            <div style="padding: 8px;">
              <div style="font-weight: bold; margin-bottom: 4px;">${s.name} (${s.code})</div>
              <div>涨跌幅: <span style="color: ${getColor(s.change)}">${s.change}%</span></div>
              <div>市值: ${s.value.toFixed(2)}亿</div>
              <div>PE: ${s.pe || '-'}</div>
              <div>PB: ${s.pb || '-'}</div>
            </div>
          `
        }
        return `<div style="padding: 8px;"><strong>${
          data.name
        }</strong><br/>市值: ${data.value?.toFixed(2)}亿</div>`
      },
      backgroundColor: 'rgba(15, 20, 25, 0.95)',
      borderColor: '#2d3748',
      textStyle: {
        color: '#fff'
      }
    },
    series: [
      {
        type: 'treemap',
        data: transformData(),
        width: '100%',
        height: '100%',
        roam: false,
        nodeClick: 'link',
        breadcrumb: {
          show: false
        },
        label: {
          show: true,
          formatter: '{b}',
          fontSize: 11,
          color: '#fff'
        },
        upperLabel: {
          show: true,
          height: 30,
          color: '#fff',
          fontSize: 12,
          fontWeight: 'bold'
        },
        itemStyle: {
          borderColor: '#1a1f2e',
          borderWidth: 2,
          gapWidth: 2
        },
        levels: [
          {
            itemStyle: {
              borderWidth: 2,
              borderColor: '#1a1f2e',
              gapWidth: 2
            }
          },
          {
            colorSaturation: [0.3, 0.6],
            itemStyle: {
              borderWidth: 1,
              borderColor: '#1a1f2e',
              gapWidth: 1
            }
          }
        ]
      }
    ]
  }

  chartInstance.setOption(option)

  chartInstance.on('click', (params: { data?: { stock?: CloudMapStock } }) => {
    if (params.data?.stock) {
      emit('stock-click', params.data.stock)
    }
  })
}

function resizeChart() {
  chartInstance?.resize()
}

watch(
  () => [props.data, props.metric],
  () => {
    if (chartInstance) {
      chartInstance.setOption({
        series: [{ data: transformData() }]
      })
    }
  },
  { deep: true }
)

onMounted(() => {
  initChart()
  window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeChart)
  chartInstance?.dispose()
})
</script>

<style scoped lang="scss">
.treemap-chart {
  width: 100%;
  height: 500px;
}
</style>
