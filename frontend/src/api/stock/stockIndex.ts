import { defHttp } from '/@/utils/http/axios'

enum Api {
  INDEX_QUOTE = '/stock/index/quote',
  INDEX_HISTORY = '/stock/index/history',
  MARKET_SUMMARY = '/stock/index/market/summary',
  REALTIME_RANKINGS = '/stock/index/realtime/rankings',
  FUND_FLOW = '/stock/index/fund-flow'
}

export interface IndexQuoteItem {
  indexCode: string
  indexName: string
  currentPrice: number | null
  changePercent: number | null
  changeAmount: number | null
  volume: number | null
  amount: number | null
}

export interface IndexQuoteResponse {
  items: IndexQuoteItem[]
  updateTime: string
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
  totalStocks: number
  upStocks: number
  downStocks: number
  flatStocks: number
  totalAmount: number
  totalVolume: number
  limitUpCount: number
  limitDownCount: number
  tradeDate: string
  updateTime: string
}

export interface StockRankingItem {
  rank: number
  stockCode: string
  stockName: string
  currentPrice: number | null
  changePercent: number | null
  volume: number | null
  amount: number | null
  turnoverRate: number | null
  industry: string | null
  market: string | null
}

export interface RealtimeRankings {
  changePercentRanking: StockRankingItem[]
  turnoverRanking: StockRankingItem[]
  volumeRanking: StockRankingItem[]
  amountRanking: StockRankingItem[]
  updateTime: string
}

export function getIndexQuote() {
  return defHttp.get<IndexQuoteResponse>({
    url: Api.INDEX_QUOTE
  })
}

export function getIndexHistory(params: {
  indexCode: string
  period?: string
  startDate?: string
  endDate?: string
}) {
  return defHttp.get<IndexHistoryItem[]>({
    url: Api.INDEX_HISTORY,
    params
  })
}

export function getMarketSummary() {
  return defHttp.get<MarketSummary>({
    url: Api.MARKET_SUMMARY
  })
}

export function getRealtimeRankings(limit: number = 20) {
  return defHttp.get<RealtimeRankings>({
    url: Api.REALTIME_RANKINGS,
    params: { limit }
  })
}

export function getFundFlow(period: string = 'daily') {
  return defHttp.get({
    url: Api.FUND_FLOW,
    params: { period }
  })
}
