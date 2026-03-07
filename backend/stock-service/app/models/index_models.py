from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class IndexQuote(BaseModel):
    """指数实时行情模型"""
    code: str
    name: str
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌额")
    change_percent: float = Field(..., description="涨跌幅(%)")
    volume: Optional[float] = Field(None, description="成交量")
    amount: Optional[float] = Field(None, description="成交额")
    amplitude: Optional[float] = Field(None, description="振幅(%)")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    open: Optional[float] = Field(None, description="今开")
    pre_close: Optional[float] = Field(None, description="昨收")
    volume_ratio: Optional[float] = Field(None, description="量比")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")