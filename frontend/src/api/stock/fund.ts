import request from '@/config/axios'

// ==================== 基金公司 API ====================

export const getFundCompanyListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/fund/companies', params })
}

export const getFundCompanyDetailApi = (companyCode: string): Promise<IResponse> => {
  return request.get({ url: `/stock/fund/companies/${companyCode}` })
}

// ==================== 主力分析 API ====================

export const getMainForceOverviewApi = (stockCode: string): Promise<IResponse> => {
  return request.get({ url: `/stock/fund/mainforce/${stockCode}/overview` })
}

export const getMainForceTrendApi = (stockCode: string, limit = 8): Promise<IResponse> => {
  return request.get({ url: `/stock/fund/mainforce/${stockCode}/trend`, params: { limit } })
}

export const getMainForceFundsApi = (stockCode: string, params: any): Promise<IResponse> => {
  return request.get({ url: `/stock/fund/mainforce/${stockCode}/funds`, params })
}

// ==================== 基金持仓 API ====================

export const getStockHoldingsApi = (stockCode: string, params: any): Promise<IResponse> => {
  return request.get({ url: `/stock/fund/holdings/stock/${stockCode}`, params })
}

export const getFundHoldingsApi = (fundCode: string, params: any): Promise<IResponse> => {
  return request.get({ url: `/stock/fund/holdings/fund/${fundCode}`, params })
}

// ==================== 主力预警 API ====================

export const getMainForceAlertsApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/fund/alerts', params })
}

export const createMainForceAlertApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/fund/alerts', data })
}

export const markAlertReadApi = (alertId: number): Promise<IResponse> => {
  return request.put({ url: `/stock/fund/alerts/${alertId}/read` })
}

// ==================== 数据同步 API ====================

export const syncStockMainForceApi = (stockCode: string): Promise<IResponse> => {
  return request.post({ url: `/stock/fund/sync/stock/${stockCode}` })
}

export const syncFundPortfolioApi = (fundCode: string, reportDate?: string): Promise<IResponse> => {
  const params = reportDate ? { report_date: reportDate } : {}
  return request.post({ url: `/stock/fund/sync/fund/${fundCode}`, params })
}

export const syncFundCompaniesApi = (): Promise<IResponse> => {
  return request.post({ url: '/stock/fund/sync/companies' })
}
