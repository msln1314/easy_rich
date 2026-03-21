from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Text, Date, Index
from db.db_base import BaseModel


class PortfolioTrade(BaseModel):
    __tablename__ = "portfolio_trade"
    __table_args__ = (
        Index("idx_trade_portfolio", "portfolio_id"),
        Index("idx_trade_stock", "stock_code"),
        Index("idx_trade_date", "trade_date"),
        {"comment": "交易记录表"},
    )

    portfolio_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="组合ID")
    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="股票名称"
    )

    trade_type: Mapped[str] = mapped_column(
        String(10), nullable=False, comment="交易类型: buy/sell/dividend"
    )
    trade_date: Mapped[date] = mapped_column(Date, nullable=False, comment="交易日期")
    shares: Mapped[int] = mapped_column(Integer, nullable=False, comment="交易股数")
    price: Mapped[float] = mapped_column(Float, nullable=False, comment="交易价格")
    amount: Mapped[float] = mapped_column(Float, nullable=False, comment="交易金额")
    commission: Mapped[float] = mapped_column(Float, default=0, comment="手续费")
    stamp_duty: Mapped[float] = mapped_column(Float, default=0, comment="印花税")

    position_before: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="交易前持仓"
    )
    position_after: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="交易后持仓"
    )
    cost_price_before: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="交易前成本"
    )
    cost_price_after: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="交易后成本"
    )

    source: Mapped[str] = mapped_column(String(20), default="manual", comment="来源")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
