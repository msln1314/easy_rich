# backend/qmt-service/app/models/position_models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Position(BaseModel):
    """持仓信息"""
    stock_code: str
    stock_name: str
    quantity: int              # 持仓数量
    available: int             # 可用数量
    cost_price: float          # 成本价
    current_price: float       # 当前价
    profit: float              # 盈亏金额
    profit_rate: float         # 盈亏比例(%)
    market_value: float        # 市值
    updated_time: datetime


class PositionListResponse(BaseModel):
    """持仓列表响应"""
    positions: list[Position]
    total_market_value: float  # 总市值
    total_profit: float        # 总盈亏
    count: int


class Balance(BaseModel):
    """资金余额"""
    total_asset: float         # 总资产
    available_cash: float      # 可用资金
    market_value: float        # 持仓市值
    frozen_cash: float         # 冻结资金
    profit_today: float        # 今日盈亏
    profit_total: float        # 总盈亏
    updated_time: datetime


class Trade(BaseModel):
    """成交记录"""
    trade_id: str
    order_id: str
    stock_code: str
    stock_name: str
    direction: str
    price: float
    quantity: int
    trade_time: datetime
    commission: float = 0.0


class TradeListResponse(BaseModel):
    """成交记录列表响应"""
    trades: list[Trade]
    total: int