import request from '@/config/axios'

enum Api {
  OVERVIEW = '/aggregate/overview',
  FULL = '/aggregate/full',
  REALTIME = '/aggregate/realtime',
  TECHNICAL = '/aggregate/technical',
  FUND = '/aggregate/fund',
  INFO = '/aggregate/info'
}

// 股票聚合概览
export function getStockOverview(stockCode: string) {
  return request.get({
    url: `${Api.OVERVIEW}/${stockCode}`
  })
}

// 股票完整聚合数据
export function getStockFullData(stockCode: string) {
  return request.get({
    url: `${Api.FULL}/${stockCode}`
  })
}

// 实时聚合数据
export function getRealtimeData(stockCode: string) {
  return request.get({
    url: `${Api.REALTIME}/${stockCode}`
  })
}

// 技术分析聚合数据
export function getTechnicalData(stockCode: string, days: number = 60) {
  return request.get({
    url: `${Api.TECHNICAL}/${stockCode}`,
    params: { days }
  })
}

// 资金相关聚合数据
export function getFundData(stockCode: string) {
  return request.get({
    url: `${Api.FUND}/${stockCode}`
  })
}

// 资讯相关聚合数据
export function getInfoData(stockCode: string) {
  return request.get({
    url: `${Api.INFO}/${stockCode}`
  })
}
