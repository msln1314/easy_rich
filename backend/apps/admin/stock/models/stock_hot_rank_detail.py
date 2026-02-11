#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/31
# @File           : stock_hot_rank_detail.py
# @IDE            : PyCharm
# @desc           : 股票热度历史趋势及粉丝特征模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Float, Index, UniqueConstraint


class StockHotRankDetail(BaseModel):
    __tablename__ = "stock_hot_rank_detail"
    __table_args__ = (
        UniqueConstraint('stock_code', 'data_date', name='uk_stock_hot_rank'),
        Index('idx_stock_code', 'stock_code'),
        Index('idx_stock_name', 'stock_name'),
        Index('idx_data_date', 'data_date'),
        Index('idx_rank', 'rank'),
        Index('idx_created_at', 'created_at'),
        {'comment': '股票热度历史趋势及粉丝特征表'}
    )

    # 基础信息
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票代码")
    stock_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="股票名称")
    full_code: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="TS 股票代码")

    # 排名相关
    rank: Mapped[int] = mapped_column(Integer, nullable=False, comment="人气排名")
    rank_change: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="排名变化")

    # 热度相关
    hot_value: Mapped[float | None] = mapped_column(Float, nullable=True, comment="热度值")
    hot_value_change: Mapped[float | None] = mapped_column(Float, nullable=True, comment="热度值变化")

    # 价格相关
    current_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="最新价")
    change_percent: Mapped[float | None] = mapped_column(Float, nullable=True, comment="涨跌幅(%)")
    change_amount: Mapped[float | None] = mapped_column(Float, nullable=True, comment="涨跌额")

    # 成交相关
    volume: Mapped[float | None] = mapped_column(Float, nullable=True, comment="成交量(手)")
    amount: Mapped[float | None] = mapped_column(Float, nullable=True, comment="成交额(元)")
    turnover_rate: Mapped[float | None] = mapped_column(Float, nullable=True, comment="换手率(%)")
    amplitude: Mapped[float | None] = mapped_column(Float, nullable=True, comment="振幅(%)")

    # 市值相关
    total_market_cap: Mapped[float | None] = mapped_column(Float, nullable=True, comment="总市值(元)")
    circulating_market_cap: Mapped[float | None] = mapped_column(Float, nullable=True, comment="流通市值(元)")

    # 技术指标
    pe_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市盈率")
    pb_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市净率")
    volume_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="量比")

    # 时间相关
    data_date: Mapped[date] = mapped_column(DateTime, nullable=False, comment="数据日期")
    data_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="数据时间")

    # 粉丝特征
    fans_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="粉丝数量")
    fans_growth: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="粉丝增长")
    fans_attention_rate: Mapped[float | None] = mapped_column(Float, nullable=True, comment="粉丝关注度(%)")

    # 互动数据
    view_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="浏览量")
    comment_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="评论数")
    share_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="分享数")
    like_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="点赞数")

    # 情绪分析
    sentiment_score: Mapped[float | None] = mapped_column(Float, nullable=True, comment="情绪分数")
    sentiment_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="情绪类型：positive/negative/neutral")

    # 板块信息
    industry: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="所属行业")
    sector: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="所属板块")

    # 数据来源
    data_from: Mapped[str | None] = mapped_column(String(50), nullable=True, default="akshare", comment="数据来源")
