# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : stock_extended_routes.py
# @IDE            : PyCharm
# @desc           : 股票扩展API路由 - 龙虎榜、资金流、财务等

from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional, List
from datetime import datetime

from app.services.stock_extended_service import stock_extended_service
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


# ========== 龙虎榜接口 ==========


@router.get("/lhb/list", summary="获取龙虎榜数据")
async def get_lhb_list(
    trade_date: Optional[str] = Query(
        None, description="交易日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
    start_date: Optional[str] = Query(
        None, description="开始日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
    end_date: Optional[str] = Query(
        None, description="结束日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
):
    """
    获取龙虎榜数据

    - **trade_date**: 交易日期，如 20260316
    - **start_date**: 开始日期（与end_date配合使用）
    - **end_date**: 结束日期
    """
    try:
        result = await stock_extended_service.get_lhb_list(
            trade_date=trade_date, start_date=start_date, end_date=end_date
        )
        return {
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取龙虎榜失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lhb/stock/{stock_code}", summary="获取个股龙虎榜")
async def get_lhb_by_stock(
    stock_code: str = Path(..., description="股票代码"),
    days: int = Query(30, ge=1, le=365, description="查询天数"),
):
    """
    获取个股龙虎榜历史数据

    - **stock_code**: 股票代码，如 000001
    - **days**: 查询天数，默认30天
    """
    try:
        result = await stock_extended_service.get_lhb_by_stock(
            stock_code=stock_code, days=days
        )
        return {
            "stock_code": stock_code,
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取个股龙虎榜失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 资金流向接口 ==========


@router.get("/fund-flow/stock/{stock_code}", summary="获取个股资金流向")
async def get_stock_fund_flow(
    stock_code: str = Path(..., description="股票代码"),
):
    """
    获取个股资金流向数据

    包含主力净流入、散户净流入、大单/中单/小单等数据
    """
    try:
        result = await stock_extended_service.get_individual_fund_flow(
            stock_code=stock_code
        )
        if result is None:
            return {
                "stock_code": stock_code,
                "data": None,
                "message": "未找到该股票的资金流向数据",
            }
        return {
            "stock_code": stock_code,
            "data": result.__dict__,
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取资金流向失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fund-flow/rank", summary="获取资金流向排名")
async def get_fund_flow_rank(
    indicator: str = Query("今日", description="时间周期: 今日/3日/5日/10日"),
):
    """
    获取资金流向排名

    - **indicator**: 时间周期，可选：今日、3日、5日、10日
    """
    try:
        result = await stock_extended_service.get_fund_flow_rank(indicator=indicator)
        return {
            "indicator": indicator,
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取资金流向排名失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 财务数据接口 ==========


@router.get("/financial/indicators/{stock_code}", summary="获取财务指标")
async def get_financial_indicators(
    stock_code: str = Path(..., description="股票代码"),
):
    """
    获取个股财务指标

    包含ROE、ROA、毛利率、净利率、资产负债率、流动比率、速动比率、每股收益等
    """
    try:
        result = await stock_extended_service.get_financial_indicators(
            stock_code=stock_code
        )
        return {
            "stock_code": stock_code,
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取财务指标失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/financial/dividend/{stock_code}", summary="获取分红历史")
async def get_dividend_history(
    stock_code: str = Path(..., description="股票代码"),
):
    """
    获取个股分红历史数据

    包含分红年度、分红金额、股权登记日、除权除息日等
    """
    try:
        result = await stock_extended_service.get_dividend_history(
            stock_code=stock_code
        )
        return {
            "stock_code": stock_code,
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取分红历史失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 大宗交易接口 ==========


@router.get("/block-trade/list", summary="获取大宗交易数据")
async def get_block_trade(
    trade_date: Optional[str] = Query(
        None, description="交易日期 YYYYMMDD", regex=r"^\d{8}$"
    ),
):
    """
    获取大宗交易数据

    包含成交价、成交金额、成交量、买方/卖方营业部等
    """
    try:
        result = await stock_extended_service.get_block_trade(trade_date=trade_date)
        return {
            "trade_date": trade_date or datetime.now().strftime("%Y%m%d"),
            "data": [item.__dict__ for item in result],
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取大宗交易失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 股东数据接口 ==========


@router.get("/shareholder/number/{stock_code}", summary="获取股东人数")
async def get_shareholder_number(
    stock_code: str = Path(..., description="股票代码"),
):
    """
    获取个股股东人数变化

    包含股东户数、户均持股数量、户均持股金额等
    """
    try:
        result = await stock_extended_service.get_shareholder_number(
            stock_code=stock_code
        )
        return {
            "stock_code": stock_code,
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"获取股东人数失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
