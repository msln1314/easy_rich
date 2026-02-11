<template>
  <div class="chart-container">
    <div class="chart-header" v-if="title">
      <h3>{{ title }}</h3>
    </div>
    <div class="chart-wrapper" ref="chartWrapper">
      <VChart
        ref="chart"
        :option="chartOption"
        :loading="loading"
        :loading-options="loadingOptions"
        :autoresize="true"
        @zr:click="handleChartClick"
        @datazoom="handleDataZoom"
        class="chart"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { CandlestickChart, BarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  TitleComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { createBaseChartOption, formatNumber, isMobileDevice } from '@/utils/chartUtils'

// 注册需要的 ECharts 组件
use([
  CanvasRenderer,
  CandlestickChart,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  TitleComponent
])

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  title: {
    type: String,
    default: 'K线价格图表'
  },
  loading: {
    type: Boolean,
    default: false
  },
  height: {
    type: String,
    default: '400px'
  },
  showVolume: {
    type: Boolean,
    default: false
  }
})
console.log(props, 'props')
const emit = defineEmits(['chart-click', 'data-zoom'])

// 组件状态
const chart = ref(null)
const chartWrapper = ref(null)

const loadingOptions = {
  text: '加载中...',
  color: '#409EFF',
  textColor: '#409EFF',
  maskColor: 'rgba(255, 255, 255, 0.8)',
  zlevel: 0,
  fontSize: 12,
  showSpinner: true,
  spinnerRadius: 10,
  lineWidth: 5
}

// 计算图表配置
const chartOption = computed(() => {
  if (!props.data || props.data.length === 0) {
    return createEmptyChartOption()
  }

  return createKLineChartOption(props.data, {
    showVolume: props.showVolume,
    isMobile: isMobileDevice()
  })
})

// 创建空图表配置
function createEmptyChartOption() {
  const baseOption = createBaseChartOption({
    title: '',
    isMobile: isMobileDevice(),
    showDataZoom: false,
    showToolbox: false
  })

  return {
    ...baseOption,
    title: {
      text: '暂无数据',
      left: 'center',
      top: 'middle',
      textStyle: {
        fontSize: 16,
        color: '#999'
      }
    },
    xAxis: {
      type: 'category',
      data: []
    },
    yAxis: {
      type: 'value'
    },
    series: []
  }
}

// 创建K线图表配置
function createKLineChartOption(data, options = {}) {
  const { showVolume = false, isMobile = false } = options

  console.log('createKLineChartOption 接收的数据:', data)
  console.log('showVolume:', showVolume)

  // 处理数据
  const processedData = processKLineData(data)
  console.log('处理后的数据:', processedData)

  // 基础配置
  const baseOption = createBaseChartOption({
    title: '',
    isMobile,
    showDataZoom: true,
    showToolbox: false
  })

  // K线图表配置
  const klineOption = {
    ...baseOption,
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      backgroundColor: 'rgba(50, 50, 50, 0.95)',
      borderColor: '#333',
      borderWidth: 1,
      textStyle: {
        color: '#fff',
        fontSize: isMobile ? 11 : 12
      },
      formatter: function (params) {
        if (!params || params.length === 0) return ''

        const dataIndex = params[0].dataIndex
        const stockData = data[dataIndex]
        if (!stockData) return ''

        const date = stockData.date
        const open = formatNumber(stockData.open, 2)
        const high = formatNumber(stockData.high, 2)
        const low = formatNumber(stockData.low, 2)
        const close = formatNumber(stockData.close, 2)
        const volume = formatVolumeLocal(stockData.volume)
        const amount = formatAmountLocal(stockData.amount)

        // 计算涨跌幅
        const change = stockData.close - stockData.open
        const changePercent = ((change / stockData.open) * 100).toFixed(2)
        const changeColor = change >= 0 ? '#ee6666' : '#5470c6'

        return `
                <div style="padding: 8px;width:120px;">
                  <div style="font-weight: bold; margin-bottom: 6px;">${date}</div>
                  <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>开盘:</span>
                    <span style="color: #fff;">${open}</span>
                  </div>
                  <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>最高:</span>
                    <span style="color: #ee6666;">${high}</span>
                  </div>
                  <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>最低:</span>
                    <span style="color: #5470c6;">${low}</span>
                  </div>
                  <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>收盘:</span>
                    <span style="color: #fff;">${close}</span>
                  </div>
                  <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>涨跌额:</span>
                    <span style="color: ${changeColor};">${formatNumber(change, 2)}</span>
                  </div>
                   <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>涨跌幅:</span>
                    <span style="color: ${changeColor};">${changePercent}%</span>
                  </div>
                  <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>成交量:</span>
                    <span style="color: #91cc75;">${volume}</span>
                  </div>
                  <div style="display: flex; justify-content: space-between;">
                    <span>成交额:</span>
                    <span style="color: #91cc75;">${amount}</span>
                  </div>
                </div>
              `
      }
    },
    legend: {
      data: ['K线'],
      top: isMobile ? 5 : 10,
      textStyle: {
        fontSize: isMobile ? 11 : 12,
        color: '#666'
      },
      selected: {
        K线: true
      }
    },
    grid: {
      left: isMobile ? '10%' : '8%', // 增加左边距，为Y轴标签留出更多空间
      right: isMobile ? '8%' : '5%',
      bottom: isMobile ? '22%' : '18%', // 增加底部边距，为滑块留出空间
      top: isMobile ? '15%' : '12%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: processedData.dates,
      scale: true,
      boundaryGap: false,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: 'dataMin',
      max: 'dataMax',
      axisLabel: {
        fontSize: isMobile ? 10 : 11,
        color: '#666'
      }
    },
    yAxis: {
      scale: true,
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(250,250,250,0.1)', 'rgba(200,200,200,0.1)']
        }
      },
      axisLabel: {
        fontSize: isMobile ? 10 : 11,
        color: '#666',
        margin: isMobile ? 12 : 15, // 增加Y轴标签与图表的间距
        formatter: function (value) {
          return formatNumber(value, 2)
        }
      }
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100,
        filterMode: 'filter'
      },
      {
        show: true,
        type: 'slider',
        bottom: isMobile ? '2%' : '1%',
        left: isMobile ? '10%' : '8%', // 与grid保持一致的左边距
        right: isMobile ? '8%' : '5%',
        start: 0,
        end: 100,
        height: isMobile ? 16 : 20,
        filterMode: 'filter',
        textStyle: {
          fontSize: isMobile ? 9 : 10,
          color: '#666'
        },
        handleStyle: {
          color: '#409EFF',
          borderColor: '#409EFF'
        },
        dataBackground: {
          areaStyle: {
            color: 'rgba(64, 158, 255, 0.1)'
          },
          lineStyle: {
            color: 'rgba(64, 158, 255, 0.3)'
          }
        },
        selectedDataBackground: {
          areaStyle: {
            color: 'rgba(64, 158, 255, 0.2)'
          },
          lineStyle: {
            color: '#409EFF'
          }
        }
      }
    ],
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: processedData.klineData,
        itemStyle: {
          color: '#ee6666', // 阳线颜色（涨）
          color0: '#5470c6', // 阴线颜色（跌）
          borderColor: '#ee6666', // 阳线边框颜色
          borderColor0: '#5470c6' // 阴线边框颜色
        },
        emphasis: {
          itemStyle: {
            color: '#ff7f7f',
            color0: '#7ba7d9',
            borderColor: '#ff7f7f',
            borderColor0: '#7ba7d9'
          }
        }
      }
    ]
  }

  // 如果需要显示成交量，添加成交量子图
  if (showVolume) {
    klineOption.grid = [
      {
        left: isMobile ? '10%' : '8%', // 增加左边距，为Y轴标签留出更多空间
        right: isMobile ? '8%' : '5%',
        top: isMobile ? '15%' : '12%',
        height: isMobile ? '50%' : '55%' // 调整K线图高度，给成交量更多空间
      },
      {
        left: isMobile ? '10%' : '8%', // 与K线图保持一致的左边距
        right: isMobile ? '8%' : '5%',
        top: isMobile ? '70%' : '70%', // 调整成交量图位置
        height: isMobile ? '18%' : '18%' // 增加成交量图高度
      }
    ]

    klineOption.xAxis = [
      {
        type: 'category',
        data: processedData.dates,
        scale: true,
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax',
        show: false
      },
      {
        type: 'category',
        gridIndex: 1,
        data: processedData.dates,
        scale: true,
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax',
        axisLabel: {
          fontSize: isMobile ? 9 : 10, // 减小字体大小
          color: '#666',
          margin: isMobile ? 6 : 8, // 增加标签与轴的距离
          rotate: isMobile ? 45 : 0 // 移动端旋转标签避免重叠
        }
      }
    ]

    klineOption.yAxis = [
      {
        scale: true,
        splitArea: {
          show: true,
          areaStyle: {
            color: ['rgba(250,250,250,0.1)', 'rgba(200,200,200,0.1)']
          }
        },
        axisLabel: {
          fontSize: isMobile ? 10 : 11,
          color: '#666',
          margin: isMobile ? 12 : 15, // 增加K线图Y轴标签与图表的间距
          formatter: function (value) {
            return formatNumber(value, 2)
          }
        }
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: isMobile ? 1 : 2, // 移动端减少分割线数量
        axisLabel: {
          fontSize: isMobile ? 8 : 9, // 减小成交量Y轴字体
          color: '#666',
          margin: isMobile ? 8 : 10, // 增加成交量Y轴标签间距
          formatter: function (value) {
            return formatVolumeLocal(value)
          }
        },
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false }
      }
    ]

    // 添加dataZoom配置，确保K线和成交量同步缩放
    klineOption.dataZoom = [
      {
        type: 'inside',
        xAxisIndex: [0, 1], // 同时控制两个x轴
        start: 0,
        end: 100,
        filterMode: 'filter'
      },
      {
        show: true,
        xAxisIndex: [0, 1], // 同时控制两个x轴
        type: 'slider',
        bottom: isMobile ? '2%' : '1%', // 使用bottom定位，更精确控制位置
        left: isMobile ? '10%' : '8%', // 与grid保持一致的左边距
        right: isMobile ? '8%' : '5%', // 与grid保持一致的右边距
        start: 0,
        end: 100,
        height: isMobile ? 16 : 20, // 调整滑块高度
        filterMode: 'filter',
        textStyle: {
          fontSize: isMobile ? 9 : 10,
          color: '#666'
        },
        handleStyle: {
          color: '#409EFF',
          borderColor: '#409EFF'
        },
        dataBackground: {
          areaStyle: {
            color: 'rgba(64, 158, 255, 0.1)'
          },
          lineStyle: {
            color: 'rgba(64, 158, 255, 0.3)'
          }
        },
        selectedDataBackground: {
          areaStyle: {
            color: 'rgba(64, 158, 255, 0.2)'
          },
          lineStyle: {
            color: '#409EFF'
          }
        }
      }
    ]

    // 添加成交量系列
    klineOption.series.push({
      name: '成交量',
      type: 'bar',
      xAxisIndex: 1,
      yAxisIndex: 1,
      data: processedData.volumeData,
      itemStyle: {
        color: function (params) {
          const dataIndex = params.dataIndex
          const stockData = data[dataIndex]
          return stockData.close >= stockData.open ? '#ee6666' : '#5470c6'
        }
      }
    })

    klineOption.legend.data.push('成交量')
  }

  console.log('最终图表配置:', klineOption)
  return klineOption
}

// 处理K线数据
function processKLineData(data) {
  const dates = []
  const klineData = []
  const volumeData = []

  data.forEach((item) => {
    dates.push(item.date)
    klineData.push([
      item.open, // 开盘价
      item.close, // 收盘价
      item.low, // 最低价
      item.high // 最高价
    ])
    volumeData.push(item.volume)
  })

  return {
    dates,
    klineData,
    volumeData
  }
}

// 本地格式化成交量函数
function formatVolumeLocal(volume) {
  if (volume === null || volume === undefined || isNaN(volume)) {
    return '--'
  }

  if (volume >= 100000000) {
    return `${(volume / 100000000).toFixed(1)}亿`
  } else if (volume >= 10000) {
    return `${(volume / 10000).toFixed(1)}万`
  } else {
    return volume.toString()
  }
}

// 本地格式化金额函数
function formatAmountLocal(amount) {
  if (amount === null || amount === undefined || isNaN(amount)) {
    return '--'
  }

  if (amount >= 100000000) {
    return `${(amount / 100000000).toFixed(2)}亿`
  } else if (amount >= 10000) {
    return `${(amount / 10000).toFixed(2)}万`
  } else {
    return formatNumber(amount, 2)
  }
}

// 事件处理
const handleChartClick = (params) => {
  emit('chart-click', params)
}

const handleDataZoom = (params) => {
  emit('data-zoom', params)
}

// 监听窗口大小变化
const handleResize = () => {
  if (chart.value) {
    chart.value.resize()
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  background: #fafafa;
}

.chart-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.chart-wrapper {
  position: relative;
  padding: 20px;
  height: 500px;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
