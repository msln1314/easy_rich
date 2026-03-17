# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : screener_routes.py
# @IDE            : PyCharm
# @desc           : 股票筛选器API路由

from fastapi import APIRouter, Query, HTTPException, Body
from typing import List, Dict, Any
from datetime import datetime

from app.services.screener_service import screener_service

router = APIRouter()


@router.post("/stocks", summary="条件选股")
async def screen_by_condition(
    conditions: List[Dict[str, Any]] = Body(..., description="筛选条件列表"),
    limit: int = Query(50, ge=1, le=200, description="返回数量"),
):
    """根据条件筛选股票，支持多条件组合"""
    try:
        result = await screener_service.screen_by_condition(conditions, limit)
        return {"data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/limit-up", summary="涨停股筛选")
async def screen_limit_up(limit: int = Query(50, ge=1, le=200)):
    """筛选当日涨停股票"""
    try:
        result = await screener_service.screen_limit_up(limit)
        return {"data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/limit-down", summary="跌停股筛选")
async def screen_limit_down(limit: int = Query(50, ge=1, le=200)):
    """筛选当日跌停股票"""
    try:
        result = await screener_service.screen_limit_down(limit)
        return {"data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/high-turnover", summary="高换手率筛选")
async def screen_high_turnover(limit: int = Query(50, ge=1, le=200)):
    """筛选高换手率股票(>10%)"""
    try:
        result = await screener_service.screen_high_turnover(limit)
        return {"data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/low-pe", summary="低估值筛选")
async def screen_low_pe(limit: int = Query(50, ge=1, le=200)):
    """筛选低市盈率股票(0<PE<20)"""
    try:
        result = await screener_service.screen_low_pe(limit)
        return {"data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/volume-surge", summary="放量股票筛选")
async def screen_volume_surge(limit: int = Query(50, ge=1, le=200)):
    """筛选成交额排名前10%的股票"""
    try:
        result = await screener_service.screen_volume_surge(limit)
        return {"data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/small-cap", summary="小市值筛选")
async def screen_small_cap(limit: int = Query(50, ge=1, le=200)):
    """筛选小市值股票(<50亿)"""
    try:
        result = await screener_service.screen_small_cap(limit)
        return {"data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
