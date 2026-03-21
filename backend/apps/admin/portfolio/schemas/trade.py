from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class TradeBuy(BaseModel):
    stock_code: str = Field(..., description="股票代码")
    stock_name: Optional[str] = Field(None, description="股票名称")
    shares: int = Field(..., ge=1, description="买入股数")
    price: float = Field(..., gt=0, description="买入价格")
    trade_date: date = Field(..., description="交易日期")
    commission: float = Field(default=0, description="手续费")
    remark: Optional[str] = Field(None, description="备注")


class TradeSell(BaseModel):
    stock_code: str = Field(..., description="股票代码")
    shares: int = Field(..., ge=1, description="卖出股数")
    price: float = Field(..., gt=0, description="卖出价格")
    trade_date: date = Field(..., description="交易日期")
    commission: float = Field(default=0, description="手续费")
    stamp_duty: float = Field(default=0, description="印花税")
    remark: Optional[str] = Field(None, description="备注")


class TradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    portfolio_id: int
    stock_code: str
    stock_name: Optional[str] = None
    trade_type: str
    trade_date: date
    shares: int
    price: float
    amount: float
    commission: float
    stamp_duty: float
    position_before: Optional[int] = None
    position_after: Optional[int] = None
    cost_price_before: Optional[float] = None
    cost_price_after: Optional[float] = None
    source: str
    remark: Optional[str] = None
    created_at: DatetimeStr


class TradeListOut(BaseModel):
    total: int
    items: List[TradeOut]
