import request from '@/utils/request'

const API_PREFIX = '/portfolio'

export function getPortfolioList() {
  return request.get(API_PREFIX)
}

export function getPortfolioDetail(portfolioId: number) {
  return request.get(`${API_PREFIX}/${portfolioId}`)
}

export function createPortfolio(data: any) {
  return request.post(API_PREFIX, data)
}

export function updatePortfolio(portfolioId: number, data: any) {
  return request.put(`${API_PREFIX}/${portfolioId}`, data)
}

export function deletePortfolio(portfolioId: number) {
  return request.delete(`${API_PREFIX}/${portfolioId}`)
}

export function setDefaultPortfolio(portfolioId: number) {
  return request.put(`${API_PREFIX}/${portfolioId}/default`)
}

export function getPositionList(portfolioId: number) {
  return request.get(`${API_PREFIX}/position/${portfolioId}`)
}

export function addPosition(portfolioId: number, data: any) {
  return request.post(`${API_PREFIX}/position/${portfolioId}`, data)
}

export function deletePosition(portfolioId: number, stockCode: string) {
  return request.delete(`${API_PREFIX}/position/${portfolioId}/${stockCode}`)
}

export function getTradeList(portfolioId: number) {
  return request.get(`${API_PREFIX}/trade/${portfolioId}`)
}

export function recordBuy(portfolioId: number, data: any) {
  return request.post(`${API_PREFIX}/trade/${portfolioId}/buy`, data)
}

export function recordSell(portfolioId: number, data: any) {
  return request.post(`${API_PREFIX}/trade/${portfolioId}/sell`, data)
}

export function getPerformance(portfolioId: number) {
  return request.get(`${API_PREFIX}/analysis/${portfolioId}/performance`)
}

export function getPositionAnalysis(portfolioId: number) {
  return request.get(`${API_PREFIX}/analysis/${portfolioId}/positions`)
}

export function getTradeStatistics(portfolioId: number, days = 30) {
  return request.get(`${API_PREFIX}/analysis/${portfolioId}/trades`, { params: { days } })
}

export function getProfitAttribution(portfolioId: number) {
  return request.get(`${API_PREFIX}/analysis/${portfolioId}/attribution`)
}

export function createSnapshot(portfolioId: number, snapshotDate?: string) {
  return request.post(`${API_PREFIX}/analysis/${portfolioId}/snapshot`, null, {
    params: snapshotDate ? { snapshot_date: snapshotDate } : {}
  })
}

export function getRiskAlerts(portfolioId: number) {
  return request.get(`${API_PREFIX}/risk/${portfolioId}/alerts`)
}

export function checkRisk(portfolioId: number) {
  return request.post(`${API_PREFIX}/risk/${portfolioId}/check`)
}

export function checkDrawdown(portfolioId: number) {
  return request.get(`${API_PREFIX}/risk/${portfolioId}/drawdown`)
}

export function checkRebalance(portfolioId: number) {
  return request.get(`${API_PREFIX}/risk/${portfolioId}/rebalance`)
}

export function preTradeCheck(
  portfolioId: number,
  stockCode: string,
  tradeType: string,
  amount: number
) {
  return request.post(`${API_PREFIX}/risk/${portfolioId}/pre_check`, null, {
    params: { stock_code: stockCode, trade_type: tradeType, amount }
  })
}

export function handleAlert(alertId: number, handleNote?: string) {
  return request.put(`${API_PREFIX}/risk/alert/${alertId}/handle`, null, {
    params: handleNote ? { handle_note: handleNote } : {}
  })
}
