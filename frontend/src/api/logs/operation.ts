import request from '@/config/axios'

export const getLogOperationListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/logs/operations', params })
}
