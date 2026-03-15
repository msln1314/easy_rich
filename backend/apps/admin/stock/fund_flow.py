#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/15
# @File           : fund_flow.py
# @IDE            : PyCharm
# @desc           : 资金流向 API 接口

from fastapi import APIRouter, Depends, Query

from apps.admin.auth.utils.current import OpenAuth, Auth
from apps.admin.stock.services.fund_flow_service import (
    get_north_money_realtime,
    get_north_money_flow,
    get_market_fund_flow_today,
    get_market_fund_flow,
)
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger

router = APIRouter(tags=["资金流向"])


@router.get("/index/fund-flow/north-money/realtime", summary="获取实时北向资金")
async def get_north_money_realtime_api(
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取实时北向资金

    返回：
    - sh_hk_flow: 沪港通资金流向（亿元）
    - sz_hk_flow: 深港通资金流向（亿元）
    - total_flow: 北向资金合计（亿元）
    - update_time: 更新时间
    """
    try:
        result = await get_north_money_realtime()
        if result.get("code") != 200 and "data" not in result:
            return ErrorResponse(result.get("message", "获取实时北向资金失败"))
        return SuccessResponse(result.get("data", {}))
    except Exception as e:
        logger.error(f"获取实时北向资金失败: {str(e)}")
        return ErrorResponse(f"获取实时北向资金失败: {str(e)}")


@router.get("/index/fund-flow/north-money/flow", summary="获取北向资金历史流向")
async def get_north_money_flow_api(
    days: int = Query(30, ge=1, le=365, description="获取最近N天的数据"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取北向资金历史流向数据

    参数：
    - days: 获取最近N天的数据，默认30天
    """
    try:
        result = await get_north_money_flow(days)
        if result.get("code") != 200 and "data" not in result:
            return ErrorResponse(result.get("message", "获取北向资金历史失败"))
        return SuccessResponse(result.get("data", {}))
    except Exception as e:
        logger.error(f"获取北向资金历史失败: {str(e)}")
        return ErrorResponse(f"获取北向资金历史失败: {str(e)}")


@router.get("/index/fund-flow/market/flow/today", summary="获取今日市场资金流向")
async def get_market_fund_flow_today_api(
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取今日市场资金流向

    返回：
    - main_net_inflow: 主力净流入
    - main_net_inflow_pct: 主力净流入占比
    - super_large_net_inflow: 超大单净流入
    - large_net_inflow: 大单净流入
    - medium_net_inflow: 中单净流入
    - small_net_inflow: 小单净流入
    """
    try:
        result = await get_market_fund_flow_today()
        if result.get("code") != 200 and "data" not in result:
            return ErrorResponse(result.get("message", "获取今日市场资金流向失败"))
        return SuccessResponse(result.get("data", {}))
    except Exception as e:
        logger.error(f"获取今日市场资金流向失败: {str(e)}")
        return ErrorResponse(f"获取今日市场资金流向失败: {str(e)}")


@router.get("/index/fund-flow/market/flow", summary="获取市场资金流向历史")
async def get_market_fund_flow_api(
    days: int = Query(30, ge=1, le=365, description="获取最近N天的数据"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取市场资金流向历史数据

    参数：
    - days: 获取最近N天的数据，默认30天
    """
    try:
        result = await get_market_fund_flow(days)
        if result.get("code") != 200 and "data" not in result:
            return ErrorResponse(result.get("message", "获取市场资金流向历史失败"))
        return SuccessResponse(result.get("data", {}))
    except Exception as e:
        logger.error(f"获取市场资金流向历史失败: {str(e)}")
        return ErrorResponse(f"获取市场资金流向历史失败: {str(e)}")