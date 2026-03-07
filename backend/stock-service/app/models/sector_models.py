from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ConceptBoard(BaseModel):
    """概念板块模型"""
    rank: int = Field(..., description="排名")
    name: str = Field(..., description="板块名称")
    code: str = Field(..., description="板块代码")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌额")
    change_percent: float = Field(..., description="涨跌幅(%)")
    market_value: Optional[int] = Field(None, description="总市值")
    turnover_rate: float = Field(..., description="换手率(%)")
    up_count: int = Field(..., description="上涨家数")
    down_count: int = Field(..., description="下跌家数")
    leading_stock: str = Field(..., description="领涨股票")
    leading_stock_change_percent: float = Field(..., description="领涨股票涨跌幅(%)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class IndustryBoard(BaseModel):
    """行业板块模型"""
    rank: int = Field(..., description="排名")
    name: str = Field(..., description="板块名称")
    code: str = Field(..., description="板块代码")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌额")
    change_percent: float = Field(..., description="涨跌幅(%)")
    market_value: Optional[int] = Field(None, description="总市值")
    turnover_rate: float = Field(..., description="换手率(%)")
    up_count: int = Field(..., description="上涨家数")
    down_count: int = Field(..., description="下跌家数")
    leading_stock: str = Field(..., description="领涨股票")
    leading_stock_change_percent: float = Field(..., description="领涨股票涨跌幅(%)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class BoardSpot(BaseModel):
    """通用板块实时行情详情模型"""
    name: str = Field(..., description="板块名称")
    price: float = Field(..., description="最新价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    open: float = Field(..., description="开盘价")
    volume: float = Field(..., description="成交量")
    amount: float = Field(..., description="成交额")
    turnover_rate: float = Field(..., description="换手率(%)")
    change: float = Field(..., description="涨跌额")
    change_percent: float = Field(..., description="涨跌幅(%)")
    amplitude: float = Field(..., description="振幅(%)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class ConceptBoardSpot(BoardSpot):
    """概念板块实时行情详情模型"""
    pass


class IndustryBoardSpot(BoardSpot):
    """行业板块实时行情详情模型"""
    pass


class ConceptBoardConstituent(BaseModel):
    """概念板块成份股模型"""
    rank: int = Field(..., description="序号")
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change_percent: float = Field(..., description="涨跌幅(%)")
    change: float = Field(..., description="涨跌额")
    volume: float = Field(..., description="成交量(手)")
    amount: float = Field(..., description="成交额")
    amplitude: float = Field(..., description="振幅(%)")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    open: float = Field(..., description="今开")
    pre_close: float = Field(..., description="昨收")
    turnover_rate: float = Field(..., description="换手率(%)")
    pe_ratio: Optional[float] = Field(None, description="市盈率-动态")
    pb_ratio: Optional[float] = Field(None, description="市净率")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class IndustryBoardConstituent(BaseModel):
    """行业板块成份股模型"""
    rank: int = Field(..., description="序号")
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change_percent: float = Field(..., description="涨跌幅(%)")
    change: float = Field(..., description="涨跌额")
    volume: float = Field(..., description="成交量(手)")
    amount: float = Field(..., description="成交额")
    amplitude: float = Field(..., description="振幅(%)")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    open: float = Field(..., description="今开")
    pre_close: float = Field(..., description="昨收")
    turnover_rate: float = Field(..., description="换手率(%)")
    pe_ratio: Optional[float] = Field(None, description="市盈率-动态")
    pb_ratio: Optional[float] = Field(None, description="市净率")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")