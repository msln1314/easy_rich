# backend/qmt-service/app/models/quote_models.py
"""
行情数据模型
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class L2Quote(BaseModel):
    """L2十档行情"""
    stock_code: str
    stock_name: str = ""
    price: float  # 当前价
    open: float  # 开盘价
    high: float  # 最高价
    low: float  # 最低价
    pre_close: float  # 昨收
    volume: int  # 成交量
    amount: float  # 成交额

    # 五档买盘
    bid_price1: float = 0.0
    bid_volume1: int = 0
    bid_price2: float = 0.0
    bid_volume2: int = 0
    bid_price3: float = 0.0
    bid_volume3: int = 0
    bid_price4: float = 0.0
    bid_volume4: int = 0
    bid_price5: float = 0.0
    bid_volume5: int = 0

    # 五档卖盘
    ask_price1: float = 0.0
    ask_volume1: int = 0
    ask_price2: float = 0.0
    ask_volume2: int = 0
    ask_price3: float = 0.0
    ask_volume3: int = 0
    ask_price4: float = 0.0
    ask_volume4: int = 0
    ask_price5: float = 0.0
    ask_volume5: int = 0

    # L2扩展档位 (6-10档)
    bid_price6: float = 0.0
    bid_volume6: int = 0
    bid_price7: float = 0.0
    bid_volume7: int = 0
    bid_price8: float = 0.0
    bid_volume8: int = 0
    bid_price9: float = 0.0
    bid_volume9: int = 0
    bid_price10: float = 0.0
    bid_volume10: int = 0

    ask_price6: float = 0.0
    ask_volume6: int = 0
    ask_price7: float = 0.0
    ask_volume7: int = 0
    ask_price8: float = 0.0
    ask_volume8: int = 0
    ask_price9: float = 0.0
    ask_volume9: int = 0
    ask_price10: float = 0.0
    ask_volume10: int = 0

    updated_time: datetime


class L2QuoteListResponse(BaseModel):
    """L2行情列表响应"""
    quotes: List[L2Quote]
    count: int


class Tick(BaseModel):
    """逐笔成交"""
    tick_id: str
    stock_code: str
    price: float
    volume: int
    direction: str  # buy/sell/neutral
    trade_time: datetime
    order_type: str = "normal"  # normal/large/block 大单/特大单


class TickListResponse(BaseModel):
    """逐笔成交列表响应"""
    stock_code: str
    ticks: List[Tick]
    count: int


class MinuteBar(BaseModel):
    """分时数据"""
    stock_code: str
    time: datetime
    price: float
    volume: int
    amount: float
    avg_price: float
    open: float
    high: float
    low: float


class MinuteBarListResponse(BaseModel):
    """分时数据列表响应"""
    stock_code: str
    date: str
    bars: List[MinuteBar]
    count: int


class OrderBook(BaseModel):
    """订单簿深度"""
    stock_code: str
    price: float

    # 买盘深度
    bid_levels: List[dict]  # [{"price": 10.0, "volume": 1000}, ...]

    # 卖盘深度
    ask_levels: List[dict]

    updated_time: datetime


class DepthResponse(BaseModel):
    """深度数据响应"""
    stock_code: str
    depth: OrderBook


class QuoteStatus(BaseModel):
    """行情订阅状态"""
    subscribed: bool
    stock_codes: List[str]
    l2_enabled: bool
    message: str