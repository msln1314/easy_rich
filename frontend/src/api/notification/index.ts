import request from '@/config/axios'

const API_PREFIX = '/notification'

// ==================== 通知渠道 API ====================

export interface ChannelForm {
  channel_type: string
  channel_name: string
  channel_config: Record<string, any>
}

export interface ChannelItem {
  id: number
  user_id: number
  channel_type: string
  channel_name: string
  channel_config: Record<string, any>
  is_enabled: boolean
  verified: boolean
  verified_at: string | null
  created_at: string
  updated_at: string
}

export function getChannelList(channelType?: string) {
  return request.get({ url: `${API_PREFIX}/channels`, params: { channel_type: channelType } })
}

export function createChannel(data: ChannelForm) {
  return request.post({ url: `${API_PREFIX}/channels`, data })
}

export function updateChannel(id: number, data: Partial<ChannelForm> & { is_enabled?: boolean }) {
  return request.put({ url: `${API_PREFIX}/channels/${id}`, data })
}

export function deleteChannel(id: number) {
  return request.delete({ url: `${API_PREFIX}/channels/${id}` })
}

export function sendVerifyCode(channelId: number) {
  return request.post({ url: `${API_PREFIX}/channels/${channelId}/send-code` })
}

export function verifyChannel(channelId: number, code: string) {
  return request.post({ url: `${API_PREFIX}/channels/${channelId}/verify`, data: { code } })
}

export function testChannel(channelId: number, title?: string, content?: string) {
  return request.post({
    url: `${API_PREFIX}/channels/${channelId}/test`,
    data: { title, content }
  })
}

// ==================== 系统通知 API ====================

export interface SystemNotification {
  id: number
  user_id: number
  title: string
  content: string
  notification_type: string
  is_read: boolean
  read_at: string | null
  link: string | null
  extra_data: Record<string, any> | null
  created_at: string
}

export interface NotificationListResponse {
  total: number
  items: SystemNotification[]
  unread_count: number
}

export function getNotificationList(params?: { is_read?: boolean; page?: number; page_size?: number }) {
  return request.get({ url: `${API_PREFIX}/list`, params })
}

export function getUnreadCount() {
  return request.get({ url: `${API_PREFIX}/unread-count` })
}

export function markAsRead(notificationId: number) {
  return request.put({ url: `${API_PREFIX}/${notificationId}/read` })
}

export function markAllAsRead() {
  return request.put({ url: `${API_PREFIX}/read-all` })
}

// ==================== 通知规则 API ====================

export interface NotificationRuleForm {
  rule_name: string
  rule_type: 'holiday' | 'earnings' | 'dividend' | 'unlock' | 'custom'
  event_type_filter?: string
  stock_codes?: string[]
  condition_config: Record<string, any>
  action_config: Record<string, any>
  priority?: number
  valid_from?: string
  valid_to?: string
}

export interface NotificationRuleItem {
  id: number
  user_id: number
  rule_name: string
  rule_type: string
  event_type_filter: string | null
  stock_codes: string[] | null
  condition_config: Record<string, any>
  action_config: Record<string, any>
  priority: number
  is_enabled: boolean
  valid_from: string | null
  valid_to: string | null
  last_triggered_at: string | null
  created_at: string
  updated_at: string
}

export interface RuleListResponse {
  total: number
  items: NotificationRuleItem[]
}

export function getNotificationRules(ruleType?: string) {
  return request.get({ url: `${API_PREFIX}/rules`, params: { rule_type: ruleType } })
}

export function createNotificationRule(data: NotificationRuleForm) {
  return request.post({ url: `${API_PREFIX}/rules`, data })
}

export function updateNotificationRule(id: number, data: Partial<NotificationRuleForm> & { is_enabled?: boolean }) {
  return request.put({ url: `${API_PREFIX}/rules/${id}`, data })
}

export function deleteNotificationRule(id: number) {
  return request.delete({ url: `${API_PREFIX}/rules/${id}` })
}

export function checkRules(targetDate?: string) {
  return request.post({ url: `${API_PREFIX}/rules/check`, data: { target_date: targetDate } })
}

// ==================== 规则类型说明 ====================

export const RULE_TYPE_OPTIONS = [
  { label: '节假日提醒', value: 'holiday', description: '节假日前N天提醒空仓' },
  { label: '财报发布提醒', value: 'earnings', description: '财报发布前N天提醒' },
  { label: '分红除权提醒', value: 'dividend', description: '分红除权日前N天提醒' },
  { label: '解禁日提醒', value: 'unlock', description: '股票解禁前N天提醒' },
  { label: '自定义规则', value: 'custom', description: '自定义事件类型和条件' }
]

export const CHANNEL_TYPE_OPTIONS = [
  { label: '邮件', value: 'email', icon: 'Message' },
  { label: '微信推送', value: 'wechat', icon: 'ChatDotRound' },
  { label: '系统通知', value: 'system', icon: 'Bell' }
]