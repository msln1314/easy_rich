import request from '@/config/axios'

export const getTaskRecordListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/logs/tasks', params })
}
