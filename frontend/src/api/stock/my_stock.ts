import request from '@/config/axios'

// 获取我的自选股列表
export const getMyStocksApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/my_stock', params })
}

// 添加股票到分组
export const addStockToGroupApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/my_stock', data })
}

// 批量添加股票到分组
export const batchAddStocksToGroupApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/my_stock/batch', data })
}

// 从分组中移除股票
export const removeStockFromGroupApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/stock/my_stock', data })
}

// 移动股票到其他分组
export const moveStockToGroupApi = (data: any): Promise<IResponse> => {
  return request.put({ url: '/stock/my_stock/move', data })
}

// 获取各分组股票数量
export const getStockCountByGroupApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/my_stock/count', params })
}
