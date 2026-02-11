#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : stock_base_info.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from datetime import date


class StockBaseInfoCreate(BaseModel):
    """创建股票基本信息"""
    full_code: str = Field(..., description="TS 股票代码")
    stock_code: str | None = Field(None, description="股票代码")
    name: str | None = Field(None, description="股票名称")
    area: str | None = Field(None, description="地域")
    industry: str | None = Field(None, description="所属行业")
    cnspell: str | None = Field(None, description="拼音缩写")
    market: str | None = Field(None, description="市场类型")
    list_date: date | None = Field(None, description="上市日期")
    act_name: str | None = Field(None, description="实际控制人名称")
    act_ent_type: str | None = Field(None, description="实际控制人企业类型")
    is_hs: str | None = Field(None, description="是否沪深港通标的")
    delist_date: date | None = Field(None, description="退市日期")
    status: str | None = Field(None, description="上市状态")


class StockBaseInfoUpdate(BaseModel):
    """更新股票基本信息"""
    full_code: str | None = Field(None, description="TS 股票代码")
    stock_code: str | None = Field(None, description="股票代码")
    name: str | None = Field(None, description="股票名称")
    area: str | None = Field(None, description="地域")
    industry: str | None = Field(None, description="所属行业")
    cnspell: str | None = Field(None, description="拼音缩写")
    market: str | None = Field(None, description="市场类型")
    list_date: date | None = Field(None, description="上市日期")
    act_name: str | None = Field(None, description="实际控制人名称")
    act_ent_type: str | None = Field(None, description="实际控制人企业类型")
    is_hs: str | None = Field(None, description="是否沪深港通标的")
    delist_date: date | None = Field(None, description="退市日期")
    status: str | None = Field(None, description="上市状态")







class StockBaseInfoOut(BaseModel):
    """股票基本信息输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_code: str
    stock_code: str | None = None
    name: str | None = None
    area: str | None = None
    industry: str | None = None
    cnspell: str | None = None
    market: str | None = None
    list_date: date | None = None
    act_name: str | None = None
    act_ent_type: str | None = None
    is_hs: str | None = None
    delist_date: date | None = None
    status: str | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr

