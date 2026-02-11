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

    concept_name: Optional[str] = Field(None, description="概念名称")
    concept_code: Optional[str] = Field(None, description="概念代码")
    change_percent_min: Optional[float] = Field(None, description="最小涨跌幅（%）")
    change_percent_max: Optional[float] = Field(None, description="最大涨跌幅（%）")
    net_inflow_min: Optional[float] = Field(None, description="最小净流入（亿元）")
    net_inflow_max: Optional[float] = Field(None, description="最大净流入（亿元）")
    date_at: Optional[date] = Field(None, description="数据日期")
    date_at_start: Optional[date] = Field(None, description="开始日期")
    date_at_end: Optional[date] = Field(None, description="结束日期")
    data_from: Optional[str] = Field(None, description="数据来源")
    page: Optional[int] = Field(1, description="页码")
    limit: Optional[int] = Field(20, description="每页数量")
    ordering: Optional[str] = Field("-created_at", description="排序字段")
