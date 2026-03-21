from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class StockCalendarEventParams(BaseModel):
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    stock_code: Optional[str] = Field(None, description="股票代码")
    event_type: Optional[str] = Field(None, description="事件类型")
    is_watchlist: Optional[int] = Field(None, description="是否仅自选股")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")


class InvestCalendarEventParams(BaseModel):
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    event_type: Optional[str] = Field(None, description="事件类型")
    importance: Optional[int] = Field(None, ge=1, le=3, description="重要程度")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
