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
  MARKET_FLOW = '/stock/index/fund-flow/market/flow',
  // 龙虎榜相关
  LONGHUBANG_LIST = '/stock/longhubang/list',
  LONGHUBANG_DETAIL = '/stock/longhubang/detail',
  LONGHUBANG_STATISTICS = '/stock/longhubang/statistics',
  LONGHUBANG_TOP_BROKERS = '/stock/longhubang/broker/top'
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

export interface LonghubangItem {
  id: number
  trade_date: string
  stock_code: string
  stock_name: string
  full_code: string
  market: string
  close_price: number | null
  change_percent: number | null
  turnover_rate: number | null
  total_amount: number | null
  net_buy_amount: number | null
  net_buy_ratio: number | null
  reason: string | null
  buy_amount_total: number | null
  sell_amount_total: number | null
}

export interface LonghubangDetail {
  id: number
  broker_name: string
  broker_type: string | null
  buy_amount: number | null
  sell_amount: number | null
  net_amount: number | null
}

export interface LonghubangDetailResponse extends LonghubangItem {
  buy_details: LonghubangDetail[]
  sell_details: LonghubangDetail[]
}

export interface LonghubangStatistics {
  trade_date: string
  total_count: number
  up_count: number
  down_count: number
  limit_up_count: number
  limit_down_count: number
  total_net_buy: number
}

export interface LonghubangTopBroker {
  broker_name: string
  broker_type: string | null
  appear_count: number
  total_buy: number
  total_sell: number
  total_net: number
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

export const getLonghubangListApi = (params: {
  trade_date?: string
  stock_code?: string
  stock_name?: string
  page?: number
  page_size?: number
}): Promise<IResponse> => {
  return request.get({ url: Api.LONGHUBANG_LIST, params })
}

export const getLonghubangDetailApi = (lhbId: number): Promise<IResponse> => {
  return request.get({ url: `${Api.LONGHUBANG_DETAIL}/${lhbId}` })
}

export const getLonghubangStatisticsApi = (tradeDate?: string): Promise<IResponse> => {
  return request.get({ url: Api.LONGHUBANG_STATISTICS, params: { trade_date: tradeDate } })
}

export const getLonghubangTopBrokersApi = (params: {
  trade_date?: string
  limit?: number
}): Promise<IResponse> => {
  return request.get({ url: Api.LONGHUBANG_TOP_BROKERS, params })
}

export interface LimitPoolItem {
  rank: number
  stock_code: string
  stock_name: string
  close_price: number
  change_percent: number
  turnover_rate: number
  continuous_days: number | null
  open_count: number | null
  amount: number
  reason: string | null
}

export interface SectorHotItem {
  board_code: string
  board_name: string
  change_percent: number
  up_count: number
  down_count: number
  leading_stock: string | null
  leading_stock_change: number | null
}

export interface MarketSentiment {
  zt_count: number
  dt_count: number
  max_continuous: number
  continuous_stats: Record<number, number>
  zt_dt_ratio: number
  sentiment_score: number
  sentiment_level: string
}

export interface MarginSummary {
  rzye: number
  rqye: number
  rzmre: number
  rqmcl: number
  rzche: number
  rqchl: number
}

export const getLimitPoolApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/limit-pool' })
}

export const getSectorHotApi = (
  sectorType: string = 'industry',
  limit: number = 10
): Promise<IResponse> => {
  return request.get({
    url: '/stock/dashboard/sector-hot',
    params: { sector_type: sectorType, limit }
  })
}

export const getMarginSummaryApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/margin-summary' })
}

export const getHotStocksApi = (limit: number = 10): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/hot-stocks', params: { limit } })
}

export const getMarketSentimentApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/market-sentiment' })
}

export const getAllDashboardDataApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/all-dashboard-data' })
}

// ETF资金流向
export interface ETFFlowItem {
  rank: number
  etf_code: string
  etf_name: string
  net_flow: number | null
  subscribe_amount: number | null
  redeem_amount: number | null
  trade_date: string
}

export const getETFFlowOverviewApi = (top: number = 10): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/etf/overview', params: { top } })
}

export const getETFFlowRankApi = (top: number = 20): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/etf/net-flow', params: { top } })
}

// 全球指数
export interface GlobalIndexItem {
  index_code: string
  index_name: string
  price: number | null
  change: number | null
  change_percent: number | null
  update_time: string
}

export const getGlobalIndicesApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/index/global' })
}

// 恐慌贪婪指数
export interface FearGreedIndex {
  index: number
  status: string
  status_en: string
  components: Record<string, number>
  update_time: string
}

export const getFearGreedIndexApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/sentiment/fear-greed' })
}

// 南向资金
export interface SouthMoneyData {
  sh_hk_flow: number
  sz_hk_flow: number
  total_flow: number
  date: string
  time: string
  update_time: string
}

export const getSouthMoneyRealtimeApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/south-money/realtime' })
}

// 涨停池数据 - 用于涨停热力图
export interface LimitUpPoolItem {
  stock_code: string
  stock_name: string
  industry?: string
  concept?: string
  limit_up_time?: string
  seal_amount?: number
  continuous_days?: number
  change_percent?: number
}

export interface LimitUpPoolResponse {
  limit_up_list: LimitUpPoolItem[]
  limit_down_count: number
  update_time: string
}

export const getLimitUpPoolApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/limit-up-pool' })
}

// 涨跌分布数据
export interface UpDownDistribution {
  limitUp: number
  highUp: number
  mediumUp: number
  lowUp: number
  flat: number
  lowDown: number
  mediumDown: number
  highDown: number
  limitDown: number
  upTotal: number
  downTotal: number
  flatTotal: number
  update_time: string
}

export const getUpDownDistributionApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/dashboard/up-down-distribution' })
}
