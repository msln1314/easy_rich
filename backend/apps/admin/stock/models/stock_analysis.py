#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_analysis.py
# @IDE            : PyCharm
# @desc           : 股票分析模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Text, Index, UniqueConstraint, Numeric


class StockAnalysis(BaseModel):
    __tablename__ = "stock_analysis"
    __table_args__ = (
        UniqueConstraint('stock_code', 'analysis_date', 'analysis_time', name='uk_stock_analysis_time'),
        Index('idx_stock_code', 'stock_code'),
        Index('idx_stock_name', 'stock_name'),
        Index('idx_analysis_date', 'analysis_date'),
        Index('idx_analysis_result', 'analysis_result'),
        Index('idx_analysis_type', 'analysis_type'),
        Index('idx_risk_level', 'risk_level'),
        Index('idx_created_at', 'created_at'),
        {'comment': '股票分析表'}
    )

    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票代码")
    stock_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="股票名称")
    stock_industry: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="股票行业")
    analysis_date: Mapped[date | None] = mapped_column(DateTime, nullable=True, comment="分析日期")
    action_position: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="操作仓位")
    ev: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="期望收益值")
    hold_period: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="持仓周期")
    action_range: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="操作区间")
    risk_rate: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="风险收益比")
    stop_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="止损价格")
    target_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="目标价格")
    confidence_value: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="置信值")
    trade_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="交易时间")
    analysis_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="分析时间")
    analysis_result: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="分析结果：看涨/看跌/中性")
    analysis_content: Mapped[str | None] = mapped_column(Text, nullable=True, comment="分析内容/分析报告")
    analysis_summary: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="分析摘要")
    analysis_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="分析时的价格")
    open_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="分析时的开盘价")
    high_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="分析时的最高价")
    low_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="分析时的最低价")
    analysis_change_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="分析时的涨幅（%）")
    analysis_turnover_rate: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="分析时的换手率（%）")
    analysis_volume_ratio: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="分析时的量比")
    volume: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True, comment="分析时的成交量（手）")
    circulating_market_cap: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="分析时的流通市值（万元）")
    total_market_cap: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="分析时的总市值（万元）")
    analysis_type: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="分析类型：技术分析/基本面分析/消息面分析/综合分析")
    analysis_period: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="分析周期：短线/中线/长线")
    hold_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="持有类型：短线/中线/长线")
    risk_level: Mapped[str | None] = mapped_column(String(20), nullable=True, default="medium", comment="风险等级：low/medium/high")
    ma5: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="5日均线")
    ma10: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="10日均线")
    ma20: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="20日均线")
    rsi: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="RSI指标")
    macd: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True, comment="MACD值")
    amount: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="分析时的成交额（万元）")
    pe_ratio: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="分析时的市盈率")
    pb_ratio: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="分析时的市净率")
    analysis_source: Mapped[str | None] = mapped_column(String(50), nullable=True, default="system", comment="分析来源：system系统/manual人工/ai人工智能")
    analyzer: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="分析人/分析师")
    is_valid: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否有效：1有效 0无效")
    is_verified: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0, comment="是否已验证：0未验证 1已验证")
    verification_result: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="验证结果：正确/错误/部分正确")
    verification_date: Mapped[date | None] = mapped_column(DateTime, nullable=True, comment="验证日期")
    tags: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="标签，多个用逗号分隔")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注信息")
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="用户ID")
    operation_price_range: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="建仓价格")
    operation_direction: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="操作建议 买入 观望")
    data_from: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="触发来源")
    report: Mapped[str | None] = mapped_column(Text, nullable=True, comment="分析报告MD 格式")
    is_send: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="是否发送")
    score: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="评分")
    main_risks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="风险")
    key_catalysts: Mapped[str | None] = mapped_column(String(512), nullable=True, comment="催化剂")
    price_action: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="价格行为")
    trend_judgment: Mapped[str | None] = mapped_column(String(512), nullable=True, comment="趋势")
    resistance: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="压力位")
    support: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="支撑位")
    valuation: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="核心价值指标")
    market_sentiment: Mapped[str | None] = mapped_column(String(512), nullable=True, comment="市场情绪")
