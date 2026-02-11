import request from '@/config/axios'

// 常见问题类别
export const getIssueCategoryListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/help/issue/categorys', params })
}

export const addIssueCategoryApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/help/issue/categorys', data })
}

export const delIssueCategoryListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/help/issue/categorys', data })
}

export const putIssueCategoryApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/help/issue/categorys/${data.id}`, data })
}

export const getIssueCategoryApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/help/issue/categorys/${dataId}` })
}

export const getIssueCategoryOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: `/help/issue/categorys/options` })
}

// 常见问题
export const getIssueListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/help/issues', params })
}

export const addIssueApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/help/issues', data })
}

export const delIssueListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/help/issues', data })
}

export const putIssueApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/help/issues/${data.id}`, data })
}

export const getIssueApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/help/issues/${dataId}` })
}
