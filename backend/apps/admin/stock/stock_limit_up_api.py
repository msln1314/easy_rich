#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_limit_up_api.py
# @IDE            : PyCharm
# @desc           : 涨停板分析API

from fastapi import APIRouter, Depends, Query
from typing import Optional
from pydantic import BaseModel
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger
from apps.admin.auth.utils.current import AllUserAuth, Auth
from utils.akshare_enhanced import get_ak_enhanced

router = APIRouter()


class LimitUpItem(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    date: Optional[str] = None
    first_time: Optional[str] = None
    last_time: Optional[str] = None
    count: Optional[int] = None
    reason: Optional[str] = None


@router.get("/limit_up/pool", summary="获取涨停板池")
async def get_zt_pool(
    date: Optional[str] = Query(None, description="日期 YYYYMMDD"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取当日涨停板股票列表"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_zt_pool(date)

        if df is None or df.empty:
            return SuccessResponse([])

        result = df.to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取涨停板池失败: {e}")
        return ErrorResponse(f"获取涨停板池失败: {str(e)}")


@router.get("/limit_down/pool", summary="获取跌停板池")
async def get_zt_pool_sub(
    date: Optional[str] = Query(None, description="日期 YYYYMMDD"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取当日跌停板股票列表"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_zt_pool_sub(date)

        if df is None or df.empty:
            return SuccessResponse([])

        result = df.to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取跌停板池失败: {e}")
        return ErrorResponse(f"获取跌停板池失败: {str(e)}")


@router.get("/limit_up/strong", summary="获取强势涨停板")
async def get_zt_pool_strong(
    date: Optional[str] = Query(None, description="日期 YYYYMMDD"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取强势涨停板(封板未打开)列表"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_zt_pool_strong(date)

        if df is None or df.empty:
            return SuccessResponse([])

        result = df.to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取强势涨停板失败: {e}")
        return ErrorResponse(f"获取强势涨停板失败: {str(e)}")


@router.get("/limit_up/broken", summary="获取炸板股票")
async def get_zt_pool_zbgc(
    date: Optional[str] = Query(None, description="日期 YYYYMMDD"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取炸板股票(涨停后打开)列表"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_zt_pool_zbgc(date)

        if df is None or df.empty:
            return SuccessResponse([])

        result = df.to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取炸板股票失败: {e}")
        return ErrorResponse(f"获取炸板股票失败: {str(e)}")


@router.get("/limit_up/statistics", summary="涨停板统计")
async def get_limit_up_statistics(
    date: Optional[str] = Query(None, description="日期 YYYYMMDD"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取涨停板统计数据"""
    try:
        ak = get_ak_enhanced()

        zt_df = await ak.get_zt_pool(date)
        dt_df = await ak.get_zt_pool_sub(date)
        strong_df = await ak.get_zt_pool_strong(date)
        broken_df = await ak.get_zt_pool_zbgc(date)

        result = {
            "limit_up_count": len(zt_df) if zt_df is not None else 0,
            "limit_down_count": len(dt_df) if dt_df is not None else 0,
            "strong_count": len(strong_df) if strong_df is not None else 0,
            "broken_count": len(broken_df) if broken_df is not None else 0,
            "broken_rate": round(len(broken_df) / len(zt_df) * 100, 2)
            if zt_df is not None and len(zt_df) > 0
            else 0,
        }

        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取涨停板统计失败: {e}")
        return ErrorResponse(f"获取涨停板统计失败: {str(e)}")
