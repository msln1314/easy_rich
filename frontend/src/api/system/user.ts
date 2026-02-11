import request from '@/config/axios'

export const getUserListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/system/users', params })
}

export const addUserListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/system/users', data })
}

export const delUserListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/system/users', data })
}

export const putUserListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/system/users/${data.id}`, data })
}

export const getUserApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/system/users/${dataId}` })
}

export const postCurrentUserUpdatePassword = (data: any): Promise<IResponse> => {
  return request.post({ url: `/system/users/current/update/password`, data })
}

export const postCurrentUserUpdateInfo = (data: any): Promise<IResponse> => {
  return request.post({ url: `/system/users/current/update/info`, data })
}

export const getCurrentAdminUserInfo = (): Promise<IResponse> => {
  return request.get({ url: `/system/users/admin/current/info` })
}

export const postExportUserQueryListApi = (params: any, data: any): Promise<IResponse> => {
  return request.post({ url: `/system/users/export/query/list/to/excel`, params, data })
}

export const getImportTemplateApi = (): Promise<IResponse> => {
  return request.get({ url: `/system/users/download/import/template` })
}

export const postImportUserApi = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/system/users/import`,
    headersType: 'multipart/form-data',
    data
  })
}

export const postUsersInitPasswordSendSMSApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/system/users/init/password/send/sms`, data })
}

export const postUsersInitPasswordSendEmailApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/system/users/init/password/send/email`, data })
}

export const postUsersInitPasswordReserApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/system/users/init/password/reset`, data })
}
