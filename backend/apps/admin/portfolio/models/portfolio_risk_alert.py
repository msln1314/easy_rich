from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, SmallInteger, Text, DateTime, Index
from db.db_base import BaseModel


class PortfolioRiskAlert(BaseModel):
    __tablename__ = "portfolio_risk_alert"
    __table_args__ = (
        Index("idx_alert_portfolio", "portfolio_id"),
        Index("idx_alert_type", "alert_type"),
        Index("idx_alert_level", "alert_level"),
        {"comment": "风控预警表"},
    )

    portfolio_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="组合ID")
    alert_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="预警类型"
    )
    alert_level: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="预警级别"
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="预警标题")
    content: Mapped[str | None] = mapped_column(Text, nullable=True, comment="预警详情")

    related_stock_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="关联股票代码"
    )
    related_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="相关数值"
    )
    threshold_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="阈值"
    )

    is_read: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否已读")
    is_handled: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否处理")
    handle_note: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="处理备注"
    )
    handled_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="处理时间"
    )
