# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : macro_routes.py
# @IDE            : PyCharm
# @desc           : 宏观经济API路由

from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.services.macro_service import macro_service
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/gdp", summary="获取GDP数据")
async def get_gdp():
    """获取中国GDP季度数据，包括一二三产业增加值"""
    try:
        result = await macro_service.get_gdp()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cpi", summary="获取CPI数据")
async def get_cpi():
    """获取消费者价格指数(CPI)数据"""
    try:
        result = await macro_service.get_cpi()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cpi/monthly", summary="获取月度CPI数据")
async def get_cpi_monthly():
    """获取月度消费者价格指数详细数据"""
    try:
        result = await macro_service.get_cpi_monthly()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ppi", summary="获取PPI数据")
async def get_ppi():
    """获取生产者价格指数(PPI)数据"""
    try:
        result = await macro_service.get_ppi()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/money-supply", summary="获取货币供应量")
async def get_money_supply():
    """获取M0/M1/M2货币供应量数据"""
    try:
        result = await macro_service.get_money_supply()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/social-financing", summary="获取社会融资规模")
async def get_social_financing():
    """获取社会融资规模增量数据"""
    try:
        result = await macro_service.get_social_financing()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pmi", summary="获取PMI数据")
async def get_pmi():
    """获取采购经理指数(PMI)数据，包括制造业和非制造业"""
    try:
        result = await macro_service.get_pmi()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/interest-rate", summary="获取利率数据")
async def get_interest_rate():
    """获取当前利率数据，包括Shibor和LPR"""
    try:
        result = await macro_service.get_interest_rate()
        return {"data": result, "update_time": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lpr-history", summary="获取LPR历史")
async def get_lpr_history():
    """获取贷款市场报价利率(LPR)历史数据"""
    try:
        result = await macro_service.get_lpr_history()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exchange-rate", summary="获取汇率数据")
async def get_exchange_rate():
    """获取人民币汇率数据"""
    try:
        result = await macro_service.get_exchange_rate()
        return {"data": result, "update_time": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fx-reserves", summary="获取外汇储备")
async def get_fx_reserves():
    """获取外汇储备和黄金储备数据"""
    try:
        result = await macro_service.get_fx_reserves()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trade", summary="获取贸易数据")
async def get_trade_data():
    """获取进出口贸易数据"""
    try:
        result = await macro_service.get_trade_data()
        return {
            "data": result,
            "count": len(result),
            "update_time": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/overview", summary="获取宏观经济概览")
async def get_macro_overview():
    """获取宏观经济综合概览，包括GDP、CPI、PMI等关键指标"""
    try:
        result = await macro_service.get_macro_overview()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
