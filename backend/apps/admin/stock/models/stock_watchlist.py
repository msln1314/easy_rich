#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_watchlist.py
# @IDE            : PyCharm
# @desc           : 股票关注列表模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Text, Index, UniqueConstraint, Numeric


class StockWatchlist(BaseModel):
    __tablename__ = "stock_watchlist"
    __table_args__ = (
        UniqueConstraint('stock_code', 'user_id', 'date_at', name='uk_watchlist'),
        Index('idx_user_id', 'user_id'),
        Index('idx_category', 'category'),
        Index('idx_is_active', 'is_active'),
        Index('idx_created_at', 'created_at'),
        {'comment': '股票关注列表表'}
    )

    expire_at: Mapped[date | None] = mapped_column(DateTime, nullable=True, comment="到期时间")
    date_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="时间")
    full_code: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票代码")
    stock_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="股票名称")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    category: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="关注分类：自选股/热点股/潜力股/风险股等")
    tags: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="标签，多个用逗号分隔")
    follow_remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="关注备注原因")
    follow_reason: Mapped[str | None] = mapped_column(Text, nullable=True, comment="关注原因")
    priority: Mapped[int | None] = mapped_column(Integer, nullable=True, default=3, comment="关注优先级：1高 2中 3低")
    follow_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注时的股票价格")
    follow_change_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注时的涨跌幅百分比")
    follow_volume: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True, comment="关注时的成交量（手）")
    follow_turnover_rate: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注时的换手率百分比")
    follow_volume_ratio: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注时的量比")
    follow_pe_ratio: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注时的市盈率")
    follow_pb_ratio: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注时的市净率")
    follow_market_cap: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="关注时的总市值（万元）")
    follow_ma5: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注时5日均线")
    follow_ma10: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注时10日均线")
    follow_ma20: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注时20日均线")
    follow_rsi: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注时RSI指标")
    last_follow_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注时的股票价格")
    last_follow_change_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注时的涨跌幅百分比")
    last_follow_volume: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True, comment="关注时的成交量（手）")
    last_follow_turnover_rate: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注时的换手率百分比")
    last_follow_volume_ratio: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注时的量比")
    last_follow_pe_ratio: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注时的市盈率")
    last_follow_pb_ratio: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注时的市净率")
    last_follow_market_cap: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="关注时的总市值（万元）")
    is_active: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否关注：1关注中 0已取消")
    watch_days: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0, comment="关注天数")
    max_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注期间最高价")
    min_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="关注期间最低价")
    max_change_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注期间最大涨幅百分比")
    min_change_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注期间最大跌幅百分比")
    data_from: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="数据来源")
    follow_bwteen_change_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注期间涨幅 当前价格减去关注价格处于关注价格")
    follow_bwteen_max_change_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注期间最大涨幅 最大值减去关注价格除以关注价格")
    follow_bwteen_min_change_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="关注期间最大跌幅 最小值减去关注价格除以关注价格")
    max_turnover_rate: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="最大换手率")
    min_turnover_rate: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="最小换手率")
    max_volume_ratio: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="最大量比")
    min_volume_ratio: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="最小量比")
    max_volume: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True, comment="最大成交量")
    min_volume: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True, comment="最小成交量")
    is_analyze: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0, comment="是否已分析")
