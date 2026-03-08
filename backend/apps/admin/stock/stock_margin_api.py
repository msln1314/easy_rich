#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_margin_api.py
# @IDE            : PyCharm
# @desc           : 融资融券API

from fastapi import APIRouter, Depends, Query
from typing import Optional
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger
from apps.admin.auth.utils.current import AllUserAuth, Auth
from utils.akshare_enhanced import get_ak_enhanced

router = APIRouter()


@router.get("/margin/detail", summary="获取个股融资融券详情")
async def get_margin_detail(
    stock: str = Query(..., description="股票代码"),
    symbol: str = Query("融资融券", description="类型: 融资融券/融券"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取个股融资融券明细"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_margin_detail(stock, symbol)

        if df is None or df.empty:
            return SuccessResponse([])

        result = df.to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取融资融券详情失败: {stock}, {e}")
        return ErrorResponse(f"获取融资融券详情失败: {str(e)}")


@router.get("/margin/market", summary="获取市场融资融券汇总")
async def get_margin_market(auth: Auth = Depends(AllUserAuth())):
    """获取市场融资融券汇总数据"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_margin_sse()

        if df is None or df.empty:
            return SuccessResponse({})

        result = df.to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取市场融资融券汇总失败: {e}")
        return ErrorResponse(f"获取市场融资融券汇总失败: {str(e)}")
