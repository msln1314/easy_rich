import request from '@/config/axios'

export interface SectorRankingItem {
  rank: number
  sector_name: string
  sector_code: string
  change_rate: number
  volume: number
  turnover_rate: number
  leading_stocks: number
  stock_count: number
  market_cap: number
}

export interface SectorTrendData {
  date: string
  sectors: {
    [key: string]: {
      inflow: number
      outflow: number
      net_inflow: number
    }
  }
}

export interface SectorHeatmapItem {
  sector_name: string
  sector_code: string
  change_rate: number
  volume: number
  turnover_rate: number
  x?: number
  y?: number
  r?: number
}

export interface SectorRotationParams {
  start_date?: string
  end_date?: string
  sector_type?: string
}

export interface LeaderStock {
  code: string
  name: string
  price: number
  change_percent: number
  change: number
  volume: number
  amount: number
  turnover_rate: number
  score: number
  is_limit_up: boolean
}

export interface SectorLeader {
  sector_code: string
  sector_name: string
  sector_type: string
  leader_stock: LeaderStock | null
  second_leader: LeaderStock | null
  third_leader: LeaderStock | null
  change_percent: number
  up_count: number
  down_count: number
  limit_up_count: number
  limit_down_count: number
  active_stocks: number
  fund_inflow: number
  total_amount: number
  activity_score: number
}

export interface SectorRealtimeStatus {
  sector_code: string
  sector_name: string
  sector_type: string
  change_percent: number
  change: number
  price: number
  up_count: number
  down_count: number
  leading_stock: string
  leading_stock_change_percent: number
}

export interface SectorFactor {
  sector_code: string
  sector_name: string
  sector_type: string
  fund_flow_score: number
  sentiment_score: number
  technical_score: number
  pattern_score: number
  total_score: number
}

export interface RotationPrediction {
  prediction_id: string
  prediction_time: string
  target_date: string
  predictions: {
    rank: number
    sector_code: string
    sector_name: string
    probability: number
    confidence: number
    factors: {
      fund_flow: number
      sentiment: number
      technical: number
      pattern: number
    }
  }[]
  model_version: string
  confidence: number
}

export const getSectorRankingApi = (params: SectorRotationParams): Promise<IResponse> => {
  return request.get({
    url: '/v1/stock/board_industry/sector/rotation/ranking',
    params
  })
}

export const getSectorTrendApi = (params: SectorRotationParams): Promise<IResponse> => {
  return request.get({
    url: '/v1/stock/board_industry/sector/rotation/trend',
    params
  })
}

export const getSectorHeatmapApi = (params: SectorRotationParams): Promise<IResponse> => {
  return request.get({
    url: '/v1/stock/board_industry/sector/rotation/heatmap',
    params
  })
}

export const getSectorListApi = (): Promise<IResponse> => {
  return request.get({
    url: '/v1/stock/board_industry/sector/rotation/list'
  })
}

export const getSectorAnalysisSummaryApi = (dateStr?: string): Promise<IResponse> => {
  return request.get({
    url: '/v1/stock/board_industry/sector/rotation/analysis/summary',
    params: { date_str: dateStr }
  })
}

export const getSectorLeadersApi = (
  sectorType: string = 'industry',
  limit: number = 50
): Promise<IResponse> => {
  return request.get({
    url: '/v1/stock/board_industry/sector/leaders',
    params: { sector_type: sectorType, limit }
  })
}

export const getSectorLeaderByCodeApi = (
  boardCode: string,
  sectorType: string = 'industry'
): Promise<IResponse> => {
  return request.get({
    url: `/v1/stock/board_industry/sector/${boardCode}/leader`,
    params: { sector_type: sectorType }
  })
}

export const getSectorRealtimeStatusApi = (sectorType: string = 'industry'): Promise<IResponse> => {
  return request.get({
    url: '/v1/stock/board_industry/sector/realtime/status',
    params: { sector_type: sectorType }
  })
}

export const getSectorRotationHistoryApi = (
  boardCode: string,
  sectorType: string = 'industry',
  startDate?: string,
  endDate?: string
): Promise<IResponse> => {
  return request.get({
    url: `/v1/stock/board_industry/sector/rotation/history/${boardCode}`,
    params: { sector_type: sectorType, start_date: startDate, end_date: endDate }
  })
}

export const getSectorFactorsApi = (
  sectorType: string = 'industry',
  limit: number = 30
): Promise<IResponse> => {
  return request.get({
    url: '/v1/stock/board_industry/sector/factors',
    params: { sector_type: sectorType, limit }
  })
}

export const predictSectorRotationApi = (sectorType: string = 'industry'): Promise<IResponse> => {
  return request.get({
    url: '/v1/stock/board_industry/sector/rotation/predict',
    params: { sector_type: sectorType }
  })
}
