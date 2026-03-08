import request from '@/config/axios'

// Margin trading APIs
export const getMarginDetailApi = (stock: string, symbol = '融资融券'): Promise<IResponse> => {
  return request.get({ url: '/stock/margin/detail', params: { stock, symbol } })
}

export const getMarginMarketApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/margin/market' })
}

// Institution holding APIs
export const getInstitutionHoldingApi = (stock: string): Promise<IResponse> => {
  return request.get({ url: '/stock/institution/holding', params: { stock } })
}

// Research report APIs
export const getResearchReportApi = (symbol = '推荐'): Promise<IResponse> => {
  return request.get({ url: '/stock/research/report', params: { symbol } })
}
