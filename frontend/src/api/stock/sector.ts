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

// 获取板块分析概览
export const getSectorAnalysisSummaryApi = (dateStr?: string): Promise<IResponse> => {
  return request.get({
    url: '/v1/stock/board_industry/sector/rotation/analysis/summary',
    params: { date_str: dateStr }
  })
}
