import request from '@/config/axios'

export const getMenuListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/system/menus', params })
}

export const delMenuListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/system/menus', data })
}

export const addMenuListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/system/menus', data })
}

export const putMenuListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/system/menus/${data.id}`, data })
}

export const getMenuTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/system/menus/tree/options' })
}

export const getMenuRoleTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/system/menus/role/tree/options' })
}

export const getMenuRoutesApi = (): Promise<IResponse<AppCustomRouteRecordRaw[]>> => {
  return request.get({ url: '/system/menus/routes' })
}
