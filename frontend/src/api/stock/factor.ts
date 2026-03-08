import request from '@/config/axios'

// Multi-factor stock selection APIs
export const calculateFactorApi = (stock: string): Promise<IResponse> => {
  return request.get({ url: '/stock/factor/calculate', params: { stock } })
}

export const batchCalculateFactorApi = (stocks: string[]): Promise<IResponse> => {
  return request.post({ url: '/stock/factor/batch', data: stocks })
}

export const factorRankingApi = (stocks: string): Promise<IResponse> => {
  return request.get({ url: '/stock/factor/ranking', params: { stocks } })
}
