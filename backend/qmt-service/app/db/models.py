# backend/qmt-service/app/db/models.py
"""
数据库模型定义
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, JSON
from sqlalchemy import Enum as SQLEnum
import enum

from app.db.database import Base


class FactorCategory(str, enum.Enum):
    """因子分类"""
    TREND = "trend"
    MOMENTUM = "momentum"
    VOLATILITY = "volatility"
    VOLUME = "volume"
    VALUE = "value"
    GROWTH = "growth"
    QUALITY = "quality"
    SENTIMENT = "sentiment"
    CUSTOM = "custom"


class FactorDefinition(Base):
    """因子定义表"""
    __tablename__ = "factor_definition"

    id = Column(Integer, primary_key=True, autoincrement=True)
    factor_id = Column(String(50), unique=True, nullable=False, comment="因子ID")
    factor_name = Column(String(100), nullable=False, comment="因子名称")
    category = Column(SQLEnum(FactorCategory), default=FactorCategory.CUSTOM, comment="因子分类")
    description = Column(Text, nullable=True, comment="因子描述")
    formula = Column(String(500), nullable=True, comment="计算公式")
    params = Column(JSON, nullable=True, comment="参数配置")
    unit = Column(String(20), nullable=True, comment="单位")
    data_source = Column(String(50), nullable=True, comment="数据来源")
    update_freq = Column(String(20), default="daily", comment="更新频率")
    is_active = Column(Boolean, default=True, comment="是否启用")
    is_builtin = Column(Boolean, default=False, comment="是否内置因子")
    sort_order = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"<FactorDefinition {self.factor_id}: {self.factor_name}>"


class FactorValue(Base):
    """因子值表"""
    __tablename__ = "factor_value"

    id = Column(Integer, primary_key=True, autoincrement=True)
    factor_id = Column(String(50), nullable=False, index=True, comment="因子ID")
    stock_code = Column(String(20), nullable=False, index=True, comment="股票代码")
    trade_date = Column(String(8), nullable=False, index=True, comment="交易日期 YYYYMMDD")
    value = Column(Float, nullable=True, comment="因子值")
    rank = Column(Integer, nullable=True, comment="排名")
    percentile = Column(Float, nullable=True, comment="百分位")
    zscore = Column(Float, nullable=True, comment="Z-Score")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    __table_args__ = (
        # 联合唯一索引
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    def __repr__(self):
        return f"<FactorValue {self.factor_id} {self.stock_code} {self.trade_date}>"


class FactorIC(Base):
    """因子IC表"""
    __tablename__ = "factor_ic"

    id = Column(Integer, primary_key=True, autoincrement=True)
    factor_id = Column(String(50), nullable=False, index=True, comment="因子ID")
    trade_date = Column(String(8), nullable=False, index=True, comment="交易日期")
    ic = Column(Float, nullable=True, comment="Information Coefficient")
    ic_ir = Column(Float, nullable=True, comment="IC IR")
    rank_ic = Column(Float, nullable=True, comment="Rank IC")
    sample_count = Column(Integer, nullable=True, comment="样本数量")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    def __repr__(self):
        return f"<FactorIC {self.factor_id} {self.trade_date}>"


class FactorReturn(Base):
    """因子收益表"""
    __tablename__ = "factor_return"

    id = Column(Integer, primary_key=True, autoincrement=True)
    factor_id = Column(String(50), nullable=False, index=True, comment="因子ID")
    trade_date = Column(String(8), nullable=False, index=True, comment="交易日期")
    period_return = Column(Float, nullable=True, comment="周期收益")
    cumulative_return = Column(Float, nullable=True, comment="累计收益")
    sharpe = Column(Float, nullable=True, comment="夏普比率")
    max_drawdown = Column(Float, nullable=True, comment="最大回撤")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    def __repr__(self):
        return f"<FactorReturn {self.factor_id} {self.trade_date}>"