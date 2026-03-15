#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/12
# @File           : stock_quote.py
# @IDE            : PyCharm
# @desc           : 股票实时行情 API 接口

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Body

from apps.admin.auth.utils.current import OpenAuth, Auth
from apps.admin.stock.services.stock_service import StockQuoteService
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger

router = APIRouter(tags=["股票行情"])


@router.get("/stock/{stock_code}/quote", summary="获取单个股票实时行情")
async def get_stock_quote(
    stock_code: str,
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取单个股票实时行情

    支持的股票代码格式：
    - 000001 (自动识别市场)
    - 000001.SZ (标准格式)
    - sz000001 (新浪格式)

    数据源优先级：AKShare -> 新浪 -> 掘金量化
    """
    try:
        result = StockQuoteService.get_stock_quote(stock_code)

        if not result:
            return ErrorResponse(f"未找到股票 {stock_code} 的行情数据")

        return SuccessResponse(result)

    except Exception as e:
        logger.error(f"获取股票行情失败: {str(e)}")
        return ErrorResponse(f"获取股票行情失败: {str(e)}")


@router.post("/stock/quote/batch", summary="批量获取股票实时行情")
async def get_stock_quotes(
    stock_codes: List[str] = Body(..., description="股票代码列表"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    批量获取股票实时行情

    请求体示例：
    ["000001", "000002", "600000"]

    数据源优先级：AKShare -> 新浪 -> 掘金量化
    """
    try:
        if not stock_codes:
            return ErrorResponse("股票代码列表不能为空")

        if len(stock_codes) > 100:
            return ErrorResponse("单次查询数量不能超过100个")

        result = StockQuoteService.get_stock_quotes(stock_codes)

        return SuccessResponse(result)

    except Exception as e:
        logger.error(f"批量获取股票行情失败: {str(e)}")
        return ErrorResponse(f"批量获取股票行情失败: {str(e)}")


@router.get("/stock/{stock_code}/history", summary="获取股票历史K线")
async def get_stock_history(
    stock_code: str,
    period: str = Query("daily", description="周期: daily/weekly/monthly"),
    start_date: Optional[str] = Query(None, description="开始日期 YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYYMMDD"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取股票历史K线数据

    参数：
    - stock_code: 股票代码
    - period: 周期 (daily/weekly/monthly)
    - start_date: 开始日期 YYYYMMDD
    - end_date: 结束日期 YYYYMMDD

    数据源优先级：AKShare -> 掘金量化
    """
    try:
        result = StockQuoteService.get_stock_history(
            stock_code=stock_code,
            period=period,
            start_date=start_date,
            end_date=end_date,
        )

        return SuccessResponse(result)

    except Exception as e:
        logger.error(f"获取股票历史数据失败: {str(e)}")
        return ErrorResponse(f"获取股票历史数据失败: {str(e)}")


@router.get("/stock/{stock_code}/info", summary="获取股票基本信息和行情")
async def get_stock_info_with_quote(
    stock_code: str,
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取股票基本信息和实时行情

    返回股票的基本信息和实时行情数据
    """
    try:
        # 获取实时行情
        quote = StockQuoteService.get_stock_quote(stock_code)

        if not quote:
            return ErrorResponse(f"未找到股票 {stock_code} 的数据")

        return SuccessResponse({
            **quote,
            "query_time": datetime.now().isoformat(),
        })

    except Exception as e:
        logger.error(f"获取股票信息失败: {str(e)}")
        return ErrorResponse(f"获取股票信息失败: {str(e)}")