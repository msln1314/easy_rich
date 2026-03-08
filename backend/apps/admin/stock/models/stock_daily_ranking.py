#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2026/3/8
# @File : stock_daily_ranking.py
# @IDE : PyCharm
# @desc : 个股每日排行历史数据模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import (
    String,
    DateTime,
    Integer,
    Float,
    Index,
    UniqueConstraint,
    SmallInteger,
)


class StockDailyRanking(BaseModel):
    """
    个股每日排行历史数据表
    每日收盘后存储各类排行数据，便于历史查询和趋势分析
    """

    __tablename__ = "stock_daily_ranking"
    __table_args__ = (
        # 联合唯一约束：确保同一天同一排行类型下每只股票只有一条记录
        UniqueConstraint(
            "stock_code", "data_date", "ranking_type", name="uk_stock_daily_ranking"
        ),
        Index("idx_data_date", "data_date"),
        Index("idx_ranking_type", "ranking_type"),
        Index("idx_rank", "rank"),
        Index("idx_stock_code", "stock_code"),
        Index("idx_created_at", "created_at"),
        {"comment": "个股每日排行历史数据表"},
    )

    # 基础信息
    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码（如000001）"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="股票名称"
    )
    full_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="完整股票代码（如SZ000001）"
    )

    # 排行类型
    ranking_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="排行类型: volume(成交量) turnover(换手率) amount(成交额) change_percent(涨跌幅) hot(热度)",
    )

    # 排名信息
    rank: Mapped[int] = mapped_column(Integer, nullable=False, comment="当日排名")
    rank_change: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="排名变化（与上一交易日对比）"
    )

    # 排行指标值（根据排行类型不同，存储对应的指标值）
    ranking_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="排行指标值"
    )
    ranking_value_unit: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="数值单位"
    )

    # 市场信息
    market: Mapped[str | None] = mapped_column(
        String(10), nullable=True, comment="市场类型：SZ深交所/SH上交所"
    )
    industry: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="所属行业"
    )

    # 股票关键指标快照（存储排行时的股票状态，便于历史查询）
    current_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="最新价（元）"
    )
    change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨跌幅（%）"
    )
    change_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨跌额（元）"
    )

    volume: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="成交量（手）"
    )
    amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="成交额（元）"
    )
    turnover_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="换手率（%）"
    )

    total_market_cap: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="总市值（元）"
    )
    circulating_market_cap: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="流通市值（元）"
    )

    # 热度相关（仅热度排行使用）
    hot_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="热度值"
    )
    hot_rank_change: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="热度排名变化"
    )

    # 时间信息
    data_date: Mapped[date] = mapped_column(
        DateTime, nullable=False, comment="数据日期"
    )

    # 数据来源
    data_source: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="akshare", comment="数据来源"
    )
