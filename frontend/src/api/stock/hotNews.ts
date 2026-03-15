import request from '@/config/axios'

export const getHotNewsSourcesApi = (params?: { column?: string }): Promise<IResponse> => {
  return request.get({ url: '/stock/hot-news/sources', params })
}

export const getHotNewsApi = (sourceId: string): Promise<IResponse> => {
  return request.get({ url: `/stock/hot-news/${sourceId}` })
}

export const getHotNewsBatchApi = (data: string[]): Promise<IResponse> => {
  return request.post({ url: '/stock/hot-news/batch', data })
}

export const getHotNewsByColumnApi = (column: string): Promise<IResponse> => {
  return request.get({ url: `/stock/hot-news/column/${column}` })
}
