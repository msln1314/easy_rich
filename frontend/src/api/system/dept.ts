import request from '@/config/axios'

export const getDeptListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/system/depts', params })
}

export const delDeptListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/system/depts', data })
}

export const addDeptListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/system/depts', data })
}

export const putDeptListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/system/depts/${data.id}`, data })
}

export const getDeptTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/system/depts/tree/options' })
}

export const getDeptUserTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/system/depts/user/tree/options' })
}
