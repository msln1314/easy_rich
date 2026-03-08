import request from '@/config/axios'

// Composite score APIs
export const getCompositeScoreApi = (stock: string): Promise<IResponse> => {
  return request.get({ url: '/stock/composite/score', params: { stock } })
}

export const batchCompositeScoreApi = (stocks: string): Promise<IResponse> => {
  return request.get({ url: '/stock/composite/batch', params: { stocks } })
}
