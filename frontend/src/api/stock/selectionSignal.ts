import { defHttp } from '/@/utils/http/axios'

enum Api {
  SELECTION_SIGNALS = '/stock/selection',
  BUY_SIGNALS = '/stock/selection/buy-signals',
  MULTI_FILTER = '/stock/selection/multi-filter',
  STATISTICS = '/stock/selection/statistics/overview',
  SYNC = '/stock/selection/sync'
}

// 选股信号参数
export interface SelectionSignalParams {
  signal_date?: string
  recommend?: 'strong_buy' | 'buy' | 'hold' | 'sell' | 'strong_sell'
  min_score?: number
  max_score?: number
  ma_signal?: number
  macd_signal?: number
  kdj_signal?: number
  rsi_signal?: number
  volume_signal?: number
  industry?: string
  market?: string
  stock_code?: string
  stock_name?: string
  page?: number
  page_size?: number
}

// 选股信号项
export interface SelectionSignalItem {
  id: number
  stock_code: string
  stock_name: string
  full_code: string
  market: string
  industry: string
  signal_date: string
  current_price: number
  change_percent: number
  ma_signal: number
  macd_signal: number
  kdj_signal: number
  rsi_signal: number
  volume_signal: number
  total_score: number
  score_rank: number
  recommend: string
  signal_strength: number
  confidence: number
  data_time: string
}

// 多因子筛选参数
export interface MultiFactorParams {
  signal_date?: string
  require_macd_golden?: boolean
  require_kdj_golden?: boolean
  require_ma_golden?: boolean
  require_volume_increase?: boolean
  require_rsi_oversold?: boolean
  min_score?: number
  industry?: string
  market?: string
  limit?: number
}

// 信号统计
export interface SignalStatistics {
  signal_date: string
  total: number
  recommend_stats: Record<string, number>
  score_stats: Record<string, number>
}

// 获取选股信号列表
export function getSelectionSignals(params: SelectionSignalParams) {
  return defHttp.get({
    url: Api.SELECTION_SIGNALS,
    params
  })
}

// 获取买入信号
export function getBuySignals(params: {
  signal_date?: string
  min_score?: number
  limit?: number
}) {
  return defHttp.get({
    url: Api.BUY_SIGNALS,
    params
  })
}

// 多因子筛选
export function multiFactorFilter(params: MultiFactorParams) {
  return defHttp.get({
    url: Api.MULTI_FILTER,
    params
  })
}

// 获取单只股票信号详情
export function getStockSignalDetail(stockCode: string, signalDate?: string) {
  return defHttp.get({
    url: `${Api.SELECTION_SIGNALS}/${stockCode}`,
    params: { signal_date: signalDate }
  })
}

// 获取信号统计
export function getSignalStatistics(signalDate?: string) {
  return defHttp.get({
    url: Api.STATISTICS,
    params: { signal_date: signalDate }
  })
}

// 手动同步信号
export function syncSignals(limit: number = 500) {
  return defHttp.post({
    url: Api.SYNC,
    data: { limit }
  })
}

// 推荐信号映射
export const recommendMap: Record<string, { label: string; type: string }> = {
  strong_buy: { label: '强买入', type: 'danger' },
  buy: { label: '买入', type: 'warning' },
  hold: { label: '持有', type: 'info' },
  sell: { label: '卖出', type: 'success' },
  strong_sell: { label: '强卖出', type: 'primary' }
}

// 信号值映射
export const signalValueMap: Record<number, { label: string; icon: string; color: string }> = {
  1: { label: '金叉/超卖', icon: '↑', color: '#67C23A' },
  0: { label: '无信号', icon: '-', color: '#909399' },
  [-1]: { label: '死叉/超买', icon: '↓', color: '#F56C6C' }
}