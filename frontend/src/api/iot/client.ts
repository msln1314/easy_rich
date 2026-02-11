import request from '@/config/axios'

export const getClientListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/iot/clients', params })
}

export const addClientListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/iot/clients', data })
}

export const delClientListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/iot/clients', data })
}

export const putClientListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/iot/clients/${data.id}`, data })
}
export const putClientBindApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/iot/clients/bind/${data.id}`, data })
}
export const putClientUnBindApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/iot/clients/unbind/${data.id}` })
}
export const putPortStatusApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/iot/clients/status/${data.id}`, data })
}

export const getClientApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/iot/clients/${dataId}` })
}

export const postExportClientQueryListApi = (params: any, data: any): Promise<IResponse> => {
  return request.post({ url: `/iot/clients/export/excel`, params, data })
}

export const getImportTemplateApi = (): Promise<IResponse> => {
  return request.get({ url: `/iot/clients/download/import/template` })
}

export const postImportClientApi = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/iot/clients/import`,
    headersType: 'multipart/form-data',
    data
  })
}

export const postClientsActionApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/iot/clients/action`, data })
}
