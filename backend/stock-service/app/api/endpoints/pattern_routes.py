# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : pattern_routes.py
# @IDE            : PyCharm
# @desc           : K线形态识别API路由

from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional

from app.services.pattern_service import pattern_service

router = APIRouter()


@router.get("/detect/{stock_code}", summary="检测所有形态")
async def detect_all_patterns(stock_code: str):
    """检测指定股票的所有K线形态"""
    try:
        result = await pattern_service.detect_all_patterns(stock_code)
        return {
            "stock_code": stock_code,
            "data": [r.__dict__ for r in result],
            "count": len(result),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detect/{stock_code}/w-bottom", summary="检测W底形态")
async def detect_w_bottom(stock_code: str):
    """检测W底（双底）形态 - 看涨信号"""
    try:
        result = await pattern_service.detect_w_bottom(stock_code)
        if result:
            return {"stock_code": stock_code, "data": result.__dict__}
        return {"stock_code": stock_code, "data": None, "message": "未检测到W底形态"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detect/{stock_code}/m-top", summary="检测M头形态")
async def detect_m_top(stock_code: str):
    """检测M头（双顶）形态 - 看跌信号"""
    try:
        result = await pattern_service.detect_m_top(stock_code)
        if result:
            return {"stock_code": stock_code, "data": result.__dict__}
        return {"stock_code": stock_code, "data": None, "message": "未检测到M头形态"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detect/{stock_code}/head-shoulders", summary="检测头肩形态")
async def detect_head_shoulders(stock_code: str):
    """检测头肩顶/头肩底形态"""
    try:
        result = await pattern_service.detect_head_shoulders(stock_code)
        if result:
            return {"stock_code": stock_code, "data": result.__dict__}
        return {"stock_code": stock_code, "data": None, "message": "未检测到头肩形态"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detect/{stock_code}/breakout", summary="检测突破形态")
async def detect_breakout(stock_code: str):
    """检测突破形态 - 向上或向下突破"""
    try:
        result = await pattern_service.detect_breakout(stock_code)
        if result:
            return {"stock_code": stock_code, "data": result.__dict__}
        return {"stock_code": stock_code, "data": None, "message": "未检测到突破形态"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scan", summary="批量扫描形态")
async def scan_patterns(
    stock_codes: List[str] = Body(..., description="股票代码列表"),
    pattern_type: Optional[str] = Body(
        None, description="形态类型: W_BOTTOM/M_TOP/HEAD_SHOULDERS/BREAKOUT"
    ),
):
    """批量扫描多只股票的K线形态"""
    try:
        result = await pattern_service.scan_patterns(stock_codes, pattern_type)
        return {"data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
