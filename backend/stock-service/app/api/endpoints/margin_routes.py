# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : margin_routes.py
# @IDE            : PyCharm
# @desc           : 融资融券API路由

from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional
from datetime import datetime

from app.services.margin_service import margin_service
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/summary", summary="获取融资融券汇总")
async def get_margin_summary(
    exchange: str = Query("沪深京A股", description="交易所类型"),
):
    """获取融资融券市场汇总数据"""
    try:
        result = await margin_service.get_margin_summary(exchange=exchange)
        if result is None:
            return {"data": None, "message": "暂无融资融券汇总数据"}
        return {"data": result, "update_time": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"获取融资融券汇总失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detail", summary="获取融资融券明细")
async def get_margin_detail(
    trade_date: Optional[str] = Query(
        None, description="交易日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
):
    """获取融资融券明细数据，按股票列出"""
    try:
        result = await margin_service.get_margin_detail(trade_date=trade_date)
        return {
            "trade_date": trade_date or datetime.now().strftime("%Y%m%d"),
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取融资融券明细失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/{stock_code}", summary="获取个股融资融券")
async def get_stock_margin(
    stock_code: str = Path(..., description="股票代码"),
):
    """获取个股融资融券历史数据"""
    try:
        result = await margin_service.get_stock_margin(stock_code=stock_code)
        return {
            "stock_code": stock_code,
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取个股融资融券失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rank", summary="获取融资融券排名")
async def get_margin_rank(
    indicator: str = Query("融资余额", description="排名指标"),
    top: int = Query(50, ge=1, le=200, description="返回数量"),
):
    """获取融资融券排名，按融资余额或融券余额排序"""
    try:
        result = await margin_service.get_margin_rank(indicator=indicator, top=top)
        return {
            "indicator": indicator,
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取融资融券排名失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
