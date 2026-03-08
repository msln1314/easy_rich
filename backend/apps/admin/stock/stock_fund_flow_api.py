#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_fund_flow_api.py
# @IDE            : PyCharm
# @desc           : 资金流向分析API

from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from pydantic import BaseModel
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger
from apps.admin.auth.utils.current import AllUserAuth, Auth
from utils.akshare_enhanced import get_ak_enhanced

router = APIRouter()


class FundFlowItem(BaseModel):
    date: Optional[str] = None
    main_net_inflow: Optional[float] = None
    main_net_inflow_percent: Optional[float] = None
    super_large_net_inflow: Optional[float] = None
    large_net_inflow: Optional[float] = None
    medium_net_inflow: Optional[float] = None
    small_net_inflow: Optional[float] = None
    close_price: Optional[float] = None
    change_pct: Optional[float] = None


@router.get("/fund_flow/individual", summary="获取个股资金流向")
async def get_individual_fund_flow(
    stock: str = Query(..., description="股票代码"),
    market: str = Query("sh", description="市场: sh/sz"),
    auth: Auth = Depends(AllUserAuth())
):
    """获取个股资金流向数据"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_individual_fund_flow(stock, market)
        
        if df is None or df.empty:
            return SuccessResponse([])
        
        result = []
        for _, row in df.iterrows():
            item = FundFlowItem(
                date=str(row.get("日期", "")),
                main_net_inflow=float(row.get("主力净流入-净额", 0)) if row.get("主力净流入-净额") else None,
                main_net_inflow_percent=float(row.get("主力净流入-净占比", 0)) if row.get("主力净流入-净占比") else None,
                super_large_net_inflow=float(row.get("超大单净流入-净额", 0)) if row.get("超大单净流入-净额") else None,
                large_net_inflow=float(row.get("大单净流入-净额", 0)) if row.get("大单净流入-净额") else None,
                medium_net_inflow=float(row.get("中单净流入-净额", 0)) if row.get("中单净流入-净额") else None,
                small_net_inflow=float(row.get("小单净流入-净额", 0)) if row.get("小单净流入-净额") else None,
                close_price=float(row.get("收盘价", 0)) if row.get("收盘价") else None,
                change_pct=float(row.get("涨跌幅", 0)) if row.get("涨跌幅") else None,
            )
            result.append(item)
        
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取个股资金流向失败: {stock}, {e}")
        return ErrorResponse(f"获取资金流向失败: {str(e)}")


@router.get("/fund_flow/market", summary="获取大盘资金流向")
async def get_market_fund_flow(auth: Auth = Depends(AllUserAuth())):
    """获取大盘资金流向数据"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_market_fund_flow()
        
        if df is None or df.empty:
            return SuccessResponse({})
        
        result = df.to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取大盘资金流向失败: {e}")
        return ErrorResponse(f"获取大盘资金流向失败: {str(e)}")


@router.get("/fund_flow/sector", summary="获取板块资金流排行")
async def get_sector_fund_flow(
    sector_type: str = Query("行业资金流", description="板块类型: 行业资金流/概念资金流"),
    auth: Auth = Depends(AllUserAuth())
):
    """获取板块资金流排行"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_sector_fund_flow_rank(sector_type)
        
        if df is None or df.empty:
            return SuccessResponse([])
        
        result = df.head(50).to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取板块资金流排行失败: {e}")
        return ErrorResponse(f"获取板块资金流排行失败: {str(e)}")


@router.get("/fund_flow/north", summary="获取北向资金流向")
async def get_north_fund_flow(auth: Auth = Depends(AllUserAuth())):
    """获取北向资金(沪股通/深股通)流向"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_hk_hsgt_north_flow()
        
        if df is None or df.empty:
            return SuccessResponse({})
        
        result = df.to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取北向资金流向失败: {e}")
        return ErrorResponse(f"获取北向资金流向失败: {str(e)}")


@router.get("/fund_flow/north_holding", summary="获取北向资金持股")
async def get_north_holding(auth: Auth = Depends(AllUserAuth())):
    """获取北向资金持股明细"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_hk_hsgt_north Holding()
        
        if df is None or df.empty:
            return SuccessResponse([])
        
        result = df.head(100).to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取北向资金持股失败: {e}")
        return ErrorResponse(f"获取北向资金持股失败: {str(e)}")


@router.get("/fund_flow/lhb", summary="获取龙虎榜数据")
async def get_lhb_data(
    date: Optional[str] = Query(None, description="日期 YYYYMMDD"),
    auth: Auth = Depends(AllUserAuth())
):
    """获取龙虎榜数据"""
    try:
        ak = get_ak_enhanced()
        df = await ak.get_lhb(date)
        
        if df is None or df.empty:
            return SuccessResponse([])
        
        result = df.to_dict(orient="records")
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取龙虎榜数据失败: {e}")
        return ErrorResponse(f"获取龙虎榜数据失败: {str(e)}")
