import request from '@/config/axios'

export const getStockHistoryApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_base/history', params })
}

export const getStockInfoApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_base/info', params })
}

export const getStockPageApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_base', params })
}

export const getStockDetailApi = (id: number): Promise<IResponse> => {
  return request.get({ url: `/stock/stock_base/${id}` })
}

export const createStockApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_base', data })
}

export const updateStockApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/stock/stock_base/${data.id}`, data })
}

export const deleteStockApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/stock/stock_base', data })
}

export const exportStockApi = (params: any, data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_base/export/excel', params, data })
}

// 个股排行相关接口
export const getStockRankingApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/ranking', params })
}

export const getRankingIndustriesApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/ranking/industries' })
}

export const getRankingMarketsApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/ranking/markets' })
}

export const syncRankingDataApi = (): Promise<IResponse> => {
  return request.post({ url: '/stock/ranking/sync' })
}
