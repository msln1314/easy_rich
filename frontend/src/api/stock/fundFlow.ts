import request from '@/config/axios'

// Fund flow APIs
export const getIndividualFundFlowApi = (stock: string, market = 'sh'): Promise<IResponse> => {
  return request.get({ url: '/stock/fund_flow/individual', params: { stock, market } })
}

export const getMarketFundFlowApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/fund_flow/market' })
}

export const getSectorFundFlowApi = (sectorType = '行业资金流'): Promise<IResponse> => {
  return request.get({ url: '/stock/fund_flow/sector', params: { sector_type: sectorType } })
}

export const getNorthFundFlowApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/fund_flow/north' })
}

export const getNorthHoldingApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/fund_flow/north_holding' })
}

export const getLhbApi = (date?: string): Promise<IResponse> => {
  return request.get({ url: '/stock/fund_flow/lhb', params: { date } })
}
