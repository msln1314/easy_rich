#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_analysis.py
# @IDE            : PyCharm
# @desc           : 股票分析 pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr,DecimalField
from datetime import date, datetime



class StockAnalysisCreate(BaseModel):
    """创建股票分析"""
    stock_code: str = Field(..., description="股票代码")
    stock_name: str | None = Field(None, description="股票名称")
    stock_industry: str | None = Field(None, description="股票行业")

    analysis_price: DecimalField | None = Field(None, description="分析时的价格")
    open_price: DecimalField | None = Field(None, description="分析时的开盘价")
    high_price: DecimalField | None = Field(None, description="分析时的最高价")
    low_price: DecimalField | None = Field(None, description="分析时的最低价")
    analysis_change_percent: DecimalField | None = Field(None, description="分析时的涨幅（%）")
    analysis_turnover_rate: DecimalField | None = Field(None, description="分析时的换手率（%）")
    analysis_volume_ratio: DecimalField | None = Field(None, description="分析时的量比")
    volume: DecimalField | None = Field(None, description="分析时的成交量（手）")
    circulating_market_cap: DecimalField | None = Field(None, description="分析时的流通市值（万元）")
    total_market_cap: DecimalField | None = Field(None, description="分析时的总市值（万元）")
    analysis_type: str | None = Field(None, description="分析类型：技术分析/基本面分析/消息面分析/综合分析")
    analysis_period: str | None = Field(None, description="分析周期：短线/中线/长线")
    hold_type: str | None = Field(None, description="持有类型：短线/中线/长线")

    ma5: DecimalField | None = Field(None, description="5日均线")
    ma10: DecimalField | None = Field(None, description="10日均线")
    ma20: DecimalField | None = Field(None, description="20日均线")
    rsi: DecimalField | None = Field(None, description="RSI指标")
    macd: DecimalField | None = Field(None, description="MACD值")
    amount: DecimalField | None = Field(None, description="分析时的成交额（万元）")
    pe_ratio: DecimalField | None = Field(None, description="分析时的市盈率")
    pb_ratio: DecimalField | None = Field(None, description="分析时的市净率")
    notes: str | None = Field(None, description="备注信息")
    user_id: int | None = Field(None, description="用户ID")
    is_send: int | None = Field(None, description="是否发送")
    is_valid : int | None = Field(default=0, description="是否有效：1有效 0无效")
    score: int | None = Field(None, description="评分")
    

class StockAnalysisUpdateVerification(BaseModel):
    """股票分析输出"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_valid: int = Field(1, description="是否有效：1有效 0无效")
    is_verified: int | None = Field(0, description="是否已验证：0未验证 1已验证")
    verification_result: str | None = Field(None, description="验证结果：正确/错误/部分正确")
    verification_date: date | None = Field(None, description="验证日期")
  

class StockAnalysisUpdate(BaseModel):
    """更新股票分析"""
    stock_code: str | None = Field(None, description="股票代码")
    stock_name: str | None = Field(None, description="股票名称")
    stock_industry: str | None = Field(None, description="股票行业")
    analysis_date: date | None = Field(None, description="分析日期")
    action_position: str | None = Field(None, description="操作仓位")
    ev: DecimalField | None = Field(None, description="期望收益值")
    hold_period: str | None = Field(None, description="持仓周期")
    action_range: str | None = Field(None, description="操作区间")
    risk_rate: str | None = Field(None, description="风险收益比")
    stop_price: DecimalField | None = Field(None, description="止损价格")
    target_price: DecimalField | None = Field(None, description="目标价格")
    confidence_value: DecimalField | None = Field(None, description="置信值")
    trade_time: datetime | None = Field(None, description="交易时间")
    analysis_time: datetime | None = Field(None, description="分析时间")
    analysis_result: str | None = Field(None, description="分析结果：看涨/看跌/中性")
    analysis_content: str | None = Field(None, description="分析内容/分析报告")
    analysis_summary: str | None = Field(None, description="分析摘要")
    analysis_price: DecimalField | None = Field(None, description="分析时的价格")
    open_price: DecimalField | None = Field(None, description="分析时的开盘价")
    high_price: DecimalField | None = Field(None, description="分析时的最高价")
    low_price: DecimalField | None = Field(None, description="分析时的最低价")
    analysis_change_percent: DecimalField | None = Field(None, description="分析时的涨幅（%）")
    analysis_turnover_rate: DecimalField | None = Field(None, description="分析时的换手率（%）")
    analysis_volume_ratio: DecimalField | None = Field(None, description="分析时的量比")
    volume: DecimalField | None = Field(None, description="分析时的成交量（手）")
    circulating_market_cap: DecimalField | None = Field(None, description="分析时的流通市值（万元）")
    total_market_cap: DecimalField | None = Field(None, description="分析时的总市值（万元）")
    analysis_type: str | None = Field(None, description="分析类型：技术分析/基本面分析/消息面分析/综合分析")
    analysis_period: str | None = Field(None, description="分析周期：短线/中线/长线")
    hold_type: str | None = Field(None, description="持有类型：短线/中线/长线")
    risk_level: str | None = Field(None, description="风险等级：low/medium/high")
    ma5: DecimalField | None = Field(None, description="5日均线")
    ma10: DecimalField | None = Field(None, description="10日均线")
    ma20: DecimalField | None = Field(None, description="20日均线")
    rsi: DecimalField | None = Field(None, description="RSI指标")
    macd: DecimalField | None = Field(None, description="MACD值")
    amount: DecimalField | None = Field(None, description="分析时的成交额（万元）")
    pe_ratio: DecimalField | None = Field(None, description="分析时的市盈率")
    pb_ratio: DecimalField | None = Field(None, description="分析时的市净率")
    analysis_source: str | None = Field(None, description="分析来源：system系统/manual人工/ai人工智能")
    analyzer: str | None = Field(None, description="分析人/分析师")
    is_valid: int | None = Field(None, description="是否有效：1有效 0无效")
    is_verified: int | None = Field(None, description="是否已验证：0未验证 1已验证")
    verification_result: str | None = Field(None, description="验证结果：正确/错误/部分正确")
    verification_date: date | None = Field(None, description="验证日期")
    tags: str | None = Field(None, description="标签，多个用逗号分隔")
    notes: str | None = Field(None, description="备注信息")
    user_id: int | None = Field(None, description="用户ID")
    operation_price_range: str | None = Field(None, description="建仓价格")
    operation_direction: str | None = Field(None, description="操作建议 买入 观望")
    data_from: str | None = Field(None, description="触发来源")
    report: str | None = Field(None, description="分析报告MD 格式")
    is_send: int | None = Field(None, description="是否发送")
    score: int | None = Field(None, description="评分")
    main_risks: str | None = Field(None, description="风险")
    key_catalysts: str | None = Field(None, description="催化剂")
    price_action: str | None = Field(None, description="价格行为")
    trend_judgment: str | None = Field(None, description="趋势")
    resistance: str | None = Field(None, description="压力位")
    support: str | None = Field(None, description="支撑位")
    valuation: str | None = Field(None, description="核心价值指标")
    market_sentiment: str | None = Field(None, description="市场情绪")


class StockAnalysisOut(BaseModel):
    """股票分析输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    stock_code: str
    stock_name: str | None = None
    stock_industry: str | None = None
    analysis_date: DatetimeStr | None = None
    action_position: str | None = None
    ev: DecimalField | None = None
    hold_period: str | None = None
    action_range: str | None = None
    risk_rate: str | None = None
    stop_price: DecimalField | None = None
    target_price: DecimalField | None = None
    confidence_value: DecimalField | None = None
    trade_time: DatetimeStr | None = None
    analysis_time: DatetimeStr | None = None
    analysis_result: str | None = None
    analysis_content: str | None = None
    analysis_summary: str | None = None
    analysis_price: DecimalField | None = None
    open_price: DecimalField | None = None
    high_price: DecimalField | None = None
    low_price: DecimalField | None = None
    analysis_change_percent: DecimalField | None = None
    analysis_turnover_rate: DecimalField | None = None
    analysis_volume_ratio: DecimalField | None = None
    volume: DecimalField | None = None
    circulating_market_cap: DecimalField | None = None
    total_market_cap: DecimalField | None = None
    analysis_type: str | None = None
    analysis_period: str | None = None
    hold_type: str | None = None
    risk_level: str | None = None
    ma5: DecimalField | None = None
    ma10: DecimalField | None = None
    ma20: DecimalField | None = None
    rsi: DecimalField | None = None
    macd: DecimalField | None = None
    amount: DecimalField | None = None
    pe_ratio: DecimalField | None = None
    pb_ratio: DecimalField | None = None
    analysis_source: str | None = None
    analyzer: str | None = None
    is_valid: int | None = None
    is_verified: int | None = None
    verification_result: str | None = None
    verification_date: DatetimeStr | None = None
    tags: str | None = None
    notes: str | None = None
    user_id: int | None = None
    operation_price_range: str | None = None
    operation_direction: str | None = None
    data_from: str | None = None
    report: str | None = None
    is_send: int | None = None
    score: int | None = None
    main_risks: str | None = None
    key_catalysts: str | None = None
    price_action: str | None = None
    trend_judgment: str | None = None
    resistance: str | None = None
    support: str | None = None
    valuation: str | None = None
    market_sentiment: str | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr
