import request from '@/config/axios'

export const getLogActionListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/logs/actions', params })
}
