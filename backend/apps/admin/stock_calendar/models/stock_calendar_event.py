from datetime import date, time
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Time, Text, Float, SmallInteger, Index
from db.db_base import BaseModel


class StockCalendarEvent(BaseModel):
    __tablename__ = "stock_calendar_event"
    __table_args__ = (
        Index("idx_stock_code", "stock_code"),
        Index("idx_event_date", "event_date"),
        Index("idx_event_type", "event_type"),
        Index("idx_date_type", "event_date", "event_type"),
        {"comment": "个股日历事件表"},
    )

    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="股票名称"
    )

    event_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="事件类型"
    )
    event_date: Mapped[date] = mapped_column(Date, nullable=False, comment="事件日期")
    event_time: Mapped[time | None] = mapped_column(
        Time, nullable=True, comment="事件时间"
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False, comment="事件标题")
    content: Mapped[str | None] = mapped_column(Text, nullable=True, comment="事件详情")

    impact_data: Mapped[dict | None] = mapped_column(
        Text, nullable=True, comment="事件影响数据JSON"
    )

    ai_impact_score: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="影响评分 -5~5"
    )
    ai_sentiment: Mapped[int | None] = mapped_column(
        SmallInteger, nullable=True, comment="情感: 1-利好 2-中性 3-利空"
    )
    ai_analysis: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="AI影响分析"
    )
    ai_suggestion: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="AI操作建议"
    )

    is_in_watchlist: Mapped[int] = mapped_column(
        SmallInteger, default=0, comment="是否在用户自选股中"
    )
    data_source: Mapped[str] = mapped_column(
        String(50), default="akshare", comment="数据来源"
    )
    source_url: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="来源链接"
    )
