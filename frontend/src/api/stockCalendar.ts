import request from '@/utils/request'

const API_PREFIX = '/stock_calendar'

export function getEventList(params: {
  start_date?: string
  end_date?: string
  stock_code?: string
  event_type?: string
  is_watchlist?: number
  page?: number
  page_size?: number
}) {
  return request.get(`${API_PREFIX}/events`, { params })
}

export function getEventDetail(eventId: number) {
  return request.get(`${API_PREFIX}/events/${eventId}`)
}

export function getEventsByStock(stockCode: string, days = 90) {
  return request.get(`${API_PREFIX}/events/by_stock/${stockCode}`, { params: { days } })
}

export function getEventsByDate(date: string) {
  return request.get(`${API_PREFIX}/events/by_date/${date}`)
}

export function createEvent(data: any) {
  return request.post(`${API_PREFIX}/events`, data)
}

export function getReminderList(userId: number, isActive?: number) {
  return request.get(`${API_PREFIX}/reminders`, { params: { user_id: userId, is_active: isActive } })
}

export function createReminder(data: {
  user_id: number
  stock_code: string
  event_id: number
  remind_days?: number
  remind_time?: string
  remind_type?: string
}) {
  return request.post(`${API_PREFIX}/reminders`, data)
}

export function updateReminder(reminderId: number, data: any) {
  return request.put(`${API_PREFIX}/reminders/${reminderId}`, data)
}

export function deleteReminder(reminderId: number) {
  return request.delete(`${API_PREFIX}/reminders/${reminderId}`)
}