import request from '@/config/axios'

export const getMonitorStrategyListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_monitor_strategy', params })
}

export const delMonitorStrategyApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/stock/stock_monitor_strategy', data })
}

export const addMonitorStrategyApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_monitor_strategy', data })
}

export const putMonitorStrategyApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/stock/stock_monitor_strategy/${data.id}`, data })
}

export const getMonitorStrategyDetailApi = (id: number): Promise<IResponse> => {
  return request.get({ url: `/stock/stock_monitor_strategy/${id}` })
}

export const updateMonitorStrategyActiveApi = (data: any): Promise<IResponse> => {
  return request.put({
    url: `/stock/stock_monitor_strategy/${data.id}/active`,
    data: { is_active: data.is_active }
  })
}

export const postExportMonitorStrategyApi = (params: any, data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_monitor_strategy/export/excel', params, data })
}

export const getMonitorStrategyLogsApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_monitor_log', params })
}
