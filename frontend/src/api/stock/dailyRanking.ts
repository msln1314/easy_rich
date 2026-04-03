import request from '@/config/axios'

enum Api {
  DAILY_RANKING = '/stock/daily-ranking',
  REALTIME_RANKING = '/stock/daily-ranking/realtime',
  HOT_RANKING = '/stock/daily-ranking/hot',
  RANKING_TREND = '/stock/daily-ranking/trend',
  RANKING_SUMMARY = '/stock/daily-ranking/summary',
  SYNC_RANKING = '/stock/daily-ranking/sync',
  INDUSTRIES = '/stock/daily-ranking/industries',
  HOT_DETAIL = '/stock/daily-ranking/hot-detail'
}

export interface RankingItem {
  rank: number
  stockCode: string
  stockName: string
  industry: string
  market: string
  currentPrice: number
  changePercent: number
  changeAmount: number
  volume: number
  amount: number
  turnoverRate: number
  totalMarketCap: number
}

export interface DailyRankingParams {
  rankingType: 'volume' | 'turnover' | 'amount' | 'change_percent' | 'hot'
  order?: 'desc' | 'asc'
  industry?: string
  market?: string
  stockCode?: string
  stockName?: string
  dataDate?: string
  page?: number
  pageSize?: number
}

export interface HotRankingItem {
  id: number
  stockCode: string
  stockName: string
  fullCode: string
  rank: number
  rankChange: number
  currentPrice: number
  changePercent: number
  hotValue: number
  volume: number
  amount: number
  turnoverRate: number
  fansCount: number
  viewCount: number
  commentCount: number
}

export interface RankingTrendItem {
  dataDate: string
  rank: number
  rankChange: number
  rankingValue: number
}

export interface RankingTrend {
  stockCode: string
  stockName: string
  rankingType: string
  trendData: RankingTrendItem[]
}

export interface RankingSummary {
  rankingType: string
  dataDate: string
  totalCount: number
  topStocks: Array<{
    rank: number
    stockCode: string
    stockName: string
    rankingValue: number
    rankingValueUnit: string
    changePercent: number
    currentPrice: number
  }>
}

export function getDailyRanking(params: DailyRankingParams) {
  return request.get({
    url: Api.DAILY_RANKING,
    params
  })
}

export function getRealtimeRanking(params: {
  rankingType: 'volume' | 'turnover' | 'amount' | 'change_percent'
  industry?: string
  market?: string
  limit?: number
}) {
  return request.get({
    url: Api.REALTIME_RANKING,
    params
  })
}

export function getHotRanking(params: {
  dataDate?: string
  market?: string
  industry?: string
  page?: number
  pageSize?: number
}) {
  return request.get({
    url: Api.HOT_RANKING,
    params
  })
}

export function getRankingTrend(params: {
  stockCode: string
  rankingType: 'volume' | 'turnover' | 'amount' | 'change_percent' | 'hot'
  startDate?: string
  endDate?: string
}) {
  return request.get({
    url: Api.RANKING_TREND,
    params
  })
}

export function getRankingSummary(params: {
  rankingType: 'volume' | 'turnover' | 'amount' | 'change_percent' | 'hot'
  dataDate?: string
  topN?: number
}) {
  return request.get({
    url: Api.RANKING_SUMMARY,
    params
  })
}

export function syncDailyRanking(params: { rankingTypes?: string[]; dataDate?: string }) {
  return request.post({
    url: Api.SYNC_RANKING,
    params
  })
}

export function getIndustries(rankingType: string) {
  return request.get({
    url: Api.INDUSTRIES,
    params: { rankingType }
  })
}

export function getHotDetail(stockCode: string, days: number = 7) {
  return request.get({
    url: `${Api.HOT_DETAIL}/${stockCode}`,
    params: { days }
  })
}
