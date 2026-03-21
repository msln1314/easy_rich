from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, Index
from db.db_base import BaseModel


class ExperienceNote(BaseModel):
    __tablename__ = "experience_note"
    __table_args__ = (
        Index("idx_exp_user_id", "user_id"),
        Index("idx_exp_category", "category"),
        Index("idx_exp_created", "created_at"),
        {"comment": "心得经验表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")

    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="内容")

    category: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="分类"
    )
    tags: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="标签JSON数组"
    )

    related_stocks: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="关联股票代码JSON"
    )
    related_trades: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="关联交易ID JSON"
    )
    related_review_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="关联复盘ID"
    )

    mood: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="心情")
    importance: Mapped[str] = mapped_column(
        String(20), default="normal", comment="重要程度"
    )

    view_count: Mapped[int] = mapped_column(Integer, default=0, comment="查看次数")
