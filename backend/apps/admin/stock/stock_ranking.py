#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/1
# @File           : stock_ranking.py
# @IDE            : PyCharm
# @desc           : 个股排行 API

from fastapi import APIRouter, Depends
from sqlalchemy import desc, asc, select, func
from typing import Optional

from apps.admin.stock import crud
from apps.admin.stock.models.stock_basic_info import StockBasicInfo
from apps.admin.stock.params.stock_ranking import StockRankingParams
from apps.admin.stock.schemas.stock_ranking import StockRankingOut, StockRankingListOut
from utils.response import SuccessResponse, ErrorResponse
from apps.admin.auth.utils.current import OpenAuth, Auth

router = APIRouter(prefix="/stock/ranking", tags=["个股排行"])


@router.get("", summary="获取个股排行列表")
async def get_stock_ranking(
    params: StockRankingParams = Depends(),
    auth: Auth = Depends(OpenAuth())
):
    """
    获取个股排行列表

    - **ranking_type**: 排行类型 (turnover/amount/volume_ratio/change_percent/market_cap/amplitude)
    - **order**: 排序方向 (desc/asc)
    - **industry**: 行业筛选
    - **market**: 市场筛选
    - **stock_code**: 股票代码
    - **stock_name**: 股票名称（支持模糊搜索）
    """
    try:
        dal = crud.StockBaseInfoDal(auth.db)

        # 构建查询
        query = select(StockBasicInfo).filter(
            StockBasicInfo.status == "L",
            StockBasicInfo.trade_status == "交易中"
        )

        # 应用筛选条件
        if params.industry:
            query = query.filter(StockBasicInfo.industry == params.industry)

        if params.market:
            query = query.filter(StockBasicInfo.market == params.market)

        if params.stock_code:
            query = query.filter(StockBasicInfo.stock_code == params.stock_code)

        if params.stock_name:
            if isinstance(params.stock_name, tuple) and params.stock_name[0] == "like":
                query = query.filter(StockBasicInfo.stock_name.like(f"%{params.stock_name[1]}%"))

        # 获取排序字段
        sort_field = params.get_sort_field()

        if sort_field:
            if params.order.value == "desc":
                query = query.order_by(sort_field.is_(None), desc(sort_field))
            else:
                query = query.order_by(sort_field.is_(None), asc(sort_field))

        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await dal.execute_query(count_query)
        total = total_result.scalar()

        # 分页查询
        query = query.offset(params.offset).limit(params.limit)
        results = await dal.get_datas(query=query)

        # 计算排名
        start_rank = params.offset + 1
        items = []
        for idx, stock in enumerate(results):
            stock_dict = {
                'id': stock.id,
                'stock_code': stock.stock_code,
                'stock_name': stock.stock_name,
                'industry': stock.industry,
                'board': stock.board,
                'market': stock.market,
                'current_price': stock.current_price,
                'change_percent': stock.change_percent,
                'change_amount': stock.change_amount,
                'open_price': stock.open_price,
                'high_price': stock.high_price,
                'low_price': stock.low_price,
                'close_price': stock.close_price,
                'volume': stock.volume,
                'amount': stock.amount,
                'turnover_rate': stock.turnover_rate,
                'volume_ratio': stock.volume_ratio,
                'total_market_cap': stock.total_market_cap,
                'circulating_market_cap': stock.circulating_market_cap,
                'pe_ratio': stock.pe_ratio,
                'pb_ratio': stock.pb_ratio,
                'amplitude': stock.amplitude,
                'change_speed': stock.change_speed,
                'change_5min': stock.change_5min,
                'change_60day': stock.change_60day,
                'change_ytd': stock.change_ytd,
                'created_at': stock.created_at,
                'updated_at': stock.updated_at,
                'rank': start_rank + idx,
            }
            items.append(StockRankingOut(**stock_dict))

        # 构造返回数据
        result = StockRankingListOut(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            ranking_type=params.ranking_type.value,
            order=params.order.value
        )

        return SuccessResponse(result)

    except Exception as e:
        return ErrorResponse(f"获取排行数据失败: {str(e)}")


@router.get("/industries", summary="获取行业列表")
async def get_industries(auth: Auth = Depends(OpenAuth())):
    """获取所有行业列表，用于筛选"""
    try:
        dal = crud.StockBaseInfoDal(auth.db)

        query = select(StockBasicInfo.industry).filter(
            StockBasicInfo.industry.isnot(None),
            StockBasicInfo.status == "L"
        ).distinct()

        result = await dal.execute_query(query)
        industries = result.scalars().all()
        industry_list = sorted([ind for ind in industries if ind])

        return SuccessResponse(industry_list)
    except Exception as e:
        return ErrorResponse(f"获取行业列表失败: {str(e)}")


@router.get("/markets", summary="获取市场类型列表")
async def get_markets(auth: Auth = Depends(OpenAuth())):
    """获取所有市场类型列表，用于筛选"""
    try:
        dal = crud.StockBaseInfoDal(auth.db)

        query = select(StockBasicInfo.market).filter(
            StockBasicInfo.market.isnot(None),
            StockBasicInfo.status == "L"
        ).distinct()

        result = await dal.execute_query(query)
        markets = result.scalars().all()
        market_list = [mkt for mkt in markets if mkt]

        return SuccessResponse(market_list)
    except Exception as e:
        return ErrorResponse(f"获取市场类型列表失败: {str(e)}")


@router.post("/sync", summary="同步实时行情数据")
async def sync_realtime_data(auth: Auth = Depends(OpenAuth())):
    """
    同步实时行情数据

    从 akshare 获取最新行情数据并更新到数据库
    """
    try:
        from apps.module_task.task_service import sync_stock_realtime_to_basic

        result = await sync_stock_realtime_to_basic(auth.db)
        return SuccessResponse(result)
    except Exception as e:
        return ErrorResponse(f"同步失败: {str(e)}")