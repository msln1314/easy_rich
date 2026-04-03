// frontend/src/api/stock/qmt.ts
import request from '@/config/axios'

const QMT_BASE_URL = '/qmt'

// ==================== 交易相关 ====================

/**
 * 下单
 */
export const placeOrderApi = (data: {
  stock_code: string
  direction: 'buy' | 'sell'
  price?: number
  quantity: number
  order_type?: 'limit' | 'market'
}): Promise<IResponse> => {
  return request.post({ url: `${QMT_BASE_URL}/trade/order`, data })
}

/**
 * 撤单
 */
export const cancelOrderApi = (orderId: string): Promise<IResponse> => {
  return request.delete({ url: `${QMT_BASE_URL}/trade/order/${orderId}` })
}

/**
 * 查询委托列表
 */
export const getOrdersApi = (params?: {
  status?: string
  date?: string
}): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/trade/orders`, params })
}

/**
 * 查询委托详情
 */
export const getOrderDetailApi = (orderId: string): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/trade/orders/${orderId}` })
}

// ==================== 持仓相关 ====================

/**
 * 查询持仓列表
 */
export const getPositionsApi = (): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/position/list` })
}

/**
 * 查询资金余额
 */
export const getBalanceApi = (): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/position/balance` })
}

/**
 * 查询成交记录
 */
export const getTradesApi = (params?: {
  date?: string
  stock_code?: string
}): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/position/trades`, params })
}

/**
 * 查询今日成交
 */
export const getTodayTradesApi = (): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/position/trades/today` })
}

// ==================== 服务状态 ====================

/**
 * 健康检查
 */
export const getQMTHealthApi = (): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/health` })
}