/**
 * 股票相关工具函数
 */

/**
 * 验证股票代码格式
 * @param stockCode - 股票代码
 * @returns 是否为有效的股票代码格式
 */
export function validateStockCode(stockCode: string): boolean {
  if (!stockCode) return false

  // 支持格式: sh.600000, sz.000001 等
  const regex = /^[a-zA-Z]{2}\.\d{6}$/
  return regex.test(stockCode)
}

/**
 * 格式化股票代码（转换为小写）
 * @param stockCode - 股票代码
 * @returns 格式化后的股票代码
 */
export function formatStockCode(stockCode: string): string {
  if (!stockCode) return ''
  return stockCode.toLowerCase()
}

/**
 * 获取市场名称
 * @param stockCode - 股票代码
 * @returns 市场名称
 */
export function getMarketName(stockCode: string): string {
  if (!stockCode) return '未知'

  const prefix = stockCode.toLowerCase().split('.')[0]

  switch (prefix) {
    case 'sh':
      return '上海证券交易所'
    case 'sz':
      return '深圳证券交易所'
    case 'bj':
      return '北京证券交易所'
    default:
      return '未知市场'
  }
}

/**
 * 格式化数字为千分位格式
 * @param num - 数字
 * @param decimals - 小数位数
 * @returns 格式化后的数字字符串
 */
export function formatNumber(num: number | null | undefined, decimals: number = 2): string {
  if (num === null || num === undefined || isNaN(num)) return '--'

  return Number(num).toLocaleString('zh-CN', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  })
}

/**
 * 格式化价格
 * @param price - 价格
 * @returns 格式化后的价格字符串
 */
export function formatPrice(price: number | null | undefined): string {
  return formatNumber(price, 2)
}

/**
 * 格式化成交量
 * @param volume - 成交量
 * @returns 格式化后的成交量字符串
 */
export function formatVolume(volume: number | null | undefined): string {
  if (volume === null || volume === undefined || isNaN(volume)) return '--'

  const num = Number(volume)

  if (num >= 100000000) {
    return (num / 100000000).toFixed(2) + '亿'
  } else if (num >= 10000) {
    return (num / 10000).toFixed(2) + '万'
  } else {
    return num.toString()
  }
}

/**
 * 格式化股本数量
 * @param shares - 股本数量
 * @returns 格式化后的股本字符串
 */
export function formatShares(shares: number | null | undefined): string {
  if (shares === null || shares === undefined || isNaN(shares)) return '--'

  const num = Number(shares)

  if (num >= 100000000) {
    return (num / 100000000).toFixed(2) + '亿股'
  } else if (num >= 10000) {
    return (num / 10000).toFixed(2) + '万股'
  } else {
    return num.toString() + '股'
  }
}

/**
 * 格式化市值
 * @param marketCap - 市值
 * @returns 格式化后的市值字符串
 */
export function formatMarketCap(marketCap: number | null | undefined): string {
  if (marketCap === null || marketCap === undefined || isNaN(marketCap)) return '--'

  const num = Number(marketCap)

  if (num >= 100000000) {
    return (num / 100000000).toFixed(2) + '亿元'
  } else if (num >= 10000) {
    return (num / 10000).toFixed(2) + '万元'
  } else {
    return num.toFixed(2) + '元'
  }
}

/**
 * 格式化成交额
 * @param turnover - 成交额
 * @returns 格式化后的成交额字符串
 */
export function formatTurnover(turnover: number | null | undefined): string {
  if (turnover === null || turnover === undefined || isNaN(turnover)) return '--'

  const num = Number(turnover)

  if (num >= 100000000) {
    return (num / 100000000).toFixed(2) + '亿元'
  } else if (num >= 10000) {
    return (num / 10000).toFixed(2) + '万元'
  } else {
    return num.toFixed(2) + '元'
  }
}

/**
 * 格式化百分比
 * @param percent - 百分比数值
 * @returns 格式化后的百分比字符串
 */
export function formatPercent(percent: number | null | undefined): string {
  if (percent === null || percent === undefined || isNaN(percent)) return '--'
  return Number(percent).toFixed(2) + '%'
}

/**
 * 格式化比率
 * @param ratio - 比率数值
 * @returns 格式化后的比率字符串
 */
export function formatRatio(ratio: number | null | undefined): string {
  if (ratio === null || ratio === undefined || isNaN(ratio)) return '--'
  return Number(ratio).toFixed(2)
}

/**
 * 格式化涨跌额
 * @param changeAmount - 涨跌额
 * @returns 格式化后的涨跌额字符串
 */
export function formatChangeAmount(changeAmount: number | null | undefined): string {
  if (changeAmount === null || changeAmount === undefined || isNaN(changeAmount)) return '--'

  const num = Number(changeAmount)
  const sign = num > 0 ? '+' : ''

  return sign + num.toFixed(2)
}

/**
 * 格式化涨跌幅
 * @param changePercent - 涨跌幅
 * @returns 格式化后的涨跌幅字符串
 */
export function formatChangePercent(changePercent: number | null | undefined): string {
  if (changePercent === null || changePercent === undefined || isNaN(changePercent)) return '--'

  const num = Number(changePercent)
  const sign = num > 0 ? '+' : ''

  return sign + num.toFixed(2) + '%'
}

/**
 * 获取涨跌颜色类名
 * @param value - 涨跌值
 * @returns CSS类名
 */
export function getChangeClass(value: number | null | undefined): string {
  if (value === null || value === undefined || isNaN(value)) return 'price-neutral'

  const num = Number(value)

  if (num > 0) {
    return 'price-up'
  } else if (num < 0) {
    return 'price-down'
  } else {
    return 'price-neutral'
  }
}

/**
 * 计算涨跌幅
 * @param current - 当前价格
 * @param previous - 前一日价格
 * @returns 包含涨跌额和涨跌幅的对象
 */
export function calculateChange(
  current: number | null | undefined,
  previous: number | null | undefined
): { change: number; changePercent: number } {
  if (!current || !previous) {
    return { change: 0, changePercent: 0 }
  }

  const change = current - previous
  const changePercent = (change / previous) * 100

  return {
    change: Number(change.toFixed(2)),
    changePercent: Number(changePercent.toFixed(2))
  }
}
