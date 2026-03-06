#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/1
# @File           : stock_fund_flow.py
# @IDE            : PyCharm
# @desc           : 股票资金流向模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Index


class StockFundFlow(BaseModel):
    """个股资金流向模型"""
    __tablename__ = "stock_fund_flow"
    __table_args__ = (
        Index('idx_stock_code_date', 'stock_code', 'trade_date'),
        Index('idx_stock_code', 'stock_code'),
        Index('idx_trade_date', 'trade_date'),
        Index('idx_main_net_inflow', 'main_net_inflow'),
        Index('idx_main_net_inflow_percent', 'main_net_inflow_percent'),
        Index('idx_super_large_net_inflow', 'super_large_net_inflow'),
        {'comment': '个股资金流向表'}
    )

    # 股票信息
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票代码")
    stock_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="股票名称")
    full_code: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="全称")
    
    # 交易日期
    trade_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="交易日期")
    
    # 主力资金流向
    main_net_inflow: Mapped[float] = mapped_column(Float, nullable=False, comment="主力净流入(元)")
    main_net_inflow_percent: Mapped[float] = mapped_column(Float, nullable=False, comment="主力净流入占比(%)")
    
    # 超大单资金流向
    super_large_net_inflow: Mapped[float] = mapped_column(Float, nullable=False, comment="超大单净流入(元)")
    
    # 大单资金流向
    large_net_inflow: Mapped[float] = mapped_column(Float, nullable=False, comment="大单净流入(元)")
    
    # 中单资金流向
    medium_net_inflow: Mapped[float] = mapped_column(Float, nullable=False, comment="中单净流入(元)")
    
    # 小单资金流向
    small_net_inflow: Mapped[float] = mapped_column(Float, nullable=False, comment="小单净流入(元)")
    
    # 时间信息
    data_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="数据时间（采集时间）")
    
    # 数据来源
    data_from: Mapped[str | None] = mapped_column(String(50), nullable=True, default="akshare", comment="数据来源：akshare")
