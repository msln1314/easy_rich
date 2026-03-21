export type EventType = 
  | 'earnings_report'
  | 'earnings_forecast'
  | 'dividend'
  | 'unlock'
  | 'shareholders_mtg'
  | 'ipo_listing'
  | 'rating_change'
  | 'block_trade'
  | 'repurchase'
  | 'major_news'

export type AISentiment = 1 | 2 | 3

export interface CalendarEvent {
  id: number
  stock_code: string
  stock_name: string | null
  event_type: EventType
  event_date: string
  event_time: string | null
  title: string
  content: string | null
  impact_data: Record<string, any> | null
  ai_impact_score: number | null
  ai_sentiment: AISentiment | null
  ai_analysis: string | null
  ai_suggestion: string | null
  is_in_watchlist: number
  data_source: string
  source_url: string | null
  created_at: string
  updated_at: string
}

export interface EventReminder {
  id: number
  user_id: number
  stock_code: string
  event_id: number
  remind_days: number
  remind_time: string
  remind_type: 'system' | 'email'
  is_active: number
  last_remind_at: string | null
  created_at: string
}

export const EVENT_TYPE_MAP: Record<EventType, { label: string; color: string }> = {
  earnings_report: { label: '财报发布', color: '#409EFF' },
  earnings_forecast: { label: '业绩预告', color: '#67C23A' },
  dividend: { label: '分红除权', color: '#E6A23C' },
  unlock: { label: '解禁日', color: '#F56C6C' },
  shareholders_mtg: { label: '股东大会', color: '#909399' },
  ipo_listing: { label: '新股上市', color: '#409EFF' },
  rating_change: { label: '评级变动', color: '#E6A23C' },
  block_trade: { label: '大宗交易', color: '#909399' },
  repurchase: { label: '股票回购', color: '#67C23A' },
  major_news: { label: '重要公告', color: '#F56C6C' }
}

export const AI_SENTIMENT_MAP: Record<AISentiment, { label: string; color: string; icon: string }> = {
  1: { label: '利好', color: '#67C23A', icon: '↑' },
  2: { label: '中性', color: '#909399', icon: '→' },
  3: { label: '利空', color: '#F56C6C', icon: '↓' }
}