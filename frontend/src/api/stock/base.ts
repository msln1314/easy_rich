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
