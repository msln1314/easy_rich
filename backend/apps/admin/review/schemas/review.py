from datetime import date
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class ReviewCreate(BaseModel):
    portfolio_id: Optional[int] = None
    review_type: str = Field(..., description="复盘类型")
    review_date: date = Field(..., description="复盘日期")
    market_summary: Optional[dict] = None
    market_analysis: Optional[str] = None
    position_summary: Optional[dict] = None
    position_analysis: Optional[str] = None
    trade_summary: Optional[dict] = None
    trade_analysis: Optional[str] = None
    strategy_summary: Optional[dict] = None
    strategy_analysis: Optional[str] = None
    profit_summary: Optional[dict] = None
    notes: Optional[str] = None
    next_plan: Optional[dict] = None
    ai_analysis: Optional[str] = None
    status: str = "draft"


class ReviewUpdate(BaseModel):
    market_summary: Optional[dict] = None
    market_analysis: Optional[str] = None
    position_summary: Optional[dict] = None
    position_analysis: Optional[str] = None
    trade_summary: Optional[dict] = None
    trade_analysis: Optional[str] = None
    strategy_summary: Optional[dict] = None
    strategy_analysis: Optional[str] = None
    profit_summary: Optional[dict] = None
    notes: Optional[str] = None
    next_plan: Optional[dict] = None
    ai_analysis: Optional[str] = None
    status: Optional[str] = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    portfolio_id: Optional[int] = None
    review_type: str
    review_date: date
    market_summary: Optional[Any] = None
    market_analysis: Optional[str] = None
    position_summary: Optional[Any] = None
    position_analysis: Optional[str] = None
    trade_summary: Optional[Any] = None
    trade_analysis: Optional[str] = None
    strategy_summary: Optional[Any] = None
    strategy_analysis: Optional[str] = None
    profit_summary: Optional[Any] = None
    notes: Optional[str] = None
    next_plan: Optional[Any] = None
    ai_analysis: Optional[str] = None
    status: str
    created_at: DatetimeStr
    updated_at: DatetimeStr


class ReviewListOut(BaseModel):
    total: int
    items: List[ReviewOut]
