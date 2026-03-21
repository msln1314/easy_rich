from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class RuleCreate(BaseModel):
    rule_type: str = Field(..., description="规则类型: trap/baseline")
    category: Optional[str] = None
    name: str = Field(..., description="规则名称")
    description: Optional[str] = None
    severity: Optional[str] = None
    check_timing: Optional[List[str]] = None
    check_condition: Optional[dict] = None
    is_active: int = 1


class RuleUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    check_timing: Optional[List[str]] = None
    check_condition: Optional[dict] = None
    is_active: Optional[int] = None


class RuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    rule_type: str
    category: Optional[str] = None
    name: str
    description: Optional[str] = None
    severity: Optional[str] = None
    check_timing: Optional[list] = None
    check_condition: Optional[dict] = None
    is_active: int
    created_at: DatetimeStr
    updated_at: DatetimeStr


class ViolationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    rule_id: int
    violation_time: datetime
    violation_context: Optional[dict] = None
    related_stock_code: Optional[str] = None
    related_trade_id: Optional[int] = None
    user_note: Optional[str] = None
    created_at: DatetimeStr
