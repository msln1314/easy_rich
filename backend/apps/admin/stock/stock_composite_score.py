#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_composite_score.py
# @IDE            : PyCharm
# @desc           : 综合评分系统API

from fastapi import APIRouter, Depends, Query
from typing import Optional, Dict, Any
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger
from apps.admin.auth.utils.current import AllUserAuth, Auth
from apps.admin.stock.services.factor_engine import get_factor_engine
from utils.akshare_enhanced import get_ak_enhanced

router = APIRouter()


@router.get("/composite/score", summary="获取综合评分")
async def get_composite_score(
    stock: str = Query(..., description="股票代码"), auth: Auth = Depends(AllUserAuth())
):
    """获取股票综合评分 (多维度)"""
    try:
        engine = get_factor_engine()
        ak = get_ak_enhanced()

        factor_result = await engine.calculate_all_factors(stock)

        fund_flow_df = await ak.get_individual_fund_flow(stock)
        fund_score = 50
        if fund_flow_df is not None and not fund_flow_df.empty:
            main_net = fund_flow_df.iloc[0].get("主力净流入-净额", 0)
            if main_net and float(main_net) > 50000000:
                fund_score = 90
            elif main_net and float(main_net) > 10000000:
                fund_score = 70
            elif main_net and float(main_net) < -10000000:
                fund_score = 30

        composite = (
            factor_result.get("value_score", 50) * 0.20
            + factor_result.get("growth_score", 50) * 0.20
            + factor_result.get("quality_score", 50) * 0.20
            + factor_result.get("momentum_score", 50) * 0.15
            + fund_score * 0.25
        )

        recommendation = "持有"
        if composite >= 80:
            recommendation = "强烈买入"
        elif composite >= 70:
            recommendation = "买入"
        elif composite >= 55:
            recommendation = "持有"
        elif composite >= 40:
            recommendation = "观望"
        else:
            recommendation = "卖出"

        result = {
            "stock_code": stock,
            "composite_score": round(composite, 2),
            "recommendation": recommendation,
            "value_score": factor_result.get("value_score", 0),
            "growth_score": factor_result.get("growth_score", 0),
            "quality_score": factor_result.get("quality_score", 0),
            "momentum_score": factor_result.get("momentum_score", 0),
            "fund_score": fund_score,
            "factors": factor_result,
        }

        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"获取综合评分失败: {stock}, {e}")
        return ErrorResponse(f"获取综合评分失败: {str(e)}")


@router.get("/composite/batch", summary="批量获取综合评分")
async def batch_composite_score(
    stocks: str = Query(..., description="股票代码列表,逗号分隔"),
    auth: Auth = Depends(AllUserAuth()),
):
    """批量获取股票综合评分"""
    try:
        stock_list = [s.strip() for s in stocks.split(",")]
        engine = get_factor_engine()
        ak = get_ak_enhanced()

        results = []
        for stock in stock_list[:20]:
            try:
                factor_result = await engine.calculate_all_factors(stock)

                fund_flow_df = await ak.get_individual_fund_flow(stock)
                fund_score = 50
                if fund_flow_df is not None and not fund_flow_df.empty:
                    main_net = fund_flow_df.iloc[0].get("主力净流入-净额", 0)
                    if main_net and float(main_net) > 50000000:
                        fund_score = 90
                    elif main_net and float(main_net) > 10000000:
                        fund_score = 70
                    elif main_net and float(main_net) < -10000000:
                        fund_score = 30

                composite = (
                    factor_result.get("value_score", 50) * 0.20
                    + factor_result.get("growth_score", 50) * 0.20
                    + factor_result.get("quality_score", 50) * 0.20
                    + factor_result.get("momentum_score", 50) * 0.15
                    + fund_score * 0.25
                )

                recommendation = "持有"
                if composite >= 80:
                    recommendation = "强烈买入"
                elif composite >= 70:
                    recommendation = "买入"
                elif composite >= 55:
                    recommendation = "持有"
                elif composite >= 40:
                    recommendation = "观望"
                else:
                    recommendation = "卖出"

                results.append(
                    {
                        "stock_code": stock,
                        "composite_score": round(composite, 2),
                        "recommendation": recommendation,
                    }
                )
            except Exception as e:
                logger.error(f"计算评分失败: {stock}, {e}")

        sorted_results = sorted(
            results, key=lambda x: x["composite_score"], reverse=True
        )

        return SuccessResponse(sorted_results)
    except Exception as e:
        logger.error(f"批量获取综合评分失败: {e}")
        return ErrorResponse(f"批量获取综合评分失败: {str(e)}")
