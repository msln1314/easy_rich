#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/21
# @File           : stock_selection_signal.py
# @IDE            : PyCharm
# @desc           : 选股信号模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Integer, Index, Text


class StockSelectionSignal(BaseModel):
    """
    选股信号表
    存储每日股票技术信号和评分
    """

    __tablename__ = "stock_selection_signal"
    __table_args__ = (
        Index("idx_signal_stock_date", "stock_code", "signal_date"),
        Index("idx_signal_date", "signal_date"),
        Index("idx_signal_score", "total_score"),
        Index("idx_signal_recommend", "recommend"),
        {"comment": "选股信号表"},
    )

    # 股票基本信息
    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="股票名称"
    )
    full_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="完整代码"
    )
    market: Mapped[str | None] = mapped_column(
        String(10), nullable=True, comment="市场(SH/SZ)"
    )
    industry: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="所属行业"
    )

    # 信号日期
    signal_date: Mapped[date] = mapped_column(
        DateTime, nullable=False, comment="信号日期"
    )

    # 价格信息
    current_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="当前价格"
    )
    change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨跌幅(%)"
    )
    volume: Mapped[float | None] = mapped_column(Float, nullable=True, comment="成交量")
    amount: Mapped[float | None] = mapped_column(Float, nullable=True, comment="成交额")

    # 技术指标信号
    ma_signal: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="均线信号(1金叉/-1死叉/0无)"
    )
    macd_signal: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="MACD信号(1金叉/-1死叉/0无)"
    )
    kdj_signal: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="KDJ信号(1金叉/-1死叉/0无)"
    )
    rsi_signal: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="RSI信号(1超卖/-1超买/0无)"
    )
    boll_signal: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="布林带信号(1下轨支撑/-1上轨压力/0无)"
    )
    volume_signal: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="成交量信号(1放量/-1缩量/0无)"
    )

    # 技术指标值
    ma5: Mapped[float | None] = mapped_column(Float, nullable=True, comment="MA5")
    ma10: Mapped[float | None] = mapped_column(Float, nullable=True, comment="MA10")
    ma20: Mapped[float | None] = mapped_column(Float, nullable=True, comment="MA20")
    dif: Mapped[float | None] = mapped_column(Float, nullable=True, comment="DIF")
    dea: Mapped[float | None] = mapped_column(Float, nullable=True, comment="DEA")
    macd: Mapped[float | None] = mapped_column(Float, nullable=True, comment="MACD柱")
    k_value: Mapped[float | None] = mapped_column(Float, nullable=True, comment="K值")
    d_value: Mapped[float | None] = mapped_column(Float, nullable=True, comment="D值")
    j_value: Mapped[float | None] = mapped_column(Float, nullable=True, comment="J值")
    rsi_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="RSI值"
    )

    # 分项评分
    macd_score: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="MACD评分"
    )
    kdj_score: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="KDJ评分"
    )
    rsi_score: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="RSI评分"
    )
    ma_score: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="均线评分"
    )
    volume_score: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="成交量评分"
    )
    trend_score: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="趋势评分"
    )
    potential_score: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="潜力评分"
    )

    # 综合评分
    total_score: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="综合评分(0-100)"
    )
    score_rank: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="评分排名"
    )

    # 推荐信号
    recommend: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="推荐信号(strong_buy/buy/hold/sell/strong_sell)",
    )
    signal_strength: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="信号强度(1-5)"
    )
    confidence: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="置信度(0-1)"
    )

    # 风险指标
    volatility: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="波动率"
    )
    max_drawdown: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="最大回撤"
    )

    # 信号详情
    signal_detail: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="信号详情(JSON)"
    )

    # 数据来源
    data_from: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="system", comment="数据来源"
    )
    data_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="数据生成时间"
    )
