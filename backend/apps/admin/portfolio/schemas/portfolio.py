from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class PortfolioCreate(BaseModel):
    name: str = Field(..., description="组合名称")
    description: Optional[str] = Field(None, description="组合描述")
    target_allocation: Optional[List[dict]] = Field(None, description="目标资产配置")
    max_single_position: float = Field(default=20.0, description="单只股票最大仓位")
    max_sector_position: float = Field(default=40.0, description="单个行业最大仓位")
    max_drawdown: float = Field(default=15.0, description="最大回撤预警线")
    rebalance_threshold: float = Field(default=5.0, description="再平衡触发阈值")
    rebalance_period: str = Field(default="monthly", description="再平衡周期")
    benchmark_index: str = Field(default="000300", description="基准指数代码")


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    target_allocation: Optional[List[dict]] = None
    max_single_position: Optional[float] = None
    max_sector_position: Optional[float] = None
    max_drawdown: Optional[float] = None
    rebalance_threshold: Optional[float] = None
    rebalance_period: Optional[str] = None
    benchmark_index: Optional[str] = None
    is_active: Optional[int] = None


class PortfolioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    target_allocation: Optional[Any] = None
    max_single_position: float
    max_sector_position: float
    max_drawdown: float
    rebalance_threshold: float
    rebalance_period: str
    benchmark_index: str
    total_value: Optional[float] = None
    total_cost: Optional[float] = None
    total_profit: Optional[float] = None
    profit_rate: Optional[float] = None
    annual_return: Optional[float] = None
    is_default: int
    is_active: int
    created_at: DatetimeStr
    updated_at: DatetimeStr


class PortfolioListOut(BaseModel):
    total: int
    items: List[PortfolioOut]
