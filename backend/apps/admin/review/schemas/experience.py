from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class ExperienceCreate(BaseModel):
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    related_stocks: Optional[List[str]] = None
    related_trades: Optional[List[int]] = None
    related_review_id: Optional[int] = None
    mood: Optional[str] = None
    importance: str = "normal"


class ExperienceUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    related_stocks: Optional[List[str]] = None
    related_trades: Optional[List[int]] = None
    related_review_id: Optional[int] = None
    mood: Optional[str] = None
    importance: Optional[str] = None


class ExperienceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    content: str
    category: Optional[str] = None
    tags: Optional[list] = None
    related_stocks: Optional[list] = None
    related_trades: Optional[list] = None
    related_review_id: Optional[int] = None
    mood: Optional[str] = None
    importance: str
    view_count: int
    created_at: DatetimeStr
    updated_at: DatetimeStr


class ExperienceListOut(BaseModel):
    total: int
    items: List[ExperienceOut]
