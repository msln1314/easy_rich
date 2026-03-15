import request from '@/config/axios'

export interface MonitorStrategyParams {
  page?: number
  pageSize?: number
  name?: string
  tag?: string
  stock_code?: string
  stock_name?: string
  user_id?: number
  is_active?: number
  strategy_type?: string
  priority?: number
  reason?: string
  notify_enabled?: number
}

export interface MonitorStrategyCreate {
  name: string
  tag?: string
  stock_code?: string
  stock_name?: string
  strategy_type: string
  condition_content?: string
  trigger_value_min?: number
  trigger_value_max?: number
  trigger_percent_min?: number
  trigger_percent_max?: number
  cooldown_minutes?: number
  cooldown_type?: string
  is_active?: number
  priority?: number
  reason?: string
  remark?: string
  notify_enabled?: number
  notify_method?: string
  notify_trigger_count?: number
  notify_type?: string
  strategy_config?: string
}

export interface MonitorStrategyUpdate extends Partial<MonitorStrategyCreate> {
  id: number
}

export const getMonitorStrategyListApi = (params: MonitorStrategyParams): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_monitor_strategy', params })
}

export const delMonitorStrategyApi = (ids: number[]): Promise<IResponse> => {
  return request.delete({ url: '/stock/stock_monitor_strategy', data: { ids } })
}

export const addMonitorStrategyApi = (data: MonitorStrategyCreate): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_monitor_strategy', data })
}

export const putMonitorStrategyApi = (data: MonitorStrategyUpdate): Promise<IResponse> => {
  return request.put({ url: `/stock/stock_monitor_strategy/${data.id}`, data })
}

export const getMonitorStrategyDetailApi = (id: number): Promise<IResponse> => {
  return request.get({ url: `/stock/stock_monitor_strategy/${id}` })
}

export const updateMonitorStrategyActiveApi = (
  id: number,
  is_active: number
): Promise<IResponse> => {
  return request.put({
    url: `/stock/stock_monitor_strategy/${id}/active`,
    data: { is_active }
  })
}

export const updateMonitorStrategyPriorityApi = (
  id: number,
  priority: number
): Promise<IResponse> => {
  return request.put({
    url: `/stock/stock_monitor_strategy/${id}/priority`,
    data: { priority }
  })
}

export const postExportMonitorStrategyApi = (
  params: MonitorStrategyParams,
  header: any[]
): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_monitor_strategy/export/excel', params, data: header })
}

export const getMonitorStrategyLogsApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_monitor_log', params })
}

export const getActiveStrategiesApi = (user_id?: number): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_monitor_strategy/options', params: { user_id } })
}

export const getStrategyStatisticsApi = (user_id?: number): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_monitor_strategy/statistics', params: { user_id } })
}

export const getStrategiesByStockCodeApi = (stock_code: string): Promise<IResponse> => {
  return request.get({ url: `/stock/stock_monitor_strategy/by_stock/${stock_code}` })
}

export const STRATEGY_TYPE_OPTIONS = [
  { value: 'limit_up', label: '涨停' },
  { value: 'limit_down', label: '跌停' },
  { value: 'open_board', label: '开板' },
  { value: 'turnover', label: '换手' },
  { value: 'breakout', label: '突破' },
  { value: 'rebound', label: '反弹' }
]

export const COOLDOWN_TYPE_OPTIONS = [
  { value: 'same_day', label: '同一天内一次' },
  { value: 'interval', label: '按间隔时间触发' }
]

export const NOTIFY_METHOD_OPTIONS = [
  { value: 'system', label: '系统消息' },
  { value: 'email', label: '邮件' },
  { value: 'sms', label: '短信' },
  { value: 'wechat', label: '微信' }
]

export const NOTIFY_TYPE_OPTIONS = [
  { value: 'once', label: '仅一次' },
  { value: 'always', label: '每次都推送' },
  { value: 'interval', label: '按间隔推送' }
]

export const PRIORITY_OPTIONS = [
  { value: 1, label: '高' },
  { value: 2, label: '中' },
  { value: 3, label: '低' }
]
