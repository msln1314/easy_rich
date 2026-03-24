import request from '@/config/axios'

const API_PREFIX = '/stock/portfolio'

export function getPortfolioList() {
  return request.get({ url: API_PREFIX })
}

export function getPortfolioDetail(portfolioId: number) {
  return request.get({ url: `${API_PREFIX}/${portfolioId}` })
}

export function createPortfolio(data: any) {
  return request.post({ url: API_PREFIX, data })
}

export function updatePortfolio(portfolioId: number, data: any) {
  return request.put({ url: `${API_PREFIX}/${portfolioId}`, data })
}

export function deletePortfolio(portfolioId: number) {
  return request.delete({ url: `${API_PREFIX}/${portfolioId}` })
}

export function setDefaultPortfolio(portfolioId: number) {
  return request.put({ url: `${API_PREFIX}/${portfolioId}/default` })
}

export function getPositionList(portfolioId: number) {
  return request.get({ url: `${API_PREFIX}/position/${portfolioId}` })
}

export function addPosition(portfolioId: number, data: any) {
  return request.post({ url: `${API_PREFIX}/position/${portfolioId}`, data })
}

export function deletePosition(portfolioId: number, stockCode: string) {
  return request.delete({ url: `${API_PREFIX}/position/${portfolioId}/${stockCode}` })
}

export function getTradeList(portfolioId: number) {
  return request.get({ url: `${API_PREFIX}/trade/${portfolioId}` })
}

export function recordBuy(portfolioId: number, data: any) {
  return request.post({ url: `${API_PREFIX}/trade/${portfolioId}/buy`, data })
}

export function recordSell(portfolioId: number, data: any) {
  return request.post({ url: `${API_PREFIX}/trade/${portfolioId}/sell`, data })
}

export function getPerformance(portfolioId: number) {
  return request.get({ url: `${API_PREFIX}/analysis/${portfolioId}/performance` })
}

export function getPositionAnalysis(portfolioId: number) {
  return request.get({ url: `${API_PREFIX}/analysis/${portfolioId}/positions` })
}

export function getTradeStatistics(portfolioId: number, days = 30) {
  return request.get({ url: `${API_PREFIX}/analysis/${portfolioId}/trades`, params: { days } })
}

export function getProfitAttribution(portfolioId: number) {
  return request.get({ url: `${API_PREFIX}/analysis/${portfolioId}/attribution` })
}

export function createSnapshot(portfolioId: number, snapshotDate?: string) {
  return request.post({
    url: `${API_PREFIX}/analysis/${portfolioId}/snapshot`,
    data: snapshotDate ? { snapshot_date: snapshotDate } : {}
  })
}

export function getRiskAlerts(portfolioId: number) {
  return request.get({ url: `${API_PREFIX}/risk/${portfolioId}/alerts` })
}

export function checkRisk(portfolioId: number) {
  return request.post({ url: `${API_PREFIX}/risk/${portfolioId}/check` })
}

export function checkDrawdown(portfolioId: number) {
  return request.get({ url: `${API_PREFIX}/risk/${portfolioId}/drawdown` })
}

export function checkRebalance(portfolioId: number) {
  return request.get({ url: `${API_PREFIX}/risk/${portfolioId}/rebalance` })
}

export function preTradeCheck(
  portfolioId: number,
  stockCode: string,
  tradeType: string,
  amount: number
) {
  return request.post({
    url: `${API_PREFIX}/risk/${portfolioId}/pre_check`,
    data: { stock_code: stockCode, trade_type: tradeType, amount }
  })
}

export function handleAlert(alertId: number, handleNote?: string) {
  return request.put({
    url: `${API_PREFIX}/risk/alert/${alertId}/handle`,
    data: handleNote ? { handle_note: handleNote } : {}
  })
}
