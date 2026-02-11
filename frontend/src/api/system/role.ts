import request from '@/config/axios'

export const getRoleListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/system/roles', params })
}

export const addRoleListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/system/roles', data })
}

export const delRoleListApi = (data: any): Promise<IResponse> => {
  console.log('data', data)
  return request.delete({ url: '/system/roles', data })
}

export const putRoleListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/system/roles/${data.id}`, data })
}

export const getRoleApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/system/roles/${dataId}` })
}

export const getRoleOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: `/system/roles/options` })
}
