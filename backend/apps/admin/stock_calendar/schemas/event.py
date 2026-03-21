from datetime import date, time
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class StockCalendarEventCreate(BaseModel):
    stock_code: str = Field(..., description="股票代码")
    stock_name: Optional[str] = Field(None, description="股票名称")
    event_type: str = Field(..., description="事件类型")
    event_date: date = Field(..., description="事件日期")
    event_time: Optional[time] = Field(None, description="事件时间")
    title: str = Field(..., description="事件标题")
    content: Optional[str] = Field(None, description="事件详情")
    impact_data: Optional[dict] = Field(None, description="事件影响数据")
    data_source: str = Field(default="manual", description="数据来源")


class StockCalendarEventUpdate(BaseModel):
    stock_name: Optional[str] = None
    event_time: Optional[time] = None
    title: Optional[str] = None
    content: Optional[str] = None
    impact_data: Optional[dict] = None
    ai_impact_score: Optional[float] = None
    ai_sentiment: Optional[int] = None
    ai_analysis: Optional[str] = None
    ai_suggestion: Optional[str] = None


class StockCalendarEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    stock_code: str
    stock_name: Optional[str] = None
    event_type: str
    event_date: date
    event_time: Optional[time] = None
    title: str
    content: Optional[str] = None
    impact_data: Optional[dict] = None
    ai_impact_score: Optional[float] = None
    ai_sentiment: Optional[int] = None
    ai_analysis: Optional[str] = None
    ai_suggestion: Optional[str] = None
    is_in_watchlist: int = 0
    data_source: str
    source_url: Optional[str] = None
    created_at: DatetimeStr
    updated_at: DatetimeStr


class StockCalendarEventListOut(BaseModel):
    total: int
    items: List[StockCalendarEventOut]
