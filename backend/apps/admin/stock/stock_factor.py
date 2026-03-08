#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_factor.py
# @IDE            : PyCharm
# @desc           : 多因子选股API

from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from pydantic import BaseModel
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger
from apps.admin.auth.utils.current import AllUserAuth, Auth
from apps.admin.stock.services.factor_engine import get_factor_engine

router = APIRouter()


class FactorResult(BaseModel):
    stock_code: str
    stock_name: Optional[str] = None
    pe: Optional[float] = None
    pb: Optional[float] = None
    roe: Optional[float] = None
    revenue_growth: Optional[float] = None
    change_20d: Optional[float] = None
    value_score: float = 0
    growth_score: float = 0
    quality_score: float = 0
    momentum_score: float = 0
    composite_score: float = 0


@router.get("/factor/calculate", summary="计算单只股票因子")
async def calculate_factor(
    stock: str = Query(..., description="股票代码"), auth: Auth = Depends(AllUserAuth())
):
    """计算单只股票的多因子得分"""
    try:
        engine = get_factor_engine()
        result = await engine.calculate_all_factors(stock)
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"计算因子失败: {stock}, {e}")
        return ErrorResponse(f"计算因子失败: {str(e)}")


@router.post("/factor/batch", summary="批量计算股票因子")
async def batch_calculate_factors(
    stocks: List[str], auth: Auth = Depends(AllUserAuth())
):
    """批量计算多只股票的多因子得分"""
    try:
        engine = get_factor_engine()
        results = await engine.batch_calculate(stocks)
        return SuccessResponse(results)
    except Exception as e:
        logger.error(f"批量计算因子失败: {e}")
        return ErrorResponse(f"批量计算因子失败: {str(e)}")


@router.get("/factor/ranking", summary="多因子选股排行")
async def factor_ranking(
    stocks: str = Query(..., description="股票代码列表,逗号分隔"),
    auth: Auth = Depends(AllUserAuth()),
):
    """根据多因子得分对股票进行排行"""
    try:
        stock_list = [s.strip() for s in stocks.split(",")]
        engine = get_factor_engine()
        results = await engine.batch_calculate(stock_list)

        sorted_results = sorted(
            results, key=lambda x: x.get("composite_score", 0), reverse=True
        )

        for i, item in enumerate(sorted_results):
            item["rank"] = i + 1

        return SuccessResponse(sorted_results)
    except Exception as e:
        logger.error(f"多因子排行失败: {e}")
        return ErrorResponse(f"多因子排行失败: {str(e)}")
