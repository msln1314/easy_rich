from pydantic import BaseModel, Field  # 添加 Field 的导入
from typing import Optional, List
from datetime import datetime, date

class StockInfo(BaseModel):
    """个股基本信息模型"""
    code: str
    name: str
    industry: Optional[str] = None
    listing_date: Optional[str] = None
    total_market_value: Optional[float] = None
    circulating_market_value: Optional[float] = None
    total_share: Optional[float] = None
    circulating_share: Optional[float] = None
    
class StockQuote(BaseModel):
    """个股实时行情模型"""
    code: str
    name: str
    price: float
    change: float
    change_percent: float
    open: float
    high: float
    low: float
    volume: int
    amount: float
    turnover_rate: float
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    market_cap: Optional[float] = None
    update_time: datetime
    
class StockFinancial(BaseModel):
    """个股财务信息模型"""
    code: str
    name: str
    eps: Optional[float] = None
    bvps: Optional[float] = None
    roe: Optional[float] = None
    revenue: Optional[float] = None
    revenue_yoy: Optional[float] = None
    net_profit: Optional[float] = None
    net_profit_yoy: Optional[float] = None
    report_date: Optional[datetime] = None
    
class StockFundFlow(BaseModel):
    """个股资金流向模型"""
    code: str
    name: str
    date: datetime
    main_net_inflow: float
    main_net_inflow_percent: float
    super_large_net_inflow: float
    large_net_inflow: float
    medium_net_inflow: float
    small_net_inflow: float

class StockHistory(BaseModel):
    """个股历史行情数据模型"""
    stock_code: str = Field(..., description="股票代码")
    trade_date: str = Field(..., description="交易日期")
    open: float = Field(..., description="开盘价")
    close: float = Field(..., description="收盘价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    volume: int = Field(..., description="成交量(手)")
    amount: float = Field(..., description="成交额(元)")
    amplitude: float = Field(..., description="振幅(%)")
    change_percent: float = Field(..., description="涨跌幅(%)")
    change_amount: float = Field(..., description="涨跌额(元)")
    turnover: float = Field(..., description="换手率(%)")