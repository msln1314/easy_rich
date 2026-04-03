# backend/qmt-service/app/api/endpoints/position_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models.position_models import (
    PositionListResponse,
    Balance,
    TradeListResponse,
)
from app.services.position_service import position_service

router = APIRouter()


@router.get("/list", response_model=PositionListResponse, summary="查询持仓列表")
async def get_positions():
    """查询持仓列表"""
    try:
        return await position_service.get_positions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/balance", response_model=Balance, summary="查询资金余额")
async def get_balance():
    """查询资金余额"""
    try:
        return await position_service.get_balance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trades", response_model=TradeListResponse, summary="查询成交记录")
async def get_trades(
    date: Optional[str] = Query(None, description="日期（YYYYMMDD）"),
    stock_code: Optional[str] = Query(None, description="股票代码筛选")
):
    """查询成交记录"""
    try:
        return await position_service.get_trades(date, stock_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trades/today", response_model=TradeListResponse, summary="查询今日成交")
async def get_today_trades():
    """查询今日成交"""
    try:
        return await position_service.get_today_trades()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))