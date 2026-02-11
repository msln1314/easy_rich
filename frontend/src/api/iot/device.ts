import request from '@/config/axios'

export const getDeviceListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/iot/devices', params })
}

export const addDeviceListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/iot/devices', data })
}

export const delDeviceListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/iot/devices', data })
}

export const putDeviceListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/iot/devices/${data.id}`, data })
}

export const getDeviceApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/iot/devices/${dataId}` })
}

export const postExportDeviceQueryListApi = (params: any, data: any): Promise<IResponse> => {
  return request.post({ url: `/iot/devices/export/query/list/to/excel`, params, data })
}

export const getImportTemplateApi = (): Promise<IResponse> => {
  return request.get({ url: `/iot/devices/download/import/template` })
}

export const postImportDeviceApi = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/iot/devices/import`,
    headersType: 'multipart/form-data',
    data
  })
}

export const postDeviceActionApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/iot/devices/action`, data })
}

export const getDeviceOptionsApi = (params?: any): Promise<IResponse> => {
  return request.get({ url: `/iot/devices/options`, params })
}
