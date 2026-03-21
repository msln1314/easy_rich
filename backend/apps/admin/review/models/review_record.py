from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, Date, Index
from db.db_base import BaseModel


class ReviewRecord(BaseModel):
    __tablename__ = "review_record"
    __table_args__ = (
        Index("idx_review_user_date", "user_id", "review_date"),
        Index("idx_review_type", "review_type"),
        {"comment": "复盘记录表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    portfolio_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="关联组合ID"
    )

    review_type: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="复盘类型: daily/weekly/monthly/adhoc"
    )
    review_date: Mapped[date] = mapped_column(Date, nullable=False, comment="复盘日期")

    market_summary: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="市场数据JSON"
    )
    market_analysis: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="用户市场分析"
    )

    position_summary: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="持仓数据JSON"
    )
    position_analysis: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="用户持仓分析"
    )

    trade_summary: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="交易数据JSON"
    )
    trade_analysis: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="用户交易分析"
    )

    strategy_summary: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="策略数据JSON"
    )
    strategy_analysis: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="用户策略分析"
    )

    profit_summary: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="盈亏数据JSON"
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True, comment="心得记录")

    next_plan: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="下期计划JSON"
    )

    ai_analysis: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="AI分析报告"
    )

    status: Mapped[str] = mapped_column(
        String(20), default="draft", comment="状态: draft/published"
    )
