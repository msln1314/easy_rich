import request from '@/config/axios'

export const stockPricePredictApi = (params: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_prediction/price_predict', data: params })
}
