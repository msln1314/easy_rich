from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, DateTime, Index
from db.db_base import BaseModel


class RuleViolation(BaseModel):
    __tablename__ = "rule_violation"
    __table_args__ = (
        Index("idx_viol_user_time", "user_id", "violation_time"),
        Index("idx_viol_rule", "rule_id"),
        {"comment": "违规记录表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    rule_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="规则ID")

    violation_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="违规时间"
    )
    violation_context: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="违规上下文JSON"
    )

    related_stock_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="关联股票代码"
    )
    related_trade_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="关联交易ID"
    )

    user_note: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="用户备注"
    )
