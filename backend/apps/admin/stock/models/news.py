#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/1/27
# @File           : news.py
# @IDE            : PyCharm
# @desc           : 新闻信息模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Text, Integer, Index, Numeric


class News(BaseModel):
    __tablename__ = "news"
    __table_args__ = (
        Index('ix_news_name', 'name'),
        Index('all', 'is_send', 'priority', 'date_at', 'is_analyze'),
        {'comment': '新闻信息表'}
    )

    name: Mapped[str] = mapped_column(String(250), nullable=False, comment="新闻标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    data_from: Mapped[str] = mapped_column(String(255), nullable=False, comment="数据来源")
    agent: Mapped[str] = mapped_column(String(255), nullable=False, comment="代理")
    tag: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="标签")
    is_send: Mapped[int] = mapped_column(Integer, nullable=False, comment="是否发送")
    priority: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="优先级 1 2 3 4")
    date_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="新闻日期")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="AI分析")
    url: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="链接")
    category: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="板块")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True, comment="大纲")
    views: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="浏览量")
    is_analyze: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="是否分析")
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="分析时间")
    geo_scope: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="全球范围")
    industry_scope: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="行业范围")
    impact_on_business: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="企业影响")
    impact_on_industry: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="行业影响")
    impact_on_market: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="市场影响")
    policy_level: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="政策级别")
    policy_intensity: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="政策力度")
    time_sensitivity: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="时间敏感性")
    market_expectation: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="市场预期")
    eps_impact: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="收益影响 正面还是负面")
    primary_sectors: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="受影响板块")
    secondary_sectors: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="间接传导板块")
    style_rotation: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="价值/成长/防御/周期风格影响")
    has_concept_stocks: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="是否有概念股")
    recommendation_level: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="推荐级别")
    confidence_level: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="置信级别")
    confidence_score: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="置信度")
    concept_stocks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="相关股 json")
    risks: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="风险")
    key_points: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="要点")
    analysis_report: Mapped[str | None] = mapped_column(Text, nullable=True, comment="分析报告")
    score: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="评分")
