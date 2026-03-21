from datetime import time
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class StockEventReminderCreate(BaseModel):
    user_id: int = Field(..., description="用户ID")
    stock_code: str = Field(..., description="股票代码")
    event_id: int = Field(..., description="事件ID")
    remind_days: int = Field(default=1, ge=1, le=7, description="提前几天提醒")
    remind_time: time = Field(default=time(9, 0), description="提醒时间")
    remind_type: str = Field(default="system", description="提醒方式")


class StockEventReminderUpdate(BaseModel):
    remind_days: Optional[int] = Field(None, ge=1, le=7)
    remind_time: Optional[time] = None
    remind_type: Optional[str] = None
    is_active: Optional[int] = None


class StockEventReminderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    stock_code: str
    event_id: int
    remind_days: int
    remind_time: time
    remind_type: str
    is_active: int
    last_remind_at: Optional[DatetimeStr] = None
    created_at: DatetimeStr


class StockEventReminderListOut(BaseModel):
    total: int
    items: List[StockEventReminderOut]
