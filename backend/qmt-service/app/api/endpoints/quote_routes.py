# backend/qmt-service/app/api/endpoints/quote_routes.py
"""
L2行情API路由
"""
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException

from app.services.quote_service import quote_service
from app.models.quote_models import (
    L2Quote,
    L2QuoteListResponse,
    TickListResponse,
    MinuteBarListResponse,
    DepthResponse,
    QuoteStatus,
)

router = APIRouter()


@router.get("/l2/{stock_code}", response_model=L2Quote, summary="获取L2十档行情")
async def get_l2_quote(stock_code: str):
    """
    获取单只股票的L2十档行情数据

    - **stock_code**: 股票代码，如 000001.SZ
    """
    quote = await quote_service.get_l2_quote(stock_code)
    if not quote:
        raise HTTPException(status_code=404, detail=f"未找到 {stock_code} 的行情数据")
    return quote


@router.post("/l2/batch", response_model=L2QuoteListResponse, summary="批量获取L2行情")
async def get_l2_quotes(stock_codes: List[str] = Query(..., description="股票代码列表")):
    """
    批量获取多只股票的L2十档行情

    - **stock_codes**: 股票代码列表
    """
    return await quote_service.get_l2_quotes(stock_codes)


@router.get("/ticks/{stock_code}", response_model=TickListResponse, summary="获取逐笔成交")
async def get_ticks(
    stock_code: str,
    start_time: Optional[str] = Query(None, description="开始时间，格式: YYYYMMDD HH:MM:SS"),
    end_time: Optional[str] = Query(None, description="结束时间"),
    count: int = Query(100, ge=1, le=1000, description="返回条数")
):
    """
    获取逐笔成交数据

    - **stock_code**: 股票代码
    - **start_time**: 开始时间
    - **end_time**: 结束时间
    - **count**: 返回条数，默认100
    """
    return await quote_service.get_ticks(stock_code, start_time, end_time, count)


@router.get("/minute/{stock_code}", response_model=MinuteBarListResponse, summary="获取分时数据")
async def get_minute_bars(
    stock_code: str,
    date: Optional[str] = Query(None, description="日期，格式: YYYYMMDD")
):
    """
    获取分时数据

    - **stock_code**: 股票代码
    - **date**: 日期，不传则返回今日数据
    """
    return await quote_service.get_minute_bars(stock_code, date)


@router.get("/depth/{stock_code}", response_model=DepthResponse, summary="获取订单簿深度")
async def get_depth(stock_code: str):
    """
    获取订单簿深度数据（十档买卖盘）

    - **stock_code**: 股票代码
    """
    return await quote_service.get_depth(stock_code)


@router.post("/subscribe", response_model=QuoteStatus, summary="订阅行情")
async def subscribe_quotes(stock_codes: List[str] = Query(..., description="要订阅的股票代码列表")):
    """
    订阅行情推送

    - **stock_codes**: 股票代码列表
    """
    return await quote_service.subscribe_quotes(stock_codes)


@router.delete("/subscribe", response_model=QuoteStatus, summary="取消订阅")
async def unsubscribe_quotes(stock_codes: Optional[List[str]] = Query(None, description="要取消的股票代码，为空则取消全部")):
    """
    取消行情订阅

    - **stock_codes**: 股票代码列表，为空则取消全部订阅
    """
    return await quote_service.unsubscribe_quotes(stock_codes)


@router.get("/subscribe/status", response_model=QuoteStatus, summary="获取订阅状态")
async def get_subscription_status():
    """获取当前行情订阅状态"""
    return quote_service.get_subscription_status()