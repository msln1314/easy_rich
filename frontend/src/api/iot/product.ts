import request from '@/config/axios'

export const getClientGroupListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/iot/products', params })
}

export const delClientGroupListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/iot/products', data })
}

export const addClientGroupListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/iot/products', data })
}

export const putClientGroupListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/iot/products/${data.id}`, data })
}

export const getProductOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/iot/products/options' })
}
