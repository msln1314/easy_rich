import request from '@/config/axios'

export const getUserLoginDistributeApi = (): Promise<IResponse> => {
  return request.get({ url: '/record/analysis/user/login/distribute' })
}
