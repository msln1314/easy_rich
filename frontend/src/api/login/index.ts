import request from '@/config/axios'
import type { UserLoginType } from './types'

export const loginApi = (data: UserLoginType): Promise<IResponse> => {
  return request.post({ url: '/auth/login', data })
}

export const sendCodeApi = (data: { username: string }): Promise<IResponse> => {
  return request.post({ url: '/auth/send/code', data })
}

export const registerApi = (data: {
  username: string
  code: string
  password: string
}): Promise<IResponse> => {
  return request.post({ url: '/auth/register', data })
}

export const postSMSCodeApi = (params: any): Promise<IResponse> => {
  return request.post({ url: '/system/sms/send', params })
}
