# backend/qmt-service/app/models/trade_models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class OrderDirection(str, Enum):
    """订单方向"""
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    """订单类型"""
    LIMIT = "limit"      # 限价单
    MARKET = "market"    # 市价单


class OrderStatus(str, Enum):
    """订单状态"""
    PENDING = "pending"        # 待成交
    PARTIAL = "partial"        # 部分成交
    FILLED = "filled"          # 全部成交
    CANCELLED = "cancelled"    # 已撤单
    REJECTED = "rejected"      # 已拒绝


class OrderCreate(BaseModel):
    """创建订单请求"""
    stock_code: str
    direction: OrderDirection
    price: Optional[float] = None  # 市价单可为空
    quantity: int
    order_type: OrderType = OrderType.LIMIT


class OrderResponse(BaseModel):
    """订单响应"""
    order_id: str
    stock_code: str
    stock_name: str
    direction: OrderDirection
    price: float
    quantity: int
    order_type: OrderType
    status: OrderStatus
    filled_quantity: int = 0
    filled_price: float = 0.0
    created_time: datetime
    updated_time: datetime
    message: Optional[str] = None


class OrderListResponse(BaseModel):
    """订单列表响应"""
    orders: list[OrderResponse]
    total: int


class CancelOrderResponse(BaseModel):
    """撤单响应"""
    order_id: str
    success: bool
    message: str