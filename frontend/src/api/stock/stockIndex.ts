import request from '@/config/axios'

enum Api {
  INDEX_QUOTES = '/stock/index/quote',
  INDEX_DETAIL = '/stock/index',
  INDEX_HISTORY = '/stock/index/history',
  MARKET_SUMMARY = '/stock/index/market/summary',
  REALTIME_RANKINGS = '/stock/index/realtime/rankings',
  FUND_FLOW = '/stock/index/fund-flow',
  // 资金流向相关 - stock-service
  NORTH_MONEY_REALTIME = '/stock/index/fund-flow/north-money/realtime',
  NORTH_MONEY_FLOW = '/stock/index/fund-flow/north-money/flow',
  MARKET_FLOW_TODAY = '/stock/index/fund-flow/market/flow/today',
  MARKET_FLOW = '/stock/index/fund-flow/market/flow'
}

export interface IndexQuoteItem {
  index_code: string
  index_name: string
  close_price: number | null
  change_percent: number | null
  change_amount: number | null
  volume: number | null
  amount: number | null
}

export interface IndexQuotesResponse {
  items: IndexQuoteItem[]
  update_time: string
}

export interface IndexHistoryItem {
  date: string
  open: number | null
  high: number | null
  low: number | null
  close: number | null
  volume: number | null
  amount: number | null
}

export interface MarketSummary {
  indices: IndexQuoteItem[]
  total_stocks: number
  up_stocks: number
  down_stocks: number
  flat_stocks: number
  total_amount: number
  total_volume: number
  limit_up_count: number
  limit_down_count: number
  trade_date: string
  update_time: string
}

export interface StockRankingItem {
  rank: number
  stock_code: string
  stock_name: string
  current_price: number | null
  change_percent: number | null
  volume: number | null
  amount: number | null
  turnover_rate: number | null
  industry: string | null
  market: string | null
}

export interface RealtimeRankings {
  change_percent_ranking: StockRankingItem[]
  turnover_ranking: StockRankingItem[]
  volume_ranking: StockRankingItem[]
  amount_ranking: StockRankingItem[]
  update_time: string
}

// 北向资金相关接口
export interface NorthMoneyRealtime {
  sh_hk_flow: number
  sz_hk_flow: number
  total_flow: number
  date: string
  time: string
  update_time: string
}

export interface MarketFundFlowToday {
  date: string
  sh_close: number | null
  sh_change: number | null
  sz_close: number | null
  sz_change: number | null
  main_net_inflow: number
  main_net_inflow_pct: number
  super_large_net_inflow: number
  large_net_inflow: number
  medium_net_inflow: number
  small_net_inflow: number
}

export interface NorthMoneyFlowItem {
  date: string
  time: string
  sh_hk_flow: number
  sz_hk_flow: number
  total_flow: number
}

// 指数行情接口
export const getIndexQuotesApi = (): Promise<IResponse> => {
  return request.get({ url: Api.INDEX_QUOTES })
}

export const getIndexDetailApi = (indexCode: string): Promise<IResponse> => {
  return request.get({ url: `${Api.INDEX_DETAIL}/${indexCode}` })
}

export const getIndexHistoryApi = (params: {
  indexCode: string
  period?: string
  startDate?: string
  endDate?: string
}): Promise<IResponse> => {
  return request.get({ url: Api.INDEX_HISTORY, params })
}

export const getMarketSummaryApi = (): Promise<IResponse> => {
  return request.get({ url: Api.MARKET_SUMMARY })
}

export const getRealtimeRankingsApi = (limit: number = 20): Promise<IResponse> => {
  return request.get({ url: Api.REALTIME_RANKINGS, params: { limit } })
}

export const getFundFlowApi = (period: string = 'daily'): Promise<IResponse> => {
  return request.get({ url: Api.FUND_FLOW, params: { period } })
}

// 北向资金接口
export const getNorthMoneyRealtimeApi = (): Promise<IResponse> => {
  return request.get({ url: Api.NORTH_MONEY_REALTIME })
}

export const getNorthMoneyFlowApi = (days: number = 30): Promise<IResponse> => {
  return request.get({ url: Api.NORTH_MONEY_FLOW, params: { days } })
}

export const getMarketFundFlowTodayApi = (): Promise<IResponse> => {
  return request.get({ url: Api.MARKET_FLOW_TODAY })
}

export const getMarketFundFlowApi = (days: number = 30): Promise<IResponse> => {
  return request.get({ url: Api.MARKET_FLOW, params: { days } })
}
