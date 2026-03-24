from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator
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
    check_timing: Optional[Any] = None
    check_condition: Optional[Any] = None
    is_active: int
    created_at: DatetimeStr
    updated_at: DatetimeStr

    @field_validator("check_timing", "check_condition", mode="before")
    @classmethod
    def parse_json_field(cls, v):
        if isinstance(v, str):
            import json

            try:
                return json.loads(v)
            except:
                return v
        return v


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
