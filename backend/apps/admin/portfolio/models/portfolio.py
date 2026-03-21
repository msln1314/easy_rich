from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, SmallInteger, Integer, Index
from db.db_base import BaseModel


class Portfolio(BaseModel):
    __tablename__ = "portfolio"
    __table_args__ = (
        Index("idx_portfolio_user", "user_id"),
        Index("idx_portfolio_active", "is_active"),
        {"comment": "投资组合表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="组合名称")
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="组合描述"
    )

    target_allocation: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="目标资产配置JSON"
    )

    max_single_position: Mapped[float] = mapped_column(
        Float, default=20.00, comment="单只股票最大仓位(%)"
    )
    max_sector_position: Mapped[float] = mapped_column(
        Float, default=40.00, comment="单个行业最大仓位(%)"
    )
    max_drawdown: Mapped[float] = mapped_column(
        Float, default=15.00, comment="最大回撤预警线(%)"
    )
    rebalance_threshold: Mapped[float] = mapped_column(
        Float, default=5.00, comment="再平衡触发阈值(%)"
    )
    rebalance_period: Mapped[str] = mapped_column(
        String(20), default="monthly", comment="再平衡周期"
    )

    total_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="组合总市值"
    )
    total_cost: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="组合总成本"
    )
    total_profit: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="总盈亏"
    )
    profit_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="收益率"
    )
    annual_return: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="年化收益率"
    )

    benchmark_index: Mapped[str] = mapped_column(
        String(20), default="000300", comment="基准指数代码"
    )
    is_default: Mapped[int] = mapped_column(
        SmallInteger, default=0, comment="是否默认组合"
    )
    is_active: Mapped[int] = mapped_column(SmallInteger, default=1, comment="是否启用")
