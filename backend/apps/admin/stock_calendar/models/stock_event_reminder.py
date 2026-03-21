from datetime import time
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String,
    SmallInteger,
    Integer,
    Time,
    DateTime,
    UniqueConstraint,
    Index,
)
from db.db_base import BaseModel


class StockEventReminder(BaseModel):
    __tablename__ = "stock_event_reminder"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "stock_code", "event_id", name="uk_user_stock_event"
        ),
        Index("idx_user_active", "user_id", "is_active"),
        {"comment": "用户事件提醒表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    event_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="事件ID")

    remind_days: Mapped[int] = mapped_column(
        Integer, default=1, comment="提前几天提醒: 1-7"
    )
    remind_time: Mapped[time] = mapped_column(
        Time, default=time(9, 0), comment="提醒时间"
    )
    remind_type: Mapped[str] = mapped_column(
        String(20), default="system", comment="提醒方式: system/email"
    )
    is_active: Mapped[int] = mapped_column(SmallInteger, default=1, comment="是否启用")

    last_remind_at: Mapped[str | None] = mapped_column(
        DateTime, nullable=True, comment="上次提醒时间"
    )
