from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

# ... 保留现有的模型 ...

class ChipDistribution(BaseModel):
    """筹码分布模型"""
    trade_date: str = Field(..., description="交易日期")
    stock_code: str = Field(..., description="股票代码")
    profit_ratio: float = Field(..., description="获利比例")
    avg_cost: float = Field(..., description="平均成本")
    cost_90_low: float = Field(..., description="90成本-低")
    cost_90_high: float = Field(..., description="90成本-高")
    concentration_90: float = Field(..., description="90集中度")
    cost_70_low: float = Field(..., description="70成本-低")
    cost_70_high: float = Field(..., description="70成本-高")
    concentration_70: float = Field(..., description="70集中度")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")