import request from '@/config/axios'

// ========== 类型定义 ==========

export interface DrawdownPoint {
  peak_date: string
  peak_price: number
  trough_date: string
  trough_price: number
  drawdown_percent: number
  duration_days: number
  recovery_date?: string
  recovery_days?: number
}

export interface DrawdownAnalysisResult {
  stock_code: string
  stock_name: string
  analysis_period: string
  max_drawdown: number
  max_drawdown_duration: number
  avg_drawdown: number
  avg_recovery_days: number
  drawdown_5p_count: number
  drawdown_10p_count: number
  drawdown_20p_count: number
  drawdown_30p_count: number
  drawdown_points: DrawdownPoint[]
}

export interface PullbackSignal {
  signal_date: string
  signal_type: string
  signal_strength: number
  current_drawdown: number
  support_price: number
  stop_loss_price: number
  reasoning: string
}

export interface PositionMonitor {
  stock_code: string
  cost_price: number
  current_price: number
  highest_price: number
  profit_percent: number
  drawdown_from_high: number
  drawdown_from_cost: number
  suggested_stop_profit: number
  alert_level: string
}

export interface DrawdownHistoryData {
  dates: string[]
  prices: number[]
  drawdown_areas: Array<{
    start: string
    end: string
    depth: number
  }>
}

// ========== API函数 ==========

/**
 * 回撤分析
 */
export const analyzeDrawdown = (data: {
  stock_code: string
  start_date?: string
  end_date?: string
}): Promise<IResponse<DrawdownAnalysisResult>> => {
  return request.post({ url: '/drawdown/analyze', data })
}

/**
 * 获取回调买点信号
 */
export const getPullbackSignals = (stockCode: string): Promise<IResponse<PullbackSignal[]>> => {
  return request.get({ url: `/drawdown/signals/${stockCode}` })
}

/**
 * 持仓监控
 */
export const monitorPosition = (data: {
  stock_code: string
  cost_price: number
  position_date: string
}): Promise<IResponse<PositionMonitor>> => {
  return request.post({ url: '/drawdown/position', data })
}

/**
 * 获取历史回撤图表数据
 */
export const getDrawdownHistory = (
  stockCode: string,
  threshold: number = 5
): Promise<IResponse<DrawdownHistoryData>> => {
  return request.get({ url: `/drawdown/history/${stockCode}`, params: { threshold } })
}
