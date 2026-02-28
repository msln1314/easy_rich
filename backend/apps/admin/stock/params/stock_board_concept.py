#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/31
# @File           : stock_board_concept.py
# @IDE            : PyCharm
# @desc           : 股票概念板块查询参数

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class StockBoardConceptParams(BaseModel):
    """股票概念板块查询参数"""

    board_name: Optional[str] = Field(None, description="板块名称")
    board_code: Optional[str] = Field(None, description="板块代码")
    change_percent_min: Optional[float] = Field(None, description="最小涨跌幅（%）")
    change_percent_max: Optional[float] = Field(None, description="最大涨跌幅（%）")
    net_inflow_min: Optional[float] = Field(None, description="最小净流入（亿元）")
    net_inflow_max: Optional[float] = Field(None, description="最大净流入（亿元）")
    date_at_start: Optional[str] = Field(None, description="数据日期开始")
    date_at_end: Optional[str] = Field(None, description="数据日期结束")
    leading_stock: Optional[str] = Field(None, description="领涨股")
    order_by: Optional[str] = Field(None, description="排序字段：change_percent/net_inflow/total_volume")
    order_type: Optional[str] = Field(None, description="排序方式：asc/desc")
    page: int = Field(1, description="页码")
    limit: int = Field(10, description="每页数量")

    class Config:
        # 允许通过 Query 参数传入
        extra = "allow"
