from datetime import date, time
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Time, Text, SmallInteger, Index
from db.db_base import BaseModel


class InvestCalendarEvent(BaseModel):
    __tablename__ = "invest_calendar_event"
    __table_args__ = (
        Index("idx_event_date", "event_date"),
        Index("idx_event_type", "event_type"),
        Index("idx_date_type", "event_date", "event_type"),
        {"comment": "投资日历宏观事件表"},
    )

    event_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="事件类型: macro/policy/meeting"
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False, comment="事件标题")
    content: Mapped[str | None] = mapped_column(Text, nullable=True, comment="事件详情")

    event_date: Mapped[date] = mapped_column(Date, nullable=False, comment="事件日期")
    event_time: Mapped[time | None] = mapped_column(
        Time, nullable=True, comment="事件时间"
    )
    importance: Mapped[int] = mapped_column(
        SmallInteger, default=2, comment="重要程度: 1-低 2-中 3-高"
    )

    related_stocks: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="关联股票代码列表JSON"
    )
    related_sectors: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="关联板块列表JSON"
    )

    ai_analysis: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="AI分析的事件影响"
    )
    ai_sentiment: Mapped[int | None] = mapped_column(
        SmallInteger, nullable=True, comment="AI情感: 1-利好 2-中性 3-利空"
    )
    ai_suggestion: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="AI投资建议"
    )

    data_source: Mapped[str] = mapped_column(
        String(50), default="akshare", comment="数据来源"
    )
    source_url: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="来源链接"
    )
