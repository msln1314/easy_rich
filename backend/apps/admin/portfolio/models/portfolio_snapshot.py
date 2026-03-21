from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Text, Date, Index, UniqueConstraint
from db.db_base import BaseModel


class PortfolioSnapshot(BaseModel):
    __tablename__ = "portfolio_snapshot"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "snapshot_date", name="uk_portfolio_date"),
        Index("idx_snapshot_portfolio", "portfolio_id"),
        Index("idx_snapshot_date", "snapshot_date"),
        {"comment": "组合快照表"},
    )

    portfolio_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="组合ID")
    snapshot_date: Mapped[date] = mapped_column(
        Date, nullable=False, comment="快照日期"
    )

    total_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="组合总市值"
    )
    total_cost: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="组合总成本"
    )
    profit_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="收益率"
    )

    sector_allocation: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="行业分布JSON"
    )
    top_holdings: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="前十大持仓JSON"
    )

    volatility: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="波动率"
    )
    beta: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Beta值")
