from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class PositionCreate(BaseModel):
    stock_code: str = Field(..., description="股票代码")
    stock_name: Optional[str] = Field(None, description="股票名称")
    shares: int = Field(..., description="持仓股数")
    cost_price: float = Field(..., description="成本价")
    target_ratio: Optional[float] = Field(None, description="目标仓位占比")


class PositionUpdate(BaseModel):
    shares: Optional[int] = None
    cost_price: Optional[float] = None
    target_ratio: Optional[float] = None


class PositionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    portfolio_id: int
    stock_code: str
    stock_name: Optional[str] = None
    shares: int
    available_shares: Optional[int] = None
    cost_price: float
    current_price: Optional[float] = None
    market_value: Optional[float] = None
    profit: Optional[float] = None
    profit_rate: Optional[float] = None
    position_ratio: Optional[float] = None
    target_ratio: Optional[float] = None
    dividend_received: float
    first_buy_date: Optional[date] = None
    last_trade_date: Optional[date] = None
    created_at: DatetimeStr
    updated_at: DatetimeStr


class PositionListOut(BaseModel):
    total: int
    items: List[PositionOut]
