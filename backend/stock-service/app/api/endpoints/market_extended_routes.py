# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : market_extended_routes.py
# @IDE            : PyCharm
# @desc           : 市场扩展API路由 - 涨停池、跌停池、异动等

from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional
from datetime import datetime

from app.services.market_extended_service import market_extended_service
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


# ========== 涨停池接口 ==========


@router.get("/zt-pool", summary="获取涨停池")
async def get_zt_pool(
    trade_date: Optional[str] = Query(
        None, description="交易日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
):
    """获取当日涨停股票池，包含连板数、开板次数、涨停原因等"""
    try:
        result = await market_extended_service.get_zt_pool(trade_date=trade_date)
        return {
            "trade_date": trade_date or datetime.now().strftime("%Y%m%d"),
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取涨停池失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zt-pool/strong", summary="获取强势股池")
async def get_zt_pool_strong(
    trade_date: Optional[str] = Query(
        None, description="交易日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
):
    """获取强势股池，连续涨停或多次涨停的强势股"""
    try:
        result = await market_extended_service.get_zt_pool_strong(trade_date=trade_date)
        return {
            "trade_date": trade_date or datetime.now().strftime("%Y%m%d"),
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取强势股池失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zt-pool/zhaban", summary="获取炸板池")
async def get_zt_pool_zhaban(
    trade_date: Optional[str] = Query(
        None, description="交易日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
):
    """获取涨停炸板池，曾经涨停但收盘未封住的股票"""
    try:
        result = await market_extended_service.get_zt_pool_zb(trade_date=trade_date)
        return {
            "trade_date": trade_date or datetime.now().strftime("%Y%m%d"),
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取炸板池失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 跌停池接口 ==========


@router.get("/dt-pool", summary="获取跌停池")
async def get_dt_pool(
    trade_date: Optional[str] = Query(
        None, description="交易日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
):
    """获取当日跌停股票池"""
    try:
        result = await market_extended_service.get_dt_pool(trade_date=trade_date)
        return {
            "trade_date": trade_date or datetime.now().strftime("%Y%m%d"),
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取跌停池失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 次新股池接口 ==========


@router.get("/sub-new-pool", summary="获取次新股池")
async def get_sub_new_pool(
    trade_date: Optional[str] = Query(
        None, description="交易日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
):
    """获取次新股池，近一年上市的股票"""
    try:
        result = await market_extended_service.get_sub_new_pool(trade_date=trade_date)
        return {
            "trade_date": trade_date or datetime.now().strftime("%Y%m%d"),
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取次新股池失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 异动数据接口 ==========


@router.get("/realtime-alert", summary="获取实时异动")
async def get_realtime_alert():
    """获取实时异动数据，包括快速拉升、快速下跌等"""
    try:
        result = await market_extended_service.get_realtime_alert()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取实时异动失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fast-up", summary="获取快速上涨股票")
async def get_fast_up():
    """获取快速上涨的股票列表"""
    try:
        result = await market_extended_service.get_fast_up()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取快速上涨股票失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 综合接口 ==========


@router.get("/all-pools", summary="获取所有池数据")
async def get_all_pools(
    trade_date: Optional[str] = Query(
        None, description="交易日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
):
    """一次性获取涨停池、跌停池、强势股池、次新股池所有数据"""
    try:
        result = await market_extended_service.get_all_pools(trade_date=trade_date)
        return result
    except Exception as e:
        logger.error(f"获取所有池数据失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activity", summary="获取市场活跃度")
async def get_market_activity():
    """获取市场活跃度统计，包括涨跌家数、涨停跌停数等"""
    try:
        result = await market_extended_service.get_market_activity_legu()
        if result is None:
            return {"data": None, "message": "暂无市场活跃度数据"}
        return {"data": result.__dict__, "update_time": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"获取市场活跃度失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
