#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
个股每日排行API接口
支持成交量、换手率、成交额、热度等维度的排行查询和历史数据
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from typing import Optional
from datetime import date, timedelta

from apps.admin.auth.utils.current import OpenAuth, Auth
from apps.admin.stock.params.stock_daily_ranking import (
    DailyRankingType,
    StockDailyRankingParams,
    RankingTrendParams,
    HotRankingParams,
    SyncRankingParams,
    RankingSummaryParams,
)
from apps.admin.stock.schemas.stock_daily_ranking import (
    StockDailyRankingOut,
    StockDailyRankingListOut,
    StockRankingTrendOut,
    StockRankingSummaryOut,
    HotRankingOut,
)
from apps.admin.stock import crud, models
from apps.module_task.ranking_service import (
    collect_daily_ranking,
    sync_rankings_from_realtime,
)
from utils.response import SuccessResponse, ErrorResponse

router = APIRouter(prefix="/daily-ranking", tags=["每日排行"])


@router.get("", summary="获取每日排行列表")
async def get_daily_ranking(
    params: StockDailyRankingParams = Depends(), auth: Auth = Depends(OpenAuth())
):
    """
    获取每日排行列表

    支持按以下维度查询：
    - 成交量 (volume)
    - 换手率 (turnover)
    - 成交额 (amount)
    - 涨跌幅 (change_percent)
    - 热度 (hot)
    """
    try:
        query_date = params.data_date or date.today()

        dal = crud.StockDailyRankingDal(auth.db)

        # 使用 CRUD 获取数据
        rankings, total = await dal.get_ranking_by_date_and_type(
            data_date=query_date,
            ranking_type=params.ranking_type.value,
            industry=params.industry,
            market=params.market,
            stock_code=params.stock_code,
            stock_name=params.stock_name[1] if params.stock_name else None,
            page=params.page,
            page_size=params.page_size,
        )

        items = [
            StockDailyRankingOut.model_validate(r, from_attributes=True).model_dump()
            for r in rankings
        ]

        result = StockDailyRankingListOut(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            ranking_type=params.ranking_type.value,
            data_date=query_date,
        )

        return SuccessResponse(result)

    except Exception as e:
        return ErrorResponse(f"获取排行数据失败: {str(e)}")


@router.get("/realtime", summary="获取实时排行列表")
async def get_realtime_ranking(
    ranking_type: DailyRankingType = Query(DailyRankingType.TURNOVER, title="排行类型"),
    industry: Optional[str] = Query(None, title="所属行业"),
    market: Optional[str] = Query(None, title="市场类型"),
    limit: int = Query(100, ge=1, le=500, title="返回数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取实时排行列表（从 StockBasicInfo 实时查询）
    """
    try:
        dal = crud.StockBaseInfoDal(auth.db)

        # 获取排序字段名称
        field_name_map = {
            DailyRankingType.VOLUME: "volume",
            DailyRankingType.TURNOVER: "turnover_rate",
            DailyRankingType.AMOUNT: "amount",
            DailyRankingType.CHANGE_PERCENT: "change_percent",
        }

        order_field = field_name_map.get(ranking_type)
        if not order_field:
            return ErrorResponse(f"不支持的排行类型: {ranking_type.value}")

        # 使用 kwargs 传递简单查询条件
        query_params = {
            "status": "L",
            "trade_status": "交易中",
        }
        if industry:
            query_params["industry"] = industry
        if market:
            query_params["market"] = market

        # 使用 DalBase 的 get_datas 方法
        stocks = await dal.get_datas(
            limit=limit,
            v_order="desc",
            v_order_field=order_field,
            v_return_objs=True,
            **query_params,
        )

        items = []
        for idx, stock in enumerate(stocks):
            stock_dict = {
                "rank": idx + 1,
                "stock_code": stock.stock_code,
                "stock_name": stock.stock_name,
                "industry": stock.industry,
                "market": stock.market,
                "current_price": stock.current_price,
                "change_percent": stock.change_percent,
                "volume": stock.volume,
                "amount": stock.amount,
                "turnover_rate": stock.turnover_rate,
            }
            items.append(StockDailyRankingOut(**stock_dict))

        return SuccessResponse(items)

    except Exception as e:
        return ErrorResponse(f"获取实时排行失败: {str(e)}")


@router.get("/hot", summary="获取热度排行")
async def get_hot_ranking(
    params: HotRankingParams = Depends(), auth: Auth = Depends(OpenAuth())
):
    """
    获取东方财富个股人气榜热度排行
    """
    try:
        query_date = params.data_date or date.today()
        dal = crud.StockHotRankDal(auth.db)

        # 使用 CRUD 获取热度排行
        hot_stocks, total = await dal.get_hot_rank_by_date(
            data_date=query_date,
            market=params.market,
            page=params.page,
            page_size=params.page_size,
        )

        items = []
        for stock in hot_stocks:
            hot_out = HotRankingOut(
                id=stock.id,
                stock_code=stock.stock_code,
                stock_name=stock.stock_name,
                full_code=stock.full_code,
                rank=stock.rank,
                rank_change=stock.rank_change,
                current_price=stock.current_price,
                change_percent=stock.change_percent,
                data_date=stock.data_date,
                data_time=stock.data_time,
                created_at=stock.created_at,
            )
            items.append(hot_out.model_dump())

        result = StockDailyRankingListOut(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            ranking_type="hot",
            data_date=query_date,
        )

        return SuccessResponse(result)

    except Exception as e:
        return ErrorResponse(f"获取热度排行失败: {str(e)}")


@router.get("/trend", summary="获取排行趋势")
async def get_ranking_trend(
    params: RankingTrendParams = Depends(), auth: Auth = Depends(OpenAuth())
):
    """
    获取指定股票的排行趋势（历史走势）
    """
    try:
        dal = crud.StockDailyRankingDal(auth.db)

        # 使用 CRUD 获取排行趋势
        rankings = await dal.get_ranking_by_stock(
            stock_code=params.stock_code,
            ranking_type=params.ranking_type.value,
            start_date=params.start_date,
            end_date=params.end_date,
        )

        trend_data = [
            {
                "data_date": r.data_date,
                "rank": r.rank,
                "rank_change": r.rank_change,
                "ranking_value": r.ranking_value,
            }
            for r in rankings
        ]

        stock_name = rankings[0].stock_name if rankings else None

        result = StockRankingTrendOut(
            stock_code=params.stock_code,
            stock_name=stock_name,
            ranking_type=params.ranking_type.value,
            trend_data=trend_data,
        )

        return SuccessResponse(result)

    except Exception as e:
        return ErrorResponse(f"获取排行趋势失败: {str(e)}")


@router.get("/summary", summary="获取排行榜单汇总")
async def get_ranking_summary(
    params: RankingSummaryParams = Depends(), auth: Auth = Depends(OpenAuth())
):
    """
    获取排行榜单汇总信息（当日TOP10）
    """
    try:
        query_date = params.data_date or date.today()
        dal = crud.StockDailyRankingDal(auth.db)

        # 使用 CRUD 获取排行汇总
        rankings, total_count = await dal.get_ranking_summary(
            data_date=query_date,
            ranking_type=params.ranking_type.value,
            top_n=params.top_n,
        )

        top_stocks = [
            {
                "rank": r.rank,
                "stock_code": r.stock_code,
                "stock_name": r.stock_name,
                "ranking_value": r.ranking_value,
                "ranking_value_unit": r.ranking_value_unit,
                "change_percent": r.change_percent,
                "current_price": r.current_price,
            }
            for r in rankings
        ]

        result = StockRankingSummaryOut(
            ranking_type=params.ranking_type.value,
            data_date=query_date,
            total_count=total_count,
            top_stocks=top_stocks,
        )

        return SuccessResponse(result)

    except Exception as e:
        return ErrorResponse(f"获取排行榜单汇总失败: {str(e)}")


@router.post("/sync", summary="同步每日排行数据")
async def sync_daily_ranking(
    params: SyncRankingParams = Depends(), auth: Auth = Depends(OpenAuth())
):
    """
    手动触发排行数据同步（每日收盘后执行）
    """
    try:
        target_date = params.data_date or date.today()
        db = auth.db

        if params.ranking_types and len(params.ranking_types) == 1:
            result = await collect_daily_ranking(
                db, params.ranking_types[0], target_date
            )
        else:
            result = await sync_rankings_from_realtime(db, target_date)

        if result["is_success"]:
            return SuccessResponse(result)
        else:
            return ErrorResponse(result.get("message", "同步失败"))

    except Exception as e:
        return ErrorResponse(f"同步排行数据失败: {str(e)}")


@router.get("/industries", summary="获取行业列表")
async def get_industries(
    ranking_type: DailyRankingType = Query(DailyRankingType.TURNOVER, title="排行类型"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取指定排行类型关联的行业列表（从股票基本信息表获取）
    """
    try:
        dal = crud.StockBaseInfoDal(auth.db)

        # 从 StockBasicInfo 表获取行业列表（distinct 查询）
        query = (
            select(models.StockBasicInfo.industry)
            .where(
                models.StockBasicInfo.status == "L",
                models.StockBasicInfo.trade_status == "交易中",
                models.StockBasicInfo.industry.isnot(None),
            )
            .distinct()
        )
        result = await dal.execute_query(query)
        industries = sorted([ind for ind in result.scalars().all() if ind])

        return SuccessResponse(industries)

    except Exception as e:
        return ErrorResponse(f"获取行业列表失败: {str(e)}")


@router.get("/hot-detail/{stock_code}", summary="获取股票热度详情")
async def get_hot_detail(
    stock_code: str,
    days: int = Query(7, ge=1, le=30, title="查询天数"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取指定股票的历史热度数据
    """
    try:
        start_date = date.today() - timedelta(days=days)
        dal = crud.StockHotRankDetailDal(auth.db)

        # 使用 CRUD 获取热度详情
        details = await dal.get_details_by_stock(
            stock_code=stock_code,
            start_date=start_date,
        )

        trend_data = [
            {
                "data_date": d.data_date,
                "rank": d.rank,
                "rank_change": d.rank_change,
                "hot_value": d.hot_value,
                "view_count": d.view_count,
                "comment_count": d.comment_count,
                "sentiment_score": d.sentiment_score,
            }
            for d in details
        ]

        return SuccessResponse(
            {
                "stock_code": stock_code,
                "stock_name": details[0].stock_name if details else None,
                "trend_data": trend_data,
            }
        )

    except Exception as e:
        return ErrorResponse(f"获取热度详情失败: {str(e)}")