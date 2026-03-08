#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_institution_api.py
# @IDE            : PyCharm
# @desc           : 机构持仓与券商研报API

from fastapi import APIRouter, Depends, Query
from typing import Optional
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger
from apps.admin.auth.utils.current import AllUserAuth, Auth
from utils.akshare_enhanced import get_ak_enhanced

router = APIRouter()


@router.get("/institution/holding", summary="获取机构持仓数据")
async def get_institution_holding(
    stock: str = Query(..., description="股票代码"), auth: Auth = Depends(AllUserAuth())
):
    """获取机构持仓数据"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_institution_holding(stock)

        if df is None or df.empty:
            return SuccessResponse([])

        result = df.to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取机构持仓失败: {stock}, {e}")
        return ErrorResponse(f"获取机构持仓失败: {str(e)}")


@router.get("/research/report", summary="获取券商研报")
async def get_research_report(
    symbol: str = Query("推荐", description="研报类型: 推荐/增持/中性等"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取券商研报数据"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_research_report(symbol)

        if df is None or df.empty:
            return SuccessResponse([])

        result = df.head(50).to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取券商研报失败: {e}")
        return ErrorResponse(f"获取券商研报失败: {str(e)}")
