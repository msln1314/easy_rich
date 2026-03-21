export interface Portfolio {
  id: number
  user_id: number
  name: string
  description: string | null
  target_allocation: any[] | null
  max_single_position: number
  max_sector_position: number
  max_drawdown: number
  rebalance_threshold: number
  rebalance_period: string
  benchmark_index: string
  total_value: number | null
  total_cost: number | null
  total_profit: number | null
  profit_rate: number | null
  annual_return: number | null
  is_default: number
  is_active: number
  created_at: string
  updated_at: string
}

export interface Position {
  id: number
  portfolio_id: number
  stock_code: string
  stock_name: string | null
  shares: number
  available_shares: number | null
  cost_price: number
  current_price: number | null
  market_value: number | null
  profit: number | null
  profit_rate: number | null
  position_ratio: number | null
  target_ratio: number | null
  dividend_received: number
  first_buy_date: string | null
  last_trade_date: string | null
  created_at: string
  updated_at: string
}

export interface Trade {
  id: number
  portfolio_id: number
  stock_code: string
  stock_name: string | null
  trade_type: 'buy' | 'sell' | 'dividend'
  trade_date: string
  shares: number
  price: number
  amount: number
  commission: number
  stamp_duty: number
  position_before: number | null
  position_after: number | null
  cost_price_before: number | null
  cost_price_after: number | null
  source: string
  remark: string | null
  created_at: string
}

export interface TradeBuy {
  stock_code: string
  stock_name?: string
  shares: number
  price: number
  trade_date: string
  commission?: number
  remark?: string
}

export interface TradeSell {
  stock_code: string
  shares: number
  price: number
  trade_date: string
  commission?: number
  stamp_duty?: number
  remark?: string
}

export interface PortfolioCreate {
  name: string
  description?: string
  target_allocation?: any[]
  max_single_position?: number
  max_sector_position?: number
  max_drawdown?: number
  rebalance_threshold?: number
  rebalance_period?: string
  benchmark_index?: string
}

export interface RiskAlert {
  id: number
  portfolio_id: number
  alert_type: string
  alert_level: string
  title: string
  content: string | null
  related_stock_code: string | null
  related_value: number | null
  threshold_value: number | null
  is_read: number
  is_handled: number
  handle_note: string | null
  handled_at: string | null
  created_at: string
}

export interface PositionAnalysis {
  positions: Position[]
  sector_allocation: Record<string, number>
  top_holdings: Position[]
}

export interface TradeStatistics {
  period_days: number
  total_trades: number
  buy_count: number
  sell_count: number
  buy_amount: number
  sell_amount: number
  total_commission: number
  total_stamp_duty: number
  total_cost: number
}

export interface RebalanceSuggestion {
  stock_code: string
  stock_name: string
  current_ratio: number
  target_ratio: number
  deviation: number
  suggested_action: 'buy' | 'sell'
}