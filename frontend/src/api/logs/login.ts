import request from '@/config/axios'

export const getLogLoginListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/logs/logins', params })
}
