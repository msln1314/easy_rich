import request from '@/config/axios'

export const getClientGroupListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/iot/client_groups', params })
}

export const delClientGroupListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/iot/client_groups', data })
}

export const addClientGroupListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/iot/client_groups', data })
}

export const putClientGroupListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/iot/client_groups/${data.id}`, data })
}

export const getClientGroupTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/iot/client_groups/tree/options' })
}

export const getClientGroupUserTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/iot/client_groups/user/tree/options' })
}
