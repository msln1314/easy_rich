import request from '@/config/axios'

// Limit up/down APIs
export const getZtPoolApi = (date?: string): Promise<IResponse> => {
  return request.get({ url: '/stock/limit_up/pool', params: { date } })
}

export const getZtPoolSubApi = (date?: string): Promise<IResponse> => {
  return request.get({ url: '/stock/limit_down/pool', params: { date } })
}

export const getZtPoolStrongApi = (date?: string): Promise<IResponse> => {
  return request.get({ url: '/stock/limit_up/strong', params: { date } })
}

export const getZtPoolZbgcApi = (date?: string): Promise<IResponse> => {
  return request.get({ url: '/stock/limit_up/broken', params: { date } })
}

export const getLimitUpStatisticsApi = (date?: string): Promise<IResponse> => {
  return request.get({ url: '/stock/limit_up/statistics', params: { date } })
}
