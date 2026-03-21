from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, SmallInteger, Index
from db.db_base import BaseModel


class RiskRule(BaseModel):
    __tablename__ = "risk_rule"
    __table_args__ = (
        Index("idx_rule_user_type", "user_id", "rule_type"),
        Index("idx_rule_active", "is_active"),
        {"comment": "雷区基线规则表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")

    rule_type: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="规则类型: trap/baseline"
    )
    category: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="分类"
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="规则名称")
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="规则描述"
    )

    severity: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="严重程度"
    )

    check_timing: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="检查时机JSON"
    )
    check_condition: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="触发条件JSON"
    )

    is_active: Mapped[int] = mapped_column(SmallInteger, default=1, comment="是否启用")
