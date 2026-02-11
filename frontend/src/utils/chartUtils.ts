/**
 * 图表工具函数和配置
 */

// 类型定义
interface ChartTheme {
  color: string[]
  backgroundColor: string
  textStyle: {
    fontFamily: string
    fontSize: number
    color: string
  }
  title: {
    textStyle: {
      fontSize: number
      fontWeight: string
      color: string
    }
  }
  legend: {
    textStyle: {
      fontSize: number
      color: string
    }
  }
  grid: {
    left: string
    right: string
    bottom: string
    containLabel: boolean
    borderColor: string
  }
  tooltip: {
    backgroundColor: string
    borderColor: string
    borderWidth: number
    textStyle: {
      color: string
      fontSize: number
    }
  }
}

interface ResponsiveConfig {
  mobile: {
    grid: {
      left: string
      right: string
      bottom: string
      top: string
    }
    legend: {
      orient: 'horizontal' | 'vertical'
      bottom: string
      textStyle: {
        fontSize: number
      }
    }
    tooltip: {
      trigger: 'axis'
      axisPointer: {
        type: string
      }
    }
  }
  desktop: {
    grid: {
      left: string
      right: string
      bottom: string
      top: string
    }
    legend: {
      orient: 'horizontal' | 'vertical'
      top: string
    }
    tooltip: {
      trigger: 'axis'
      axisPointer: {
        type: string
        crossStyle: {
          color: string
        }
      }
    }
  }
}

interface BaseChartOption {
  title?: string
  isMobile?: boolean
  showDataZoom?: boolean
  showToolbox?: boolean
}

interface KLineDataItem {
  date: string
  open: number
  close: number
  low: number
  high: number
  volume: number
  amount?: number
}

interface ProcessedKLineData {
  dates: string[]
  klineData: number[][]
  volumeData: number[]
}

interface KLineChartOption extends BaseChartOption {
  showVolume?: boolean
  showMA?: boolean
  maParams?: number[]
}

// 默认图表主题配置
export const defaultTheme: ChartTheme = {
  color: [
    '#5470c6',
    '#91cc75',
    '#fac858',
    '#ee6666',
    '#73c0de',
    '#3ba272',
    '#fc8452',
    '#9a60b4',
    '#ea7ccc',
    '#ff9f7f'
  ],
  backgroundColor: '#ffffff',
  textStyle: {
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    fontSize: 12,
    color: '#333333'
  },
  title: {
    textStyle: {
      fontSize: 16,
      fontWeight: 'bold',
      color: '#333333'
    }
  },
  legend: {
    textStyle: {
      fontSize: 12,
      color: '#666666'
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
    borderColor: '#e6e6e6'
  },
  tooltip: {
    backgroundColor: 'rgba(50, 50, 50, 0.9)',
    borderColor: '#333',
    borderWidth: 1,
    textStyle: {
      color: '#fff',
      fontSize: 12
    }
  }
}

// 响应式配置
export const responsiveConfig: ResponsiveConfig = {
  mobile: {
    grid: {
      left: '5%',
      right: '5%',
      bottom: '15%',
      top: '15%'
    },
    legend: {
      orient: 'horizontal',
      bottom: '5%',
      textStyle: {
        fontSize: 10
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    }
  },
  desktop: {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%'
    },
    legend: {
      orient: 'horizontal',
      top: '5%'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      }
    }
  }
}

/**
 * 获取响应式图表配置
 * @param isMobile - 是否为移动设备
 * @returns 响应式配置
 */
export function getResponsiveConfig(
  isMobile = false
): ResponsiveConfig['mobile'] | ResponsiveConfig['desktop'] {
  return isMobile ? responsiveConfig.mobile : responsiveConfig.desktop
}

/**
 * 合并图表配置
 * @param baseConfig - 基础配置
 * @param customConfig - 自定义配置
 * @returns 合并后的配置
 */
export function mergeChartConfig(
  baseConfig: Record<string, any>,
  customConfig: Record<string, any>
): Record<string, any> {
  return deepMerge(baseConfig, customConfig)
}

/**
 * 深度合并对象
 * @param target - 目标对象
 * @param source - 源对象
 * @returns 合并后的对象
 */
function deepMerge(target: Record<string, any>, source: Record<string, any>): Record<string, any> {
  const result = { ...target }

  for (const key in source) {
    if (Object.prototype.hasOwnProperty.call(source, key)) {
      if (isObject(source[key]) && isObject(result[key])) {
        result[key] = deepMerge(result[key], source[key])
      } else {
        result[key] = source[key]
      }
    }
  }

  return result
}

/**
 * 判断是否为对象
 * @param obj - 待判断的值
 * @returns 是否为对象
 */
function isObject(obj: unknown): boolean {
  return obj !== null && typeof obj === 'object' && !Array.isArray(obj)
}

/**
 * 格式化数值
 * @param value - 数值
 * @param decimals - 小数位数
 * @returns 格式化后的字符串
 */
export function formatNumber(value: number | null | undefined, decimals = 2): string {
  if (value === null || value === undefined || isNaN(value)) {
    return '--'
  }

  return Number(value).toFixed(decimals)
}

/**
 * 格式化百分比
 * @param value - 数值
 * @param decimals - 小数位数
 * @returns 格式化后的百分比字符串
 */
export function formatPercent(value: number | null | undefined, decimals = 2): string {
  if (value === null || value === undefined || isNaN(value)) {
    return '--'
  }

  return `${(value * 100).toFixed(decimals)}%`
}

/**
 * 格式化成交量
 * @param volume - 成交量
 * @returns 格式化后的成交量字符串
 */
export function formatVolume(volume: number | null | undefined): string {
  if (volume === null || volume === undefined || isNaN(volume)) {
    return '--'
  }

  if (volume >= 100000000) {
    return `${(volume / 100000000).toFixed(2)}亿`
  } else if (volume >= 10000) {
    return `${(volume / 10000).toFixed(2)}万`
  } else {
    return volume.toString()
  }
}

/**
 * 格式化金额
 * @param amount - 金额
 * @returns 格式化后的金额字符串
 */
export function formatAmount(amount: number | null | undefined): string {
  if (amount === null || amount === undefined || isNaN(amount)) {
    return '--'
  }

  if (amount >= 100000000) {
    return `${(amount / 100000000).toFixed(2)}亿`
  } else if (amount >= 10000) {
    return `${(amount / 10000).toFixed(2)}万`
  } else {
    return amount.toFixed(2)
  }
}

/**
 * 获取颜色（涨跌色）
 * @param value - 数值
 * @param baseValue - 基准值
 * @returns 颜色值
 */
export function getTrendColor(value: number, baseValue = 0): string {
  if (value > baseValue) {
    return '#ee6666' // 红色（涨）
  } else if (value < baseValue) {
    return '#5470c6' // 蓝色（跌）
  } else {
    return '#91cc75' // 绿色（平）
  }
}

/**
 * 创建基础图表配置
 * @param options - 配置选项
 * @returns 图表配置
 */
export function createBaseChartOption(options: BaseChartOption = {}): Record<string, any> {
  const { title = '', isMobile = false, showDataZoom = true, showToolbox = true } = options

  const baseConfig: Record<string, any> = {
    title: {
      text: title,
      left: 'center',
      ...defaultTheme.title
    },
    tooltip: {
      ...defaultTheme.tooltip,
      ...getResponsiveConfig(isMobile).tooltip
    },
    legend: {
      ...defaultTheme.legend,
      ...getResponsiveConfig(isMobile).legend
    },
    grid: {
      ...defaultTheme.grid,
      ...getResponsiveConfig(isMobile).grid
    },
    color: defaultTheme.color,
    backgroundColor: defaultTheme.backgroundColor,
    textStyle: defaultTheme.textStyle
  }

  if (showDataZoom) {
    baseConfig.dataZoom = [
      {
        type: 'inside',
        xAxisIndex: 0,
        start: 0,
        end: 100
      },
      {
        type: 'slider',
        xAxisIndex: 0,
        start: 0,
        end: 100,
        height: isMobile ? 20 : 30,
        bottom: isMobile ? 5 : 10
      }
    ]
  }

  // 工具箱功能已被禁用

  return baseConfig
}

/**
 * 检测设备类型
 * @returns 是否为移动设备
 */
export function isMobileDevice(): boolean {
  return window.innerWidth <= 768
}

/**
 * 防抖函数
 * @param func - 要防抖的函数
 * @param wait - 等待时间
 * @returns 防抖后的函数
 */
export function debounce<T extends (...args: any[]) => void>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | undefined
  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    if (timeout) {
      clearTimeout(timeout)
    }
    timeout = setTimeout(later, wait)
  }
}

/**
 * 节流函数
 * @param func - 要节流的函数
 * @param limit - 限制时间
 * @returns 节流后的函数
 */
export function throttle<T extends (...args: any[]) => void>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false
  return function executedFunction(this: any, ...args: Parameters<T>) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

/**
 * 创建K线图表配置
 * @param data - 股票数据
 * @param options - 配置选项
 * @returns K线图表配置
 */
export function createKLineChartOption(
  data: KLineDataItem[],
  options: KLineChartOption = {}
): Record<string, any> {
  const {
    title = 'K线图表',
    isMobile = false,
    showVolume = false,
    showMA = false,
    maParams = [5, 10, 20, 30]
  } = options

  if (!data || data.length === 0) {
    return createEmptyChartOption(title, isMobile)
  }

  // 处理数据
  const processedData = processKLineData(data)

  // 基础配置
  const baseOption = createBaseChartOption({
    title: '',
    isMobile,
    showDataZoom: true,
    showToolbox: false
  })

  const chartOption: Record<string, any> = {
    ...baseOption,
    title: {
      text: title,
      left: 'center',
      textStyle: {
        fontSize: isMobile ? 14 : 16,
        fontWeight: 'bold',
        color: '#333'
      }
    },
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
      formatter: function (params: any) {
        return formatKLineTooltip(params, data)
      }
    },
    legend: {
      data: ['K线'],
      top: isMobile ? 25 : 30,
      textStyle: {
        fontSize: isMobile ? 11 : 12,
        color: '#666'
      }
    },
    grid: {
      left: isMobile ? '8%' : '5%',
      right: isMobile ? '8%' : '5%',
      bottom: isMobile ? '20%' : '15%',
      top: isMobile ? '20%' : '15%',
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
        formatter: function (value: number) {
          return formatNumber(value, 2)
        }
      }
    },
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

  // 添加移动平均线
  if (showMA && maParams.length > 0) {
    const maData = calculateMA(data, maParams)
    maParams.forEach((period, index) => {
      chartOption.series.push({
        name: `MA${period}`,
        type: 'line',
        data: maData[period],
        smooth: true,
        lineStyle: {
          width: 1
        },
        showSymbol: false
      })
      chartOption.legend.data.push(`MA${period}`)
    })
  }

  return chartOption
}

/**
 * 处理K线数据
 * @param data - 原始股票数据
 * @returns 处理后的数据
 */
function processKLineData(data: KLineDataItem[]): ProcessedKLineData {
  const dates: string[] = []
  const klineData: number[][] = []
  const volumeData: number[] = []

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

/**
 * 格式化K线图表提示框
 * @param params - 图表参数
 * @param data - 原始数据
 * @returns 格式化后的HTML字符串
 */
function formatKLineTooltip(params: any[], data: KLineDataItem[]): string {
  if (!params || params.length === 0) return ''

  const dataIndex = params[0].dataIndex
  const stockData = data[dataIndex]

  if (!stockData) return ''

  const date = stockData.date
  const open = formatNumber(stockData.open, 2)
  const high = formatNumber(stockData.high, 2)
  const low = formatNumber(stockData.low, 2)
  const close = formatNumber(stockData.close, 2)
  const volume = formatVolume(stockData.volume)
  const amount = formatAmount(stockData.amount)

  // 计算涨跌幅
  const change = stockData.close - stockData.open
  const changePercent = ((change / stockData.open) * 100).toFixed(2)
  const changeColor = change >= 0 ? '#ee6666' : '#5470c6'

  return `
    <div style="padding: 8px;">
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
        <span>涨跌:</span>
        <span style="color: ${changeColor};">${change >= 0 ? '+' : ''}${formatNumber(
          change,
          2
        )} (${changePercent}%)</span>
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

/**
 * 计算移动平均线
 * @param data - 股票数据
 * @param periods - 周期数组
 * @returns 移动平均线数据
 */
function calculateMA(data: KLineDataItem[], periods: number[]): Record<number, string[] | null[]> {
  const result: Record<number, string[] | null[]> = {}

  periods.forEach((period) => {
    const maData: (string | null)[] = []
    for (let i = 0; i < data.length; i++) {
      if (i < period - 1) {
        maData.push(null)
      } else {
        let sum = 0
        for (let j = 0; j < period; j++) {
          sum += data[i - j].close
        }
        maData.push((sum / period).toFixed(2))
      }
    }
    result[period] = maData
  })

  return result
}

/**
 * 创建空图表配置
 * @param title - 图表标题
 * @param isMobile - 是否为移动设备
 * @returns 空图表配置
 */
function createEmptyChartOption(title: string, isMobile: boolean): Record<string, any> {
  const baseOption = createBaseChartOption({
    title: '',
    isMobile,
    showDataZoom: false,
    showToolbox: false
  })

  return {
    ...baseOption,
    title: {
      text: title || '暂无数据',
      left: 'center',
      top: 'middle',
      textStyle: {
        fontSize: isMobile ? 14 : 16,
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
