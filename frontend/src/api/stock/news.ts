import request from '@/config/axios'

export const getNewsListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/news', params })
}

export const delNewsListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/stock/news', data })
}

export const addNewsListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/news', data })
}

export const putNewsListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/stock/news/${data.id}`, data })
}

export const getNewsApi = (id: number): Promise<IResponse> => {
  return request.get({ url: `/stock/news/${id}` })
}

export const postExportNewsListApi = (params: any, data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/news/export/excel', params, data })
}

export const updateNewsSendStatusApi = (newsId: number, isSend: number): Promise<IResponse> => {
  return request.put({ url: `/stock/news/${newsId}/send`, data: { is_send: isSend } })
}

export const updateNewsAnalyzeStatusApi = (
  newsId: number,
  analyzeData: any
): Promise<IResponse> => {
  return request.put({ url: `/stock/news/${newsId}/analyze`, data: analyzeData })
}
