# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/21
# @File           : etf_routes.py
# @IDE            : PyCharm
# @desc           : ETF资金流向API路由

from fastapi import APIRouter, Query
from app.services.etf_service import etf_service
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/overview")
async def get_etf_overview(top: int = Query(10, ge=1, le=50)):
    """获取ETF资金流向概览（包含净流入、申购、赎回排行）"""
    try:
        data = await etf_service.get_etf_overview(top)
        return {"data": data}
    except Exception as e:
        logger.error(f"获取ETF资金流向概览失败: {e}")
        return {"data": None, "error": str(e)}


@router.get("/net-flow")
async def get_etf_net_flow_rank(top: int = Query(20, ge=1, le=100)):
    """获取ETF资金净流入排行"""
    try:
        data = await etf_service.get_etf_fund_flow_rank(top)
        return {"data": data, "total": len(data)}
    except Exception as e:
        logger.error(f"获取ETF净流入排行失败: {e}")
        return {"data": [], "total": 0, "error": str(e)}


@router.get("/subscribe")
async def get_etf_subscribe_rank(top: int = Query(10, ge=1, le=50)):
    """获取ETF申购排行"""
    try:
        data = await etf_service.get_etf_subscribe_rank(top)
        return {"data": data, "total": len(data)}
    except Exception as e:
        logger.error(f"获取ETF申购排行失败: {e}")
        return {"data": [], "total": 0, "error": str(e)}


@router.get("/redeem")
async def get_etf_redeem_rank(top: int = Query(10, ge=1, le=50)):
    """获取ETF赎回排行"""
    try:
        data = await etf_service.get_etf_redeem_rank(top)
        return {"data": data, "total": len(data)}
    except Exception as e:
        logger.error(f"获取ETF赎回排行失败: {e}")
        return {"data": [], "total": 0, "error": str(e)}
