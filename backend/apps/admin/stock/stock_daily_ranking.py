#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
个股每日排行API接口
支持成交量、换手率、成交额、热度等维度的排行查询和历史数据
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc, func, asc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date, datetime

from db.database import get_async_db
from apps.admin.auth.utils.current import OpenAuth
from apps.admin.stock.models.stock_basic_info import StockBasicInfo
from apps.admin.stock.models.stock_daily_ranking import StockDailyRanking
from apps.admin.stock.models.stock_hot_rank import StockHotRank
from apps.admin.stock.models.stock_hot_rank_detail import StockHotRankDetail
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
from apps.module_task.ranking_service import (
    collect_daily_ranking,
    collect_all_rankings,
    sync_rankings_from_realtime,
)
from utils.response import SuccessResponse, ErrorResponse

router = APIRouter(prefix="/stock/daily-ranking", tags=["每日排行"])


@router.get("", summary="获取每日排行列表")
async def get_daily_ranking(
    params: StockDailyRankingParams = Depends(), auth: OpenAuth = Depends()
) -> SuccessResponse | ErrorResponse:
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
        # 确定查询日期
        query_date = params.data_date or date.today()

        # 构建基础查询
        query = select(StockDailyRanking).filter(
            StockDailyRanking.data_date == query_date,
            StockDailyRanking.ranking_type == params.ranking_type.value,
        )

        # 应用筛选条件
        if params.industry:
            query = query.filter(StockDailyRanking.industry == params.industry)

        if params.market:
            query = query.filter(StockDailyRanking.market == params.market)

        if params.stock_code:
            query = query.filter(StockDailyRanking.stock_code == params.stock_code)

        if params.stock_name:
            query = query.filter(
                StockDailyRanking.stock_name.like(f"%{params.stock_name}%")
            )

        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        from database import async_engine

        async with AsyncSession(async_engine) as session:
            count_result = await session.execute(count_query)
            total = count_result.scalar()

            # 分页和排序
            query = query.order_by(StockDailyRanking.rank)
            query = query.offset((params.page - 1) * params.page_size).limit(
                params.page_size
            )

            result = await session.execute(query)
            rankings = result.scalars().all()

        # 转换为输出模型
        items = [StockDailyRankingOut.model_validate(r).model_dump() for r in rankings]

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
    auth: OpenAuth = Depends(),
) -> SuccessResponse | ErrorResponse:
    """
    获取实时排行列表（从 StockBasicInfo 实时查询）
    """
    try:
        # 构建查询
        query = select(StockBasicInfo).filter(
            StockBasicInfo.status == "L", StockBasicInfo.trade_status == "交易中"
        )

        # 获取排序字段
        field_map = {
            DailyRankingType.VOLUME: StockBasicInfo.volume,
            DailyRankingType.TURNOVER: StockBasicInfo.turnover_rate,
            DailyRankingType.AMOUNT: StockBasicInfo.amount,
            DailyRankingType.CHANGE_PERCENT: StockBasicInfo.change_percent,
        }

        sort_field = field_map.get(ranking_type)
        if not sort_field:
            return ErrorResponse(f"不支持的排行类型: {ranking_type.value}")

        # 应用筛选
        if industry:
            query = query.filter(StockBasicInfo.industry == industry)
        if market:
            query = query.filter(StockBasicInfo.market == market)

        # 排序并限制数量
        query = query.order_by(desc(sort_field)).limit(limit)

        from database import async_engine

        async with AsyncSession(async_engine) as session:
            result = await session.execute(query)
            stocks = result.scalars().all()

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
    params: HotRankingParams = Depends(), auth: OpenAuth = Depends()
) -> SuccessResponse | ErrorResponse:
    """
    获取东方财富个股人气榜热度排行
    """
    try:
        query_date = params.data_date or date.today()

        # 构建查询
        query = select(StockHotRank).filter(StockHotRank.data_date == query_date)

        if params.market:
            query = query.filter(StockHotRank.market == params.market)

        query = query.order_by(StockHotRank.rank)

        from database import async_engine

        async with AsyncSession(async_engine) as session:
            # 获取总数
            count_query = select(func.count()).select_from(query.subquery())
            count_result = await session.execute(count_query)
            total = count_result.scalar()

            # 分页
            query = query.offset((params.page - 1) * params.page_size).limit(
                params.page_size
            )
            result = await session.execute(query)
            hot_stocks = result.scalars().all()

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
                created_at=datetime.now(),
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
    params: RankingTrendParams = Depends(), auth: OpenAuth = Depends()
) -> SuccessResponse | ErrorResponse:
    """
    获取指定股票的排行趋势（历史走势）
    """
    try:
        # 构建查询
        query = select(StockDailyRanking).filter(
            StockDailyRanking.stock_code == params.stock_code,
            StockDailyRanking.ranking_type == params.ranking_type.value,
        )

        if params.start_date:
            query = query.filter(StockDailyRanking.data_date >= params.start_date)
        if params.end_date:
            query = query.filter(StockDailyRanking.data_date <= params.end_date)

        query = query.order_by(StockDailyRanking.data_date)

        from database import async_engine

        async with AsyncSession(async_engine) as session:
            result = await session.execute(query)
            rankings = result.scalars().all()

        # 整理趋势数据
        trend_data = [
            {
                "data_date": r.data_date,
                "rank": r.rank,
                "rank_change": r.rank_change,
                "ranking_value": r.ranking_value,
            }
            for r in rankings
        ]

        # 获取股票名称
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
    params: RankingSummaryParams = Depends(), auth: OpenAuth = Depends()
) -> SuccessResponse | ErrorResponse:
    """
    获取排行榜单汇总信息（当日TOP10）
    """
    try:
        query_date = params.data_date or date.today()

        # 构建查询
        query = (
            select(StockDailyRanking)
            .filter(
                StockDailyRanking.data_date == query_date,
                StockDailyRanking.ranking_type == params.ranking_type.value,
            )
            .order_by(StockDailyRanking.rank)
            .limit(params.top_n)
        )

        from database import async_engine

        async with AsyncSession(async_engine) as session:
            result = await session.execute(query)
            rankings = result.scalars().all()

            # 获取当日上榜总数
            count_query = select(func.count()).filter(
                StockDailyRanking.data_date == query_date,
                StockDailyRanking.ranking_type == params.ranking_type.value,
            )
            count_result = await session.execute(count_query)
            total_count = count_result.scalar()

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
    params: SyncRankingParams = Depends(), auth: OpenAuth = Depends()
) -> SuccessResponse | ErrorResponse:
    """
    手动触发排行数据同步（每日收盘后执行）
    """
    try:
        target_date = params.data_date or date.today()

        async for db in get_async_db():
            if params.ranking_types and len(params.ranking_types) == 1:
                # 单类型同步
                result = await collect_daily_ranking(
                    db, params.ranking_types[0], target_date
                )
            else:
                # 同步所有类型
                result = await sync_rankings_from_realtime(db, target_date)

            if result["is_success"]:
                return SuccessResponse(result)
            else:
                return ErrorResponse(result.get("message", "同步失败"))

    except Exception as e:
        return ErrorResponse(f"同步排行数据失败: {str(e)}")


@router.get("/industries", summary="获取行业列表")
async def get_industries(
    ranking_type: DailyRankingType = Query(..., title="排行类型"),
    auth: OpenAuth = Depends(),
) -> SuccessResponse | ErrorResponse:
    """
    获取指定排行类型关联的行业列表
    """
    try:
        from database import async_engine

        async with AsyncSession(async_engine) as session:
            industries = (
                session.query(StockDailyRanking.industry)
                .filter(
                    StockDailyRanking.ranking_type == ranking_type.value,
                    StockDailyRanking.industry.isnot(None),
                )
                .distinct()
                .all()
            )

            industry_list = sorted([ind[0] for ind in industries if ind[0]])
            return SuccessResponse(industry_list)

    except Exception as e:
        return ErrorResponse(f"获取行业列表失败: {str(e)}")


@router.get("/hot-detail/{stock_code}", summary="获取股票热度详情")
async def get_hot_detail(
    stock_code: str,
    days: int = Query(7, ge=1, le=30, title="查询天数"),
    auth: OpenAuth = Depends(),
) -> SuccessResponse | ErrorResponse:
    """
    获取指定股票的历史热度数据
    """
    try:
        from datetime import timedelta

        start_date = date.today() - timedelta(days=days)

        query = (
            select(StockHotRankDetail)
            .filter(
                StockHotRankDetail.stock_code == stock_code,
                StockHotRankDetail.data_date >= start_date,
            )
            .order_by(StockHotRankDetail.data_date)
        )

        from database import async_engine

        async with AsyncSession(async_engine) as session:
            result = await session.execute(query)
            details = result.scalars().all()

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
