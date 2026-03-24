import request from '@/config/axios'

// ==================== 复盘记录 API ====================

export const getReviewListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/review/reviews', params })
}

export const getReviewDetailApi = (id: number): Promise<IResponse> => {
  return request.get({ url: `/stock/review/reviews/${id}` })
}

export const createReviewApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/review/reviews', data })
}

export const updateReviewApi = (id: number, data: any): Promise<IResponse> => {
  return request.put({ url: `/stock/review/reviews/${id}`, data })
}

export const deleteReviewApi = (ids: number[]): Promise<IResponse> => {
  return request.delete({ url: '/stock/review/reviews', data: { ids } })
}

// ==================== 心得经验 API ====================

export const getExperienceListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/review/experiences', params })
}

export const getExperienceDetailApi = (id: number): Promise<IResponse> => {
  return request.get({ url: `/stock/review/experiences/${id}` })
}

export const createExperienceApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/review/experiences', data })
}

export const updateExperienceApi = (id: number, data: any): Promise<IResponse> => {
  return request.put({ url: `/stock/review/experiences/${id}`, data })
}

export const deleteExperienceApi = (ids: number[]): Promise<IResponse> => {
  return request.delete({ url: '/stock/review/experiences', data: { ids } })
}

// ==================== 雷区基线规则 API ====================

export const getRuleListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/review/rules', params })
}

export const getRuleDetailApi = (id: number): Promise<IResponse> => {
  return request.get({ url: `/stock/review/rules/${id}` })
}

export const createRuleApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/review/rules', data })
}

export const updateRuleApi = (id: number, data: any): Promise<IResponse> => {
  return request.put({ url: `/stock/review/rules/${id}`, data })
}

export const updateRuleActiveApi = (id: number, isActive: number): Promise<IResponse> => {
  return request.put({ url: `/stock/review/rules/${id}/active`, data: { is_active: isActive } })
}

export const deleteRuleApi = (ids: number[]): Promise<IResponse> => {
  return request.delete({ url: '/stock/review/rules', data: { ids } })
}

// ==================== 违规记录 API ====================

export const getViolationListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/stock/review/violations', params })
}

export const createViolationApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/stock/review/violations', data })
}
