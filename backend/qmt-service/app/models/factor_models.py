# backend/qmt-service/app/models/factor_models.py
"""
因子数据模型
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum


class FactorCategory(str, Enum):
    """因子分类"""
    TREND = "trend"           # 趋势因子
    MOMENTUM = "momentum"     # 动量因子
    VOLATILITY = "volatility" # 波动因子
    VOLUME = "volume"         # 成交量因子
    VALUE = "value"           # 价值因子
    GROWTH = "growth"         # 成长因子
    QUALITY = "quality"       # 质量因子
    SENTIMENT = "sentiment"   # 情绪因子
    CUSTOM = "custom"         # 自定义因子


class FactorDefinition(BaseModel):
    """因子定义"""
    factor_id: str
    factor_name: str
    category: FactorCategory
    description: str = ""
    formula: str = ""  # 因子公式/计算逻辑
    params: List[Dict[str, Any]] = []  # 参数列表
    unit: str = ""  # 单位
    data_source: str = ""  # 数据来源
    update_freq: str = "daily"  # 更新频率
    is_active: bool = True
    created_at: datetime = None
    updated_at: datetime = None


class FactorDefinitionListResponse(BaseModel):
    """因子定义列表响应"""
    factors: List[FactorDefinition]
    total: int


class FactorValue(BaseModel):
    """因子值"""
    factor_id: str
    stock_code: str
    stock_name: str = ""
    value: float
    date: str  # YYYYMMDD
    rank: Optional[int] = None  # 排名
    percentile: Optional[float] = None  # 百分位
    zscore: Optional[float] = None  # Z-Score


class FactorValueListResponse(BaseModel):
    """因子值列表响应"""
    factor_id: str
    date: str
    values: List[FactorValue]
    count: int


class StockFactorValues(BaseModel):
    """单只股票的多因子值"""
    stock_code: str
    stock_name: str = ""
    date: str
    factors: Dict[str, float]  # {factor_id: value}


class StockFactorValuesResponse(BaseModel):
    """单只股票因子值响应"""
    stock_code: str
    date: str
    factors: List[Dict[str, Any]]
    count: int


class FactorCorrelation(BaseModel):
    """因子相关性"""
    factor1: str
    factor2: str
    correlation: float
    period: str  # 计算周期


class FactorCorrelationResponse(BaseModel):
    """因子相关性响应"""
    factor_id: str
    correlations: List[FactorCorrelation]
    date: str


class FactorIC(BaseModel):
    """因子IC值"""
    factor_id: str
    date: str
    ic: float  # Information Coefficient
    ic_ir: float  # IC的IR
    rank_ic: float  # Rank IC


class FactorICListResponse(BaseModel):
    """因子IC列表响应"""
    factor_id: str
    values: List[FactorIC]
    count: int


class FactorReturn(BaseModel):
    """因子收益"""
    factor_id: str
    date: str
    period_return: float  # 周期收益
    cumulative_return: float  # 累计收益
    sharpe: float  # 夏普比率
    max_drawdown: float  # 最大回撤


class FactorReturnListResponse(BaseModel):
    """因子收益列表响应"""
    factor_id: str
    values: List[FactorReturn]
    count: int


class FactorScreenRequest(BaseModel):
    """因子筛选请求"""
    factors: List[Dict[str, Any]]  # [{"factor_id": "pe", "op": "lt", "value": 20}, ...]
    date: Optional[str] = None
    limit: int = 100


class FactorScreenResult(BaseModel):
    """因子筛选结果"""
    stock_code: str
    stock_name: str = ""
    date: str
    score: float  # 综合得分
    factor_values: Dict[str, float]


class FactorScreenResponse(BaseModel):
    """因子筛选响应"""
    date: str
    stocks: List[FactorScreenResult]
    count: int