# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : institution_routes.py
# @IDE            : PyCharm
# @desc           : 机构数据API路由 - 机构调研、基金持股等

from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional
from datetime import datetime

from app.services.institution_service import institution_service
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


# ========== 机构调研 ==========


@router.get("/research/list", summary="获取机构调研列表")
async def get_research_list(
    start_date: Optional[str] = Query(
        None, description="开始日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
    end_date: Optional[str] = Query(
        None, description="结束日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
):
    """获取机构调研列表数据"""
    try:
        result = await institution_service.get_research_list(
            start_date=start_date, end_date=end_date
        )
        return {
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取机构调研列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/research/stock/{stock_code}", summary="获取个股机构调研")
async def get_research_by_stock(
    stock_code: str = Path(..., description="股票代码"),
):
    """获取个股被机构调研的历史记录"""
    try:
        result = await institution_service.get_research_by_stock(stock_code=stock_code)
        return {
            "stock_code": stock_code,
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取个股机构调研失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 基金持股 ==========


@router.get("/fund-holding/stock/{stock_code}", summary="获取个股基金持股")
async def get_fund_holding(
    stock_code: str = Path(..., description="股票代码"),
):
    """获取个股被基金持有的情况"""
    try:
        result = await institution_service.get_fund_holding(stock_code=stock_code)
        return {
            "stock_code": stock_code,
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取基金持股失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 北向资金 ==========


@router.get("/north-holding", summary="获取北向资金持股")
async def get_north_holding(
    top: int = Query(50, ge=1, le=200, description="返回数量"),
):
    """获取北向资金持股排名"""
    try:
        result = await institution_service.get_north_holding(top=top)
        return {
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取北向资金持股失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/north-holding/stock/{stock_code}", summary="获取个股北向资金持股")
async def get_north_holding_by_stock(
    stock_code: str = Path(..., description="股票代码"),
):
    """获取个股北向资金持股情况"""
    try:
        result = await institution_service.get_north_holding_by_stock(
            stock_code=stock_code
        )
        if result is None:
            return {
                "stock_code": stock_code,
                "data": None,
                "message": "未找到该股票的北向资金持股数据",
            }
        return {
            "stock_code": stock_code,
            "data": result.__dict__,
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取个股北向资金持股失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 主力持仓 ==========


@router.get("/main-force/stock/{stock_code}", summary="获取个股主力持仓")
async def get_main_force_holding(
    stock_code: str = Path(..., description="股票代码"),
):
    """获取个股主力持仓变化"""
    try:
        result = await institution_service.get_main_force_holding(stock_code=stock_code)
        return {
            "stock_code": stock_code,
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取主力持仓失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
