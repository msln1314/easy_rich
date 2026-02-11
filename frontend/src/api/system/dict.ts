import request from '@/config/axios'

export const getDictTypeListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/system/dict/types', params })
}

export const addDictTypeListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/system/dict/types', data })
}

export const delDictTypeListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/system/dict/types', data })
}

export const putDictTypeListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/system/dict/types/${data.id}`, data })
}

export const getDictTypeApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/system/dict/types/${dataId}` })
}

export const getDictTypeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: `/system/dict/types/options` })
}

export const getDictTypeDictsApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/system/dict/type/dicts`, data })
}

export const getDictDetailsListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/system/dict', params })
}

export const addDictDetailsListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/system/dict', data })
}

export const delDictDetailsListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/system/dict', data })
}

export const putDictDetailsListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/system/dict/${data.id}`, data })
}

export const getDictDetailsApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/system/dict/${dataId}` })
}
