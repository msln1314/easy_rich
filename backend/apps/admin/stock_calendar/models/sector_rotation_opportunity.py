from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Text, SmallInteger, Float
from db.db_base import BaseModel


class SectorRotationOpportunity(BaseModel):
    __tablename__ = "sector_rotation_opportunity"
    __table_args__ = {"comment": "板块轮动机会表"}

    sector_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="板块名称"
    )
    sector_code: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="板块代码"
    )

    opportunity_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="机会类型: seasonal/policy/event"
    )
    start_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="机会开始日期"
    )
    end_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="机会结束日期"
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="AI置信度评分 0-100"
    )
    historical_return: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="历史平均收益率"
    )
    win_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="历史胜率"
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="机会描述"
    )
    ai_analysis: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="AI详细分析"
    )
    related_stocks: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="相关个股列表JSON"
    )

    is_active: Mapped[int] = mapped_column(SmallInteger, default=1, comment="是否有效")
