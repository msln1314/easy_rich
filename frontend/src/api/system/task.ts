import request from '@/config/axios'

export const getTaskListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/system/tasks', params })
}

export const addTaskListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/system/tasks', data })
}

export const delTaskListApi = (dataId: string): Promise<IResponse> => {
  return request.delete({ url: `/system/tasks/${dataId}` })
}

export const putTaskListApi = (dataId: string, data: any): Promise<IResponse> => {
  return request.put({ url: `/system/tasks/${dataId}`, data })
}

export const getTaskApi = (dataId: string): Promise<IResponse> => {
  return request.get({ url: `/system/tasks/${dataId}` })
}

export const getTaskGroupOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/system/tasks/group/options' })
}

export const runOnceTaskApi = (dataId: string): Promise<IResponse> => {
  return request.post({ url: `/system/tasks/${dataId}/run` })
}
