import request from '@/config/axios'

export const getWatchListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_watchlist', params })
}

export const delWatchListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/stock/stock_watchlist', data })
}

export const addWatchListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_watchlist', data })
}

export const putWatchListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/stock/stock_watchlist/${data.id}`, data })
}

export const getProductOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_watchlist/options' })
}

export const postExportWatchListApi = (params: any, data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_watchlist/export/excel', params, data })
}

export const getTagsListApi = (): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_watchlist/tags/list' })
}
