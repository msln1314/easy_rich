#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/21
# @File           : stock_market_dashboard.py
# @IDE            : PyCharm
# @desc           : 大盘座舱数据 API 接口

from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc, func
from apps.admin.auth.utils.current import OpenAuth, Auth
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger
from apps.admin.stock import models
import httpx

router = APIRouter(prefix="/dashboard", tags=["大盘座舱"])

STOCK_SERVICE_URL = "http://localhost:8008/api/v1"


async def call_stock_service(endpoint: str, params: dict = None, timeout: float = 10.0):
    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{STOCK_SERVICE_URL}{endpoint}"
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            logger.warning(f"Stock service timeout: {endpoint}")
            return None
        except Exception as e:
            logger.error(f"Stock service error: {endpoint}, {str(e)}")
            return None


@router.get("/limit-pool", summary="获取涨跌停池数据")
async def get_limit_pool(auth: Auth = Depends(OpenAuth())):
    """获取涨停池和跌停池数据"""
    try:
        zt_data = await call_stock_service("/market-ext/zt-pool")
        dt_data = await call_stock_service("/market-ext/dt-pool")

        zt_pool = []
        if zt_data and isinstance(zt_data, list):
            zt_pool = zt_data[:20]
        elif zt_data and isinstance(zt_data, dict) and zt_data.get("data"):
            zt_pool = zt_data["data"][:20]

        dt_pool = []
        if dt_data and isinstance(dt_data, list):
            dt_pool = dt_data[:20]
        elif dt_data and isinstance(dt_data, dict) and dt_data.get("data"):
            dt_pool = dt_data["data"][:20]

        continuous_stats = {}
        for item in zt_pool:
            days = item.get("continuous_days")
            if days:
                key = f"{int(days)}板"
                continuous_stats[key] = continuous_stats.get(key, 0) + 1

        return SuccessResponse(
            {
                "zt_pool": zt_pool,
                "dt_pool": dt_pool,
                "zt_count": len(zt_pool),
                "dt_count": len(dt_pool),
                "continuous_stats": continuous_stats,
            }
        )

    except Exception as e:
        logger.error(f"获取涨跌停池失败: {str(e)}")
        return ErrorResponse(f"获取涨跌停池失败: {str(e)}")


@router.get("/sector-hot", summary="获取热门板块")
async def get_sector_hot(
    sector_type: str = Query("industry", description="板块类型: industry/concept"),
    limit: int = Query(10, ge=1, le=30, description="返回数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """获取热门板块排行 - 优先从数据库读取"""
    try:
        sectors = []

        if sector_type == "industry":
            query = (
                select(models.StockBoardIndustry)
                .where(models.StockBoardIndustry.is_delete == False)
                .order_by(desc(models.StockBoardIndustry.change_percent))
                .limit(limit)
            )

            result = await auth.db.execute(query)
            items = result.scalars().all()

            for item in items:
                sectors.append(
                    {
                        "board_code": item.board_code,
                        "board_name": item.board_name,
                        "change_percent": item.change_percent,
                        "up_count": item.up_count,
                        "down_count": item.down_count,
                        "leading_stock": item.leading_stock,
                        "leading_stock_change": item.leading_stock_change,
                    }
                )
        else:
            query = (
                select(models.StockBoardConcept)
                .where(models.StockBoardConcept.is_delete == False)
                .order_by(desc(models.StockBoardConcept.change_percent))
                .limit(limit)
            )

            result = await auth.db.execute(query)
            items = result.scalars().all()

            if items:
                for item in items:
                    sectors.append(
                        {
                            "board_code": item.board_code,
                            "board_name": item.board_name,
                            "change_percent": item.change_percent,
                            "up_count": item.up_count,
                            "down_count": item.down_count,
                            "leading_stock": item.leading_stock,
                            "leading_stock_change": item.leading_stock_change,
                        }
                    )
            else:
                data = await call_stock_service("/sector/concept", timeout=20.0)
                if data:
                    if isinstance(data, list):
                        raw_sectors = data
                    elif isinstance(data, dict):
                        raw_sectors = data.get("data", data.get("items", []))
                    else:
                        raw_sectors = []

                    sorted_sectors = sorted(
                        raw_sectors,
                        key=lambda x: x.get("change_percent", 0) or 0,
                        reverse=True,
                    )[:limit]

                    for item in sorted_sectors:
                        sectors.append(
                            {
                                "board_code": item.get("code")
                                or item.get("board_code"),
                                "board_name": item.get("name")
                                or item.get("board_name"),
                                "change_percent": item.get("change_percent"),
                                "up_count": item.get("up_count"),
                                "down_count": item.get("down_count"),
                                "leading_stock": item.get("leading_stock"),
                                "leading_stock_change": item.get(
                                    "leading_stock_change_percent"
                                )
                                or item.get("leading_stock_change"),
                            }
                        )

        return SuccessResponse(
            {
                "sectors": sectors,
                "sector_type": sector_type,
            }
        )

    except Exception as e:
        logger.error(f"获取热门板块失败: {str(e)}")
        return ErrorResponse(f"获取热门板块失败: {str(e)}")


@router.get("/margin-summary", summary="获取融资融券汇总")
async def get_margin_summary(auth: Auth = Depends(OpenAuth())):
    """获取融资融券汇总数据 - 优先从数据库读取"""
    try:
        summary = {}
        rank_list = []

        # 1. 优先从数据库获取汇总数据
        query = (
            select(models.StockMarginSummary)
            .order_by(desc(models.StockMarginSummary.trade_date))
            .limit(1)
        )
        result = await auth.db.execute(query)
        db_summary = result.scalar_one_or_none()

        if db_summary:
            summary = {
                "trade_date": db_summary.trade_date.strftime("%Y%m%d")
                if db_summary.trade_date
                else None,
                "rzye": db_summary.rzye,
                "rzmre": db_summary.rzmre,
                "rzche": db_summary.rzche,
                "rqye": db_summary.rqye,
                "rqmcl": db_summary.rqmcl,
                "rqchl": db_summary.rqchl,
                "total": db_summary.total,
                "data_from": "database",
            }

            # 2. 从数据库获取明细排行
            detail_query = (
                select(models.StockMarginDetail)
                .where(models.StockMarginDetail.trade_date == db_summary.trade_date)
                .order_by(desc(models.StockMarginDetail.rzye))
                .limit(10)
            )
            detail_result = await auth.db.execute(detail_query)
            details = detail_result.scalars().all()

            for idx, item in enumerate(details):
                rank_list.append(
                    {
                        "rank": idx + 1,
                        "stock_code": item.stock_code,
                        "stock_name": item.stock_name,
                        "rzye": item.rzye,
                        "rqye": item.rqye,
                        "data_from": "database",
                    }
                )

        # 3. 数据库无数据时，从 stock_service 获取
        if not summary:
            summary_data = await call_stock_service("/margin/summary", timeout=15.0)
            if summary_data and isinstance(summary_data, dict):
                summary = summary_data.get("data", summary_data)
                summary["data_from"] = "stock_service"

        if not rank_list:
            rank_data = await call_stock_service(
                "/margin/rank", params={"limit": 10}, timeout=15.0
            )
            if rank_data:
                if isinstance(rank_data, list):
                    rank_list = rank_data[:10]
                elif isinstance(rank_data, dict):
                    rank_list = rank_data.get("data", [])[:10]
                for item in rank_list:
                    item["data_from"] = "stock_service"

        return SuccessResponse(
            {
                "summary": summary,
                "rank": rank_list,
            }
        )

    except Exception as e:
        logger.error(f"获取融资融券数据失败: {str(e)}")
        return ErrorResponse(f"获取融资融券数据失败: {str(e)}")


@router.get("/hot-stocks", summary="获取热门股票")
async def get_hot_stocks(
    limit: int = Query(10, ge=1, le=30, description="返回数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """获取热门股票排行"""
    try:
        data = await call_stock_service(
            "/sentiment/stock/hot-rank", params={"limit": limit}, timeout=15.0
        )

        stocks = []
        if data:
            if isinstance(data, list):
                stocks = data
            elif isinstance(data, dict):
                stocks = data.get("data", [])

        return SuccessResponse(
            {
                "stocks": stocks[:limit],
            }
        )

    except Exception as e:
        logger.error(f"获取热门股票失败: {str(e)}")
        return ErrorResponse(f"获取热门股票失败: {str(e)}")


@router.get("/market-sentiment", summary="获取市场情绪指标")
async def get_market_sentiment(auth: Auth = Depends(OpenAuth())):
    """获取市场情绪综合指标"""
    try:
        zt_data = await call_stock_service("/market-ext/zt-pool")
        dt_data = await call_stock_service("/market-ext/dt-pool")

        zt_count = 0
        dt_count = 0
        continuous_stats = {}

        if zt_data:
            zt_list = zt_data if isinstance(zt_data, list) else zt_data.get("data", [])
            zt_count = len(zt_list)
            for item in zt_list:
                days = item.get("continuous_days")
                if days:
                    key = int(days)
                    continuous_stats[key] = continuous_stats.get(key, 0) + 1

        if dt_data:
            dt_list = dt_data if isinstance(dt_data, list) else dt_data.get("data", [])
            dt_count = len(dt_list)

        max_continuous = max(continuous_stats.keys()) if continuous_stats else 0

        zt_dt_ratio = (
            zt_count / (zt_count + dt_count) if (zt_count + dt_count) > 0 else 0.5
        )

        if zt_count > 50 and zt_dt_ratio > 0.7:
            sentiment_score = min(100, 60 + zt_count * 0.5)
            sentiment_level = "极度亢奋"
        elif zt_count > 30 and zt_dt_ratio > 0.6:
            sentiment_score = min(90, 50 + zt_count * 0.4)
            sentiment_level = "情绪高涨"
        elif zt_count > 15 and zt_dt_ratio > 0.5:
            sentiment_score = 50 + zt_count * 0.3
            sentiment_level = "情绪偏暖"
        elif zt_count < 10 or zt_dt_ratio < 0.3:
            sentiment_score = max(20, 40 - dt_count * 0.5)
            sentiment_level = "情绪低迷"
        else:
            sentiment_score = 50
            sentiment_level = "情绪中性"

        return SuccessResponse(
            {
                "zt_count": zt_count,
                "dt_count": dt_count,
                "max_continuous": max_continuous,
                "continuous_stats": continuous_stats,
                "zt_dt_ratio": round(zt_dt_ratio, 2),
                "sentiment_score": round(sentiment_score, 1),
                "sentiment_level": sentiment_level,
            }
        )

    except Exception as e:
        logger.error(f"获取市场情绪失败: {str(e)}")
        return ErrorResponse(f"获取市场情绪失败: {str(e)}")


@router.get("/all-dashboard-data", summary="获取大盘座舱所有数据")
async def get_all_dashboard_data(auth: Auth = Depends(OpenAuth())):
    """一次性获取大盘座舱所需的所有数据"""
    try:
        import asyncio

        results = await asyncio.gather(
            call_stock_service("/market-ext/zt-pool"),
            call_stock_service("/market-ext/dt-pool"),
            call_stock_service("/margin/summary"),
            call_stock_service("/sentiment/stock/hot-rank", params={"limit": 10}),
            return_exceptions=True,
        )

        zt_data, dt_data, margin_data, hot_data = results

        zt_pool = []
        if zt_data and not isinstance(zt_data, Exception):
            zt_pool = zt_data if isinstance(zt_data, list) else zt_data.get("data", [])

        dt_pool = []
        if dt_data and not isinstance(dt_data, Exception):
            dt_pool = dt_data if isinstance(dt_data, list) else dt_data.get("data", [])

        margin_summary = (
            margin_data
            if margin_data and not isinstance(margin_data, Exception)
            else {}
        )

        hot_stocks = []
        if hot_data and not isinstance(hot_data, Exception):
            hot_stocks = (
                hot_data if isinstance(hot_data, list) else hot_data.get("data", [])
            )

        query = (
            select(models.StockBoardIndustry)
            .where(models.StockBoardIndustry.is_delete == False)
            .order_by(desc(models.StockBoardIndustry.change_percent))
            .limit(10)
        )

        sector_result = await auth.db.execute(query)
        sector_items = sector_result.scalars().all()
        sectors = []
        for item in sector_items:
            sectors.append(
                {
                    "board_code": item.board_code,
                    "board_name": item.board_name,
                    "change_percent": item.change_percent,
                    "up_count": item.up_count,
                    "down_count": item.down_count,
                    "leading_stock": item.leading_stock,
                    "leading_stock_change": item.leading_stock_change,
                }
            )

        zt_count = len(zt_pool)
        dt_count = len(dt_pool)
        continuous_stats = {}
        for item in zt_pool:
            days = item.get("continuous_days")
            if days:
                key = int(days)
                continuous_stats[key] = continuous_stats.get(key, 0) + 1

        max_continuous = max(continuous_stats.keys()) if continuous_stats else 0
        zt_dt_ratio = (
            zt_count / (zt_count + dt_count) if (zt_count + dt_count) > 0 else 0.5
        )

        if zt_count > 50 and zt_dt_ratio > 0.7:
            sentiment_score = min(100, 60 + zt_count * 0.5)
            sentiment_level = "极度亢奋"
        elif zt_count > 30 and zt_dt_ratio > 0.6:
            sentiment_score = min(90, 50 + zt_count * 0.4)
            sentiment_level = "情绪高涨"
        elif zt_count > 15 and zt_dt_ratio > 0.5:
            sentiment_score = 50 + zt_count * 0.3
            sentiment_level = "情绪偏暖"
        elif zt_count < 10 or zt_dt_ratio < 0.3:
            sentiment_score = max(20, 40 - dt_count * 0.5)
            sentiment_level = "情绪低迷"
        else:
            sentiment_score = 50
            sentiment_level = "情绪中性"

        return SuccessResponse(
            {
                "limit_pool": {
                    "zt_pool": zt_pool[:20],
                    "dt_pool": dt_pool[:20],
                    "zt_count": zt_count,
                    "dt_count": dt_count,
                    "continuous_stats": continuous_stats,
                },
                "sector_hot": {
                    "sectors": sectors,
                    "sector_type": "industry",
                },
                "margin": {
                    "summary": margin_summary,
                },
                "hot_stocks": hot_stocks[:10],
                "sentiment": {
                    "zt_count": zt_count,
                    "dt_count": dt_count,
                    "max_continuous": max_continuous,
                    "continuous_stats": continuous_stats,
                    "zt_dt_ratio": round(zt_dt_ratio, 2),
                    "sentiment_score": round(sentiment_score, 1),
                    "sentiment_level": sentiment_level,
                },
            }
        )

    except Exception as e:
        logger.error(f"获取大盘座舱数据失败: {str(e)}")
        return ErrorResponse(f"获取大盘座舱数据失败: {str(e)}")
