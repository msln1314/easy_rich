from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Date, Index, UniqueConstraint
from db.db_base import BaseModel


class PortfolioPosition(BaseModel):
    __tablename__ = "portfolio_position"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "stock_code", name="uk_portfolio_stock"),
        Index("idx_position_portfolio", "portfolio_id"),
        Index("idx_position_stock", "stock_code"),
        {"comment": "持仓表"},
    )

    portfolio_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="组合ID")
    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="股票名称"
    )

    shares: Mapped[int] = mapped_column(Integer, nullable=False, comment="持仓股数")
    available_shares: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="可用股数"
    )
    cost_price: Mapped[float] = mapped_column(Float, nullable=False, comment="成本价")
    current_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="现价"
    )
    market_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="市值"
    )

    profit: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="盈亏金额"
    )
    profit_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="盈亏比例"
    )
    position_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="仓位占比(%)"
    )
    target_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="目标仓位占比(%)"
    )

    dividend_received: Mapped[float] = mapped_column(
        Float, default=0, comment="已收分红"
    )
    first_buy_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="首次买入日期"
    )
    last_trade_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="最近交易日期"
    )
