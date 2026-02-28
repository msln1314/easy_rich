import request from '@/config/axios'

export const getMonitorConditionListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_monitor_condition', params })
}

export const delMonitorConditionApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/stock/stock_monitor_condition', data })
}

export const addMonitorConditionApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_monitor_condition', data })
}

export const putMonitorConditionApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/stock/stock_monitor_condition/${data.id}`, data })
}

export const getActiveConditionsApi = (user_id?: number): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_monitor_condition/options', params: { user_id } })
}

export const updateActiveStatusApi = (data: any): Promise<IResponse> => {
  return request.put({
    url: `/stock/stock_monitor_condition/${data.id}/active`,
    data: { is_active: data.is_active }
  })
}

export const postExportMonitorConditionApi = (params: any, data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_monitor_condition/export/excel', params, data })
}
