<template>
  <div class="prediction-chart">
    <div class="chart-header">
      <h4>预测价格趋势图</h4>
      <span class="chart-info">蓝色线：历史数据，红色线：预测数据，灰色区域：置信区间</span>
    </div>
    <div class="chart-container" ref="chartContainer">
      <v-chart
        v-if="chartOption"
        class="chart"
        :option="chartOption"
        :loading="loading"
        autoresize
      />
      <div v-else class="no-data">
        <div class="no-data-icon">📈</div>
        <div class="no-data-text">暂无图表数据</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, CustomChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'

// 注册需要的 ECharts 组件
use([
  CanvasRenderer,
  LineChart,
  CustomChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const props = defineProps({
  predictionData: {
    type: Object,
    default: null
  },
  historicalData: {
    type: Array,
    default: () => []
  },
  stockCode: {
    type: String,
    required: true
  }
})

const chartContainer = ref(null)
const loading = ref(false)

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit'
  })
}

// 计算图表配置
const chartOption = computed(() => {
  if (
    !props.predictionData ||
    !props.predictionData.predictions ||
    props.predictionData.predictions.length === 0
  ) {
    return null
  }

  const predictions = props.predictionData.predictions
  const confidence = props.predictionData.confidence_intervals || []
  const historical = props.historicalData || []

  // 准备历史数据
  const historicalDates = historical.map((item) => formatDate(item.date))
  const historicalPrices = historical.map((item) => parseFloat(item.close))

  // 准备预测数据 - 预测日期应该在历史数据之后
  const predictionDates = predictions.map((item) => formatDate(item.date))
  const predictionPrices = predictions.map((item) => parseFloat(item.predicted_close))

  // 准备置信区间数据
  const upperBounds = confidence.map((item) => parseFloat(item.upper_bound))
  const lowerBounds = confidence.map((item) => parseFloat(item.lower_bound))

  // 创建完整的时间轴：历史日期 + 预测日期
  const allDates = [...historicalDates, ...predictionDates]

  // 创建历史数据序列：在预测时间点用null填充
  const historicalSeriesData = [
    ...historicalPrices,
    ...new Array(predictionDates.length).fill(null)
  ]

  // 创建预测数据序列：在历史时间点用null填充，但在连接点重复最后一个历史价格
  const predictionSeriesData = [...new Array(historicalDates.length).fill(null)]

  // 在预测数据开始处添加历史数据的最后一个点作为连接点
  if (historicalPrices.length > 0) {
    predictionSeriesData[historicalDates.length - 1] = historicalPrices[historicalPrices.length - 1]
  }
  predictionSeriesData.push(...predictionPrices)

  // 创建置信区间数据：只在预测时间段显示
  const upperBoundsData = [...new Array(historicalDates.length).fill(null), ...upperBounds]
  const lowerBoundsData = [...new Array(historicalDates.length).fill(null), ...lowerBounds]

  const series = [
    {
      name: '历史价格',
      type: 'line',
      data: historicalSeriesData,
      smooth: true,
      symbol: 'circle',
      symbolSize: 4,
      itemStyle: {
        color: '#1890ff'
      },
      lineStyle: {
        color: '#1890ff',
        width: 2
      },
      connectNulls: false,
      emphasis: {
        focus: 'series'
      }
    },
    {
      name: '预测价格',
      type: 'line',
      data: predictionSeriesData,
      smooth: true,
      symbol: 'diamond',
      symbolSize: 5,
      itemStyle: {
        color: '#ff4d4f'
      },
      lineStyle: {
        color: '#ff4d4f',
        width: 2,
        type: 'dashed'
      },
      connectNulls: false,
      emphasis: {
        focus: 'series'
      }
    }
  ]

  // 添加置信区间 - 创建填充区域的数据
  if (upperBounds.length > 0 && lowerBounds.length > 0) {
    // 创建置信区间填充数据（将上下边界合并为一个区域）
    const confidenceAreaData = []
    allDates.forEach((date, index) => {
      if (upperBoundsData[index] !== null && lowerBoundsData[index] !== null) {
        confidenceAreaData.push([index, lowerBoundsData[index], upperBoundsData[index]])
      } else {
        confidenceAreaData.push([index, null, null])
      }
    })

    // 置信区间填充系列
    series.push({
      name: '置信区间',
      type: 'custom',
      renderItem: function (params, api) {
        const categoryIndex = api.value(0)
        const lowVal = api.value(1)
        const highVal = api.value(2)

        if (lowVal === null || highVal === null) {
          return null
        }

        const lowPoint = api.coord([categoryIndex, lowVal])
        const highPoint = api.coord([categoryIndex, highVal])
        const halfWidth = api.size([1, 0])[0] * 0.1

        return {
          type: 'rect',
          shape: {
            x: lowPoint[0] - halfWidth,
            y: highPoint[1],
            width: halfWidth * 2,
            height: lowPoint[1] - highPoint[1]
          },
          style: {
            fill: 'rgba(255, 77, 79, 0.15)',
            stroke: 'transparent'
          }
        }
      },
      data: confidenceAreaData,
      z: 1,
      silent: true
    })
  }

  return {
    title: {
      show: false
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        }
      },
      formatter: function (params) {
        let result = `<div style="font-weight: bold; margin-bottom: 4px;">${params[0].axisValue}</div>`

        params.forEach((param) => {
          if (
            (param.seriesName === '历史价格' || param.seriesName === '预测价格') &&
            param.value !== null
          ) {
            const color = param.seriesName === '历史价格' ? '#1890ff' : '#ff4d4f'
            // 处理数组格式的数据，取第二个值（价格）
            const value = Array.isArray(param.value) ? param.value[1] : param.value
            if (typeof value === 'number') {
              result += `<div style="margin: 2px 0;">
                  <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: ${color}; margin-right: 8px;"></span>
                  <span style="font-weight: 500;">${param.seriesName}:</span>
                  <span style="margin-left: 8px; color: ${color};">¥${value.toFixed(2)}</span>
                </div>`
            }
          }
        })

        // 显示置信区间信息
        const dataIndex = params[0].dataIndex
        const predictionIndex = dataIndex - historicalDates.length
        if (predictionIndex >= 0 && confidence[predictionIndex]) {
          result += `<div style="margin: 2px 0; color: #666; font-size: 12px;">
              置信区间: ¥${confidence[predictionIndex].lower_bound.toFixed(2)} - ¥${confidence[
                predictionIndex
              ].upper_bound.toFixed(2)}
            </div>`
        }

        return result
      }
    },
    legend: {
      data: ['历史价格', '预测价格'],
      top: 10,
      textStyle: {
        fontSize: 12
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '8%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: allDates,
      boundaryGap: false,
      axisLabel: {
        fontSize: 11,
        color: '#666'
      },
      axisTick: {
        alignWithLabel: true
      }
    },
    yAxis: {
      type: 'value',
      scale: true,
      axisLabel: {
        formatter: '¥{value}',
        fontSize: 11,
        color: '#666'
      },
      splitLine: {
        lineStyle: {
          color: '#f0f0f0'
        }
      }
    },
    series: series
  }
})

// 监听数据变化
watch(
  () => [props.predictionData, props.historicalData],
  () => {
    // 数据变化时可以添加一些处理逻辑
  },
  { deep: true }
)
</script>

<style scoped>
.prediction-chart {
  width: 100%;
  background: white;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.chart-header h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.chart-info {
  font-size: 12px;
  color: #999;
}

.chart-container {
  width: 100%;
  height: 400px;
  position: relative;
}

.chart {
  width: 100%;
  height: 100%;
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.no-data-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.no-data-text {
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .chart-info {
    font-size: 11px;
  }

  .chart-container {
    height: 300px;
  }
}
</style>
