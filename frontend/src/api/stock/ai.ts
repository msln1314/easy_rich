import request from '@/config/axios'

// ========== AI对话 ==========

/**
 * AI对话请求参数
 */
export interface ChatRequest {
  stock_code: string
  message: string
  conversation_id?: string
  model?: string
}

/**
 * AI对话响应
 */
export interface ChatResponse {
  conversation_id: string
  message: string
  created_at: string
  model?: string
  tokens_used?: number
}

/**
 * 发送AI对话消息
 */
export const aiChat = (data: ChatRequest): Promise<IResponse<ChatResponse>> => {
  return request.post({ url: '/ai/chat', data })
}

// ========== 多Agent分析 ==========

/**
 * 多Agent分析请求参数
 */
export interface AgentAnalyzeRequest {
  stock_code: string
  query?: string
  mode?: 'quick' | 'standard' | 'full' | 'specialist'
  agents?: string[]
}

/**
 * Agent观点
 */
export interface AgentOpinion {
  agent_name: string
  agent_type: string
  signal: string
  confidence: number
  reasoning: string
  key_points?: string[]
  key_levels?: Record<string, number>
}

/**
 * 综合研判结果
 */
export interface SynthesisResult {
  conclusion: string
  confidence: number
  target_price?: number
  stop_loss?: number
  risk_level: string
  operation_advice: string
  key_factors?: string[]
}

/**
 * 多Agent分析响应
 */
export interface AgentAnalyzeResponse {
  stock_code: string
  stock_name: string
  analysis_time: string
  signal: string
  confidence: number
  summary: string
  agent_opinions: AgentOpinion[]
  risks?: string[]
}

/**
 * 执行多Agent分析
 */
export const agentAnalyze = (
  data: AgentAnalyzeRequest
): Promise<IResponse<AgentAnalyzeResponse>> => {
  return request.post({ url: '/ai/agents/analyze', data })
}

// ========== 研报生成 ==========

/**
 * 研报生成请求参数
 */
export interface ReportGenerateRequest {
  stock_code: string
  report_type?: 'comprehensive' | 'technical' | 'fundamental'
  include_sections?: string[]
}

/**
 * 研报响应
 */
export interface ReportResponse {
  report_id: string
  stock_code: string
  stock_name?: string
  title: string
  content: string
  created_at: string
  report_type: string
}

/**
 * 生成研报
 */
export const generateReport = (data: ReportGenerateRequest): Promise<IResponse<ReportResponse>> => {
  return request.post({ url: '/ai/report/generate', data })
}

/**
 * 获取研报详情
 */
export const getReport = (reportId: string): Promise<IResponse<ReportResponse>> => {
  return request.get({ url: `/ai/report/${reportId}` })
}

/**
 * 导出研报
 */
export const exportReport = (reportId: string, format: string = 'pdf'): Promise<IResponse> => {
  return request.get({ url: `/ai/report/${reportId}/export`, params: { format } })
}

// ========== 市场洞察 ==========

/**
 * 市场概览响应
 */
export interface MarketOverviewResponse {
  date: string
  market_sentiment: string
  index_summary: Record<string, any>
  hot_sectors: Record<string, any>[]
  cold_sectors: Record<string, any>[]
  key_events?: string[]
  interpretation: string
}

/**
 * 获取市场概览
 */
export const getMarketOverview = (): Promise<IResponse<MarketOverviewResponse>> => {
  return request.get({ url: '/ai/market/overview' })
}

/**
 * 获取板块轮动数据
 */
export const getSectorRotation = (): Promise<IResponse> => {
  return request.get({ url: '/ai/market/sectors' })
}

/**
 * 获取资金流向
 */
export const getCapitalFlow = (): Promise<IResponse> => {
  return request.get({ url: '/ai/market/capital-flow' })
}

/**
 * 市场解读请求参数
 */
export interface MarketInterpretRequest {
  focus_sectors?: string[]
  include_individual_stocks?: boolean
}

/**
 * AI市场解读
 */
export const interpretMarket = (data: MarketInterpretRequest): Promise<IResponse> => {
  return request.post({ url: '/ai/market/interpret', data })
}

// ========== 盘后复盘 ==========

/**
 * 每日复盘响应
 */
export interface DailyReviewResponse {
  date: string
  market_summary: string
  portfolio_review?: Record<string, any>[]
  watchlist_review?: Record<string, any>[]
  opportunities: string[]
  risks: string[]
  suggestions?: string
}

/**
 * 获取每日复盘
 */
export const getDailyReview = (params: {
  date?: string
}): Promise<IResponse<DailyReviewResponse>> => {
  return request.get({ url: '/ai/review/daily', params })
}

/**
 * 获取交易总结
 */
export const getTradingSummary = (params: { date?: string }): Promise<IResponse> => {
  return request.get({ url: '/ai/review/trading-summary', params })
}

/**
 * 机会挖掘请求参数
 */
export interface OpportunityDiscoveryRequest {
  focus_sectors?: string[]
  risk_preference?: 'conservative' | 'moderate' | 'aggressive'
}

/**
 * 挖掘潜在机会
 */
export const discoverOpportunities = (data: OpportunityDiscoveryRequest): Promise<IResponse> => {
  return request.post({ url: '/ai/review/opportunities', data })
}

/**
 * 获取风险预警
 */
export const getRiskWarnings = (): Promise<IResponse> => {
  return request.get({ url: '/ai/review/risk-warnings' })
}

// ========== 定时任务 ==========

/**
 * 创建定时任务请求参数
 */
export interface ScheduleCreateRequest {
  task_type: 'daily_review' | 'market_interpret' | 'custom'
  cron_expression: string
  enabled?: boolean
  params?: Record<string, any>
}

/**
 * 定时任务
 */
export interface Schedule {
  id: string
  task_type: string
  cron_expression: string
  enabled: boolean
  params?: Record<string, any>
  created_at: string
  updated_at: string
}

/**
 * 创建定时任务
 */
export const createSchedule = (data: ScheduleCreateRequest): Promise<IResponse<Schedule>> => {
  return request.post({ url: '/ai/schedule/create', data })
}

/**
 * 获取定时任务列表
 */
export const getScheduleList = (): Promise<IResponse<Schedule[]>> => {
  return request.get({ url: '/ai/schedule/list' })
}

/**
 * 删除定时任务
 */
export const deleteSchedule = (scheduleId: string): Promise<IResponse> => {
  return request.delete({ url: `/ai/schedule/${scheduleId}` })
}

/**
 * 更新定时任务状态
 */
export const toggleSchedule = (scheduleId: string, enabled: boolean): Promise<IResponse> => {
  return request.put({ url: `/ai/schedule/${scheduleId}`, data: { enabled } })
}
