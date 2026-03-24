import { defHttp } from '/@/utils/http/axios'

enum Api {
  SCREEN_STOCKS = '/screener/stocks',
  LIMIT_UP = '/screener/limit-up',
  LIMIT_DOWN = '/screener/limit-down',
  HIGH_TURNOVER = '/screener/high-turnover',
  LOW_PE = '/screener/low-pe',
  VOLUME_SURGE = '/screener/volume-surge',
  SMALL_CAP = '/screener/small-cap'
}

// 条件字段类型
export interface Condition {
  field: string
  operator: 'gt' | 'lt' | 'gte' | 'lte' | 'between'
  value: number
  value2?: number
}

// 选股结果
export interface ScreenerResult {
  stock_code: string
  stock_name: string
  price: number | null
  change_percent: number | null
  match_score: number
  match_reasons: string[]
}

// 条件选股
export function screenByCondition(conditions: Condition[], limit: number = 50) {
  return defHttp.post({
    url: Api.SCREEN_STOCKS,
    data: { conditions, limit }
  })
}

// 涨停股筛选
export function screenLimitUp(limit: number = 50) {
  return defHttp.get({
    url: Api.LIMIT_UP,
    params: { limit }
  })
}

// 跌停股筛选
export function screenLimitDown(limit: number = 50) {
  return defHttp.get({
    url: Api.LIMIT_DOWN,
    params: { limit }
  })
}

// 高换手率筛选
export function screenHighTurnover(limit: number = 50) {
  return defHttp.get({
    url: Api.HIGH_TURNOVER,
    params: { limit }
  })
}

// 低估值筛选
export function screenLowPE(limit: number = 50) {
  return defHttp.get({
    url: Api.LOW_PE,
    params: { limit }
  })
}

// 放量股票筛选
export function screenVolumeSurge(limit: number = 50) {
  return defHttp.get({
    url: Api.VOLUME_SURGE,
    params: { limit }
  })
}

// 小市值筛选
export function screenSmallCap(limit: number = 50) {
  return defHttp.get({
    url: Api.SMALL_CAP,
    params: { limit }
  })
}

// 条件字段配置
export const conditionFields = [
  { label: '价格', field: 'price', unit: '元' },
  { label: '涨跌幅', field: 'change_percent', unit: '%' },
  { label: '成交量', field: 'volume', unit: '手' },
  { label: '成交额', field: 'amount', unit: '元' },
  { label: '换手率', field: 'turnover_rate', unit: '%' },
  { label: '市盈率', field: 'pe_ratio', unit: '' },
  { label: '市净率', field: 'pb_ratio', unit: '' },
  { label: '总市值', field: 'market_cap', unit: '元' },
  { label: '振幅', field: 'amplitude', unit: '%' }
]

// 操作符配置
export const operators = [
  { label: '大于', value: 'gt' },
  { label: '小于', value: 'lt' },
  { label: '大于等于', value: 'gte' },
  { label: '小于等于', value: 'lte' },
  { label: '介于', value: 'between' }
]