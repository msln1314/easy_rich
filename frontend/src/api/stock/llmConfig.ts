import request from '@/config/axios'

// ========== 类型定义 ==========

export type ModelProvider =
  | 'openai'
  | 'deepseek'
  | 'aliyun'
  | 'zhipu'
  | 'baidu'
  | 'tencent'
  | 'custom'

export interface ProviderInfo {
  value: string
  label: string
  default_api_base: string
  models: string[]
}

export interface LLMModelConfig {
  id: number
  name: string
  provider: ModelProvider
  model_name: string
  api_base: string
  max_tokens: number
  temperature: number
  timeout: number
  is_default: boolean
  is_enabled: boolean
  description?: string
  created_at?: string
  updated_at?: string
  api_key_masked: string
}

export interface LLMModelConfigCreate {
  name: string
  provider: ModelProvider
  model_name: string
  api_key: string
  api_base: string
  max_tokens?: number
  temperature?: number
  timeout?: number
  is_default?: boolean
  is_enabled?: boolean
  description?: string
}

export interface LLMModelConfigUpdate {
  name?: string
  provider?: ModelProvider
  model_name?: string
  api_key?: string
  api_base?: string
  max_tokens?: number
  temperature?: number
  timeout?: number
  is_default?: boolean
  is_enabled?: boolean
  description?: string
}

// ========== API 函数 ==========

/**
 * 获取支持的模型提供商列表
 */
export const getProviders = (): Promise<IResponse<ProviderInfo[]>> => {
  return request.get({ url: '/llm-config/providers' })
}

/**
 * 获取所有模型配置列表
 */
export const getLLMConfigList = (): Promise<IResponse<LLMModelConfig[]>> => {
  return request.get({ url: '/llm-config/list' })
}

/**
 * 获取单个模型配置
 */
export const getLLMConfig = (id: number): Promise<IResponse<LLMModelConfig>> => {
  return request.get({ url: `/llm-config/${id}` })
}

/**
 * 创建模型配置
 */
export const createLLMConfig = (data: LLMModelConfigCreate): Promise<IResponse<LLMModelConfig>> => {
  return request.post({ url: '/llm-config/create', data })
}

/**
 * 更新模型配置
 */
export const updateLLMConfig = (id: number, data: LLMModelConfigUpdate): Promise<IResponse<LLMModelConfig>> => {
  return request.put({ url: `/llm-config/${id}`, data })
}

/**
 * 删除模型配置
 */
export const deleteLLMConfig = (id: number): Promise<IResponse> => {
  return request.delete({ url: `/llm-config/${id}` })
}

/**
 * 设置默认模型
 */
export const setDefaultLLMConfig = (id: number): Promise<IResponse> => {
  return request.post({ url: `/llm-config/${id}/set-default` })
}

/**
 * 启用/禁用模型配置
 */
export const toggleLLMConfig = (id: number): Promise<IResponse<{ is_enabled: boolean }>> => {
  return request.post({ url: `/llm-config/${id}/toggle` })
}

/**
 * 测试模型配置
 */
export const testLLMConfig = (id: number): Promise<IResponse<{ success: boolean; message: string }>> => {
  return request.post({ url: `/llm-config/${id}/test` })
}