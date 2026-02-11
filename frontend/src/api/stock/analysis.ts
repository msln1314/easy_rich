import request from '@/config/axios'

export const createStockAnalysisApi = (params: any): Promise<IResponse> => {
  return request.post({ url: '/stock/stock_analysis', data: params })
}

export const getStockAnalysisListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/stock_analysis', params })
}

export const deleteStockAnalysisApi = (ids: any): Promise<IResponse> => {
  return request.delete({ url: '/stock/stock_analysis', data: ids })
}

export const getStockAnalysisDetailApi = (id: number): Promise<IResponse> => {
  return request.get({ url: `/stock/stock_analysis/${id}` })
}

export const updateStockAnalysisApi = (id: number, data: any): Promise<IResponse> => {
  return request.put({ url: `/stock/stock_analysis/${id}`, data })
}

export const getAnalysisByStockCodeApi = (
  stockCode: string,
  limit: number = 10
): Promise<IResponse> => {
  return request.get({ url: `/stock/stock_analysis/stock/${stockCode}`, params: { limit } })
}

export const getAnalysisByResultApi = (result: string): Promise<IResponse> => {
  return request.get({ url: `/stock/stock_analysis/result/${result}` })
}

export const getValidAnalysesApi = (isValid: number = 1): Promise<IResponse> => {
  return request.get({ url: `/stock/stock_analysis/valid/${isValid}` })
}

export const verifyAnalysisApi = (
  id: number,
  data: { verification_result: string }
): Promise<IResponse> => {
  return request.put({ url: `/stock/stock_analysis/${id}/verify`, data })
}

export const updateAnalysisSendStatusApi = (id: number, isSend: number): Promise<IResponse> => {
  return request.put({ url: `/stock/stock_analysis/${id}/send`, data: isSend })
}
