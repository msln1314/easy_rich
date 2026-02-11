import request from '@/config/axios'

// 创建股票分组
export const createStockGroupApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_group', data })
}

// 获取用户分组树
export const getStockGroupTreeApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_group/tree', params })
}

// 获取用户分组列表
export const getStockGroupListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_group/list', params })
}

// 获取分组详情
export const getStockGroupDetailApi = (id: number): Promise<IResponse> => {
  return request.get({ url: `/stock/stock_group/${id}` })
}

// 更新股票分组
export const updateStockGroupApi = (id: number, data: any): Promise<IResponse> => {
  return request.put({ url: `/stock/stock_group/${id}`, data })
}

// 删除股票分组
export const deleteStockGroupApi = (ids: number[]): Promise<IResponse> => {
  return request.delete({ url: '/stock/stock_group', data: { ids } })
}

// 更新分组状态
export const updateStockGroupStatusApi = (id: number, status: number): Promise<IResponse> => {
  return request.put({ url: `/stock/stock_group/${id}/status`, data: { status } })
}
