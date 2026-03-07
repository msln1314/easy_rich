from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class MarginDetail(BaseModel):
    """融资融券明细模型"""
    trade_date: date = Field(..., description="交易日期")
    stock_code: str = Field(..., description="证券代码")
    stock_name: str = Field(..., description="证券简称")
    market: str = Field(..., description="市场(上海/深圳)")
    financing_buy: int = Field(..., description="融资买入额(元)")
    financing_balance: int = Field(..., description="融资余额(元)")
    financing_repay: Optional[int] = Field(None, description="融资偿还额(元)")
    securities_sell: int = Field(..., description="融券卖出量(股/份)")
    securities_balance: int = Field(..., description="融券余量(股/份)")
    securities_repay: Optional[int] = Field(None, description="融券偿还量(股/份)")
    securities_balance_amount: Optional[int] = Field(None, description="融券余额(元)")
    margin_balance: Optional[int] = Field(None, description="融资融券余额(元)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class StockHotRank(BaseModel):
    """股票热度排名模型"""
    rank: int = Field(..., description="当前排名")
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌额")
    change_percent: float = Field(..., description="涨跌幅(%)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class StockHotUpRank(BaseModel):
    """股票飙升榜模型"""
    rank_change: int = Field(..., description="排名较昨日变动")
    rank: int = Field(..., description="当前排名")
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌额")
    change_percent: float = Field(..., description="涨跌幅(%)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")

class StockHotKeyword(BaseModel):
    """股票热门关键词模型"""
    time: datetime = Field(..., description="时间")
    stock_code: str = Field(..., description="股票代码")
    concept_name: str = Field(..., description="概念名称")
    concept_code: str = Field(..., description="概念代码")
    heat: int = Field(..., description="热度")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")