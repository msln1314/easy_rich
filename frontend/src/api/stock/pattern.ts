import { defHttp } from '/@/utils/http/axios'

enum Api {
  DETECT_ALL = '/pattern/detect',
  SCAN = '/pattern/scan'
}

// 形态结果
export interface PatternResult {
  stock_code: string
  stock_name: string
  pattern_type: string
  pattern_name: string
  confidence: number
  signal: 'buy' | 'sell' | 'hold'
  price: number | null
  target_price: number | null
  stop_loss: number | null
  description: string
  detected_time: string
}

// 检测所有形态
export function detectAllPatterns(stockCode: string) {
  return defHttp.get({
    url: `${Api.DETECT_ALL}/${stockCode}`
  })
}

// 检测W底
export function detectWBottom(stockCode: string) {
  return defHttp.get({
    url: `${Api.DETECT_ALL}/${stockCode}/w-bottom`
  })
}

// 检测M头
export function detectMTop(stockCode: string) {
  return defHttp.get({
    url: `${Api.DETECT_ALL}/${stockCode}/m-top`
  })
}

// 检测头肩形态
export function detectHeadShoulders(stockCode: string) {
  return defHttp.get({
    url: `${Api.DETECT_ALL}/${stockCode}/head-shoulders`
  })
}

// 检测突破
export function detectBreakout(stockCode: string) {
  return defHttp.get({
    url: `${Api.DETECT_ALL}/${stockCode}/breakout`
  })
}

// 批量扫描形态
export function scanPatterns(stockCodes: string[], patternType?: string) {
  return defHttp.post({
    url: Api.SCAN,
    data: {
      stock_codes: stockCodes,
      pattern_type: patternType
    }
  })
}

// 形态类型映射
export const patternTypeMap: Record<string, { name: string; signal: string; color: string; description: string }> = {
  W_BOTTOM: {
    name: 'W底（双底）',
    signal: 'buy',
    color: '#67C23A',
    description: 'W底是典型的底部反转形态，由两个相近的低点构成，预示行情可能由跌转涨。建议在突破颈线位后买入。'
  },
  M_TOP: {
    name: 'M头（双顶）',
    signal: 'sell',
    color: '#F56C6C',
    description: 'M头是典型的顶部反转形态，由两个相近的高点构成，预示行情可能由涨转跌。建议在跌破颈线位后卖出。'
  },
  HEAD_SHOULDERS_TOP: {
    name: '头肩顶',
    signal: 'sell',
    color: '#F56C6C',
    description: '头肩顶由左肩、头部、右肩三个高点构成，是重要的顶部反转信号。建议跌破颈线后减仓或清仓。'
  },
  HEAD_SHOULDERS_BOTTOM: {
    name: '头肩底',
    signal: 'buy',
    color: '#67C23A',
    description: '头肩底由左肩、头部、右肩三个低点构成，是重要的底部反转信号。建议突破颈线后买入。'
  },
  BREAKOUT_UP: {
    name: '向上突破',
    signal: 'buy',
    color: '#67C23A',
    description: '股价突破近期高点，表明上涨动能增强，可能开启新一轮上涨行情。'
  },
  BREAKOUT_DOWN: {
    name: '向下突破',
    signal: 'sell',
    color: '#F56C6C',
    description: '股价跌破近期低点，表明下跌动能增强，可能开启新一轮下跌行情。'
  }
}

// 形态类型选项
export const patternTypeOptions = [
  { label: '全部形态', value: '' },
  { label: 'W底', value: 'W_BOTTOM' },
  { label: 'M头', value: 'M_TOP' },
  { label: '头肩形态', value: 'HEAD_SHOULDERS' },
  { label: '突破形态', value: 'BREAKOUT' }
]