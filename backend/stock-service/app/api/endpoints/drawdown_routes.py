# backend/stock-service/app/api/endpoints/drawdown_routes.py
# -*- coding: utf-8 -*-
"""
回撤分析API路由
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import date

from app.models.drawdown_models import (
    DrawdownAnalysisResult,
    PullbackSignal,
    PositionMonitor,
    DrawdownHistoryData,
    DrawdownAnalyzeRequest,
    PositionMonitorRequest,
)
from app.services.drawdown_service import DrawdownService

router = APIRouter()
drawdown_service = DrawdownService()


@router.post("/analyze", response_model=DrawdownAnalysisResult)
async def analyze_drawdown(request: DrawdownAnalyzeRequest):
    """
    回撤分析

    分析指定股票的历史回撤情况，返回各项指标
    """
    try:
        result = await drawdown_service.analyze_drawdown(
            stock_code=request.stock_code,
            start_date=request.start_date,
            end_date=request.end_date,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/signals/{stock_code}", response_model=list[PullbackSignal])
async def get_pullback_signals(stock_code: str):
    """
    获取回调买点信号

    基于技术支撑位、历史回撤规律、量价配合判断买点
    """
    try:
        signals = await drawdown_service.get_pullback_signals(stock_code)
        return signals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取信号失败: {str(e)}")


@router.post("/position", response_model=PositionMonitor)
async def monitor_position(request: PositionMonitorRequest):
    """
    持仓监控

    输入成本价和买入日期，监控盈利/亏损和回撤情况
    """
    try:
        result = await drawdown_service.monitor_position(
            stock_code=request.stock_code,
            cost_price=request.cost_price,
            position_date=request.position_date,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"监控失败: {str(e)}")


@router.get("/history/{stock_code}", response_model=DrawdownHistoryData)
async def get_history_data(
    stock_code: str,
    threshold: float = Query(5.0, ge=1, le=50, description="回撤阈值(%)"),
):
    """
    获取历史回撤图表数据

    用于前端ECharts展示回撤走势图
    """
    try:
        result = await drawdown_service.get_history_data(stock_code, threshold)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史数据失败: {str(e)}")