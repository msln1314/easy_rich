#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_watchlist.py
# @IDE            : PyCharm
# @desc           : 股票关注列表 pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr, DecimalField
from datetime import date, datetime

class StockWatchlistCreate(BaseModel):
    """创建股票关注列表"""
    expire_at: date | None = Field(None, description="到期时间")
    date_at: datetime = Field(..., description="时间")
    full_code: str | None = Field(None, description="TS 股票代码")
    stock_code: str = Field(..., description="股票代码")
    stock_name: str | None = Field(None, description="股票名称")
    user_id: int = Field(..., description="用户ID")
    category: str | None = Field(None, description="关注分类：自选股/热点股/潜力股/风险股等")
    tags: str | None = Field(None, description="标签，多个用逗号分隔")
    follow_remark: str | None = Field(None, description="关注备注原因")
    follow_reason: str | None = Field(None, description="关注原因")
    priority: int | None = Field(3, description="关注优先级：1高 2中 3低")
    follow_price: DecimalField = Field(None, description="关注时的股票价格")
    follow_change_percent: DecimalField = Field(None, description="关注时的涨跌幅百分比")
    follow_volume: DecimalField = Field(None, description="关注时的成交量（手）")
    follow_turnover_rate: DecimalField = Field(None, description="关注时的换手率百分比")
    follow_volume_ratio: DecimalField = Field(None, description="关注时的量比")
    follow_pe_ratio: DecimalField = Field(None, description="关注时的市盈率")
    follow_pb_ratio: DecimalField = Field(None, description="关注时的市净率")
    follow_market_cap: DecimalField = Field(None, description="关注时的总市值（万元）")
    follow_ma5: DecimalField = Field(None, description="关注时5日均线")
    follow_ma10: DecimalField = Field(None, description="关注时10日均线")
    follow_ma20: DecimalField = Field(None, description="关注时20日均线")
    follow_rsi: DecimalField = Field(None, description="关注时RSI指标")
    data_from: str | None = Field(None, description="数据来源")


class StockWatchlistUpdate(BaseModel):
    """更新股票关注列表"""
    expire_at: date | None = Field(None, description="到期时间")
    date_at: datetime | None = Field(None, description="时间")
    full_code: str | None = Field(None, description="TS 股票代码")
    stock_code: str | None = Field(None, description="股票代码")
    stock_name: str | None = Field(None, description="股票名称")
    user_id: int | None = Field(None, description="用户ID")
    category: str | None = Field(None, description="关注分类：自选股/热点股/潜力股/风险股等")
    tags: str | None = Field(None, description="标签，多个用逗号分隔")
    follow_remark: str | None = Field(None, description="关注备注原因")
    follow_reason: str | None = Field(None, description="关注原因")
    priority: int | None = Field(None, description="关注优先级：1高 2中 3低")
    follow_price: DecimalField = Field(None, description="关注时的股票价格")
    follow_change_percent: DecimalField = Field(None, description="关注时的涨跌幅百分比")
    follow_volume: DecimalField = Field(None, description="关注时的成交量（手）")
    follow_turnover_rate: DecimalField = Field(None, description="关注时的换手率百分比")
    follow_volume_ratio: DecimalField = Field(None, description="关注时的量比")
    follow_pe_ratio: DecimalField = Field(None, description="关注时的市盈率")
    follow_pb_ratio: DecimalField = Field(None, description="关注时的市净率")
    follow_market_cap: DecimalField = Field(None, description="关注时的总市值（万元）")
    follow_ma5: DecimalField = Field(None, description="关注时5日均线")
    follow_ma10: DecimalField = Field(None, description="关注时10日均线")
    follow_ma20: DecimalField = Field(None, description="关注时20日均线")
    follow_rsi: DecimalField = Field(None, description="关注时RSI指标")
    last_follow_price: DecimalField = Field(None, description="关注时的股票价格")
    last_follow_change_percent: DecimalField = Field(None, description="关注时的涨跌幅百分比")
    last_follow_volume: DecimalField = Field(None, description="关注时的成交量（手）")
    last_follow_turnover_rate: DecimalField = Field(None, description="关注时的换手率百分比")
    last_follow_volume_ratio: DecimalField = Field(None, description="关注时的量比")
    last_follow_pe_ratio: DecimalField = Field(None, description="关注时的市盈率")
    last_follow_pb_ratio: DecimalField = Field(None, description="关注时的市净率")
    last_follow_market_cap: DecimalField = Field(None, description="关注时的总市值（万元）")
    is_active: int | None = Field(None, description="是否关注：1关注中 0已取消")
    watch_days: int | None = Field(None, description="关注天数")
    max_price: DecimalField = Field(None, description="关注期间最高价")
    min_price: DecimalField = Field(None, description="关注期间最低价")
    max_change_percent: DecimalField = Field(None, description="关注期间最大涨幅百分比")
    min_change_percent: DecimalField = Field(None, description="关注期间最大跌幅百分比")
    data_from: str | None = Field(None, description="数据来源")
    follow_bwteen_change_percent: DecimalField = Field(None, description="关注期间涨幅 当前价格减去关注价格处于关注价格")
    follow_bwteen_max_change_percent: DecimalField = Field(None, description="关注期间最大涨幅 最大值减去关注价格除以关注价格")
    follow_bwteen_min_change_percent: DecimalField = Field(None, description="关注期间最大跌幅 最小值减去关注价格除以关注价格")
    max_turnover_rate: DecimalField = Field(None, description="最大换手率")
    min_turnover_rate: DecimalField = Field(None, description="最小换手率")
    max_volume_ratio: DecimalField = Field(None, description="最大量比")
    min_volume_ratio: DecimalField = Field(None, description="最小量比")
    max_volume: DecimalField = Field(None, description="最大成交量")
    min_volume: DecimalField = Field(None, description="最小成交量")
    is_analyze: int | None = Field(None, description="是否已分析")


class StockWatchlistOut(BaseModel):
    """股票关注列表输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    expire_at: date | None = None
    date_at: DatetimeStr
    full_code: str | None = None
    stock_code: str
    stock_name: str | None = None
    user_id: int
    category: str | None = None
    tags: str | None = None
    follow_remark: str | None = None
    follow_reason: str | None = None
    priority: int | None = None
    follow_price: DecimalField
    follow_change_percent: DecimalField
    follow_volume: DecimalField
    follow_turnover_rate: DecimalField
    follow_volume_ratio: DecimalField
    follow_pe_ratio: DecimalField
    follow_pb_ratio: DecimalField
    follow_market_cap: DecimalField
    follow_ma5: DecimalField
    follow_ma10: DecimalField
    follow_ma20: DecimalField
    follow_rsi: DecimalField
    last_follow_price: DecimalField
    last_follow_change_percent: DecimalField
    last_follow_volume: DecimalField
    last_follow_turnover_rate: DecimalField
    last_follow_volume_ratio: DecimalField
    last_follow_pe_ratio: DecimalField
    last_follow_pb_ratio: DecimalField
    last_follow_market_cap: DecimalField
    is_active: int
    watch_days: int | None = None
    max_price: DecimalField
    min_price: DecimalField
    max_change_percent: DecimalField
    min_change_percent: DecimalField
    data_from: str | None = None
    follow_bwteen_change_percent: DecimalField
    follow_bwteen_max_change_percent: DecimalField
    follow_bwteen_min_change_percent: DecimalField
    max_turnover_rate: DecimalField
    min_turnover_rate: DecimalField
    max_volume_ratio: DecimalField
    min_volume_ratio: DecimalField
    max_volume: DecimalField
    min_volume: DecimalField
    is_analyze: int | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr
