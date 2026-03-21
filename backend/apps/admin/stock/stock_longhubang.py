#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/21
# @File           : stock_longhubang.py
# @IDE            : PyCharm
# @desc           : 龙虎榜 API 接口

from datetime import datetime, date, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, desc

from apps.admin.auth.utils.current import OpenAuth, Auth
from apps.admin.stock import models
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger

router = APIRouter(prefix="/longhubang", tags=["龙虎榜"])


@router.get("/list", summary="获取龙虎榜列表")
async def get_longhubang_list(
    trade_date: Optional[str] = Query(None, description="交易日期 YYYY-MM-DD"),
    stock_code: Optional[str] = Query(None, description="股票代码"),
    stock_name: Optional[str] = Query(None, description="股票名称（模糊搜索）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """获取龙虎榜数据列表"""
    try:
        query = select(models.StockLonghubang)

        if trade_date:
            td = datetime.strptime(trade_date, "%Y-%m-%d").date()
            query = query.filter(models.StockLonghubang.trade_date == td)
        else:
            subquery = select(func.max(models.StockLonghubang.trade_date))
            result = await auth.db.execute(subquery)
            latest_date = result.scalar()
            if latest_date:
                query = query.filter(models.StockLonghubang.trade_date == latest_date)

        if stock_code:
            query = query.filter(models.StockLonghubang.stock_code == stock_code)

        if stock_name:
            query = query.filter(
                models.StockLonghubang.stock_name.like(f"%{stock_name}%")
            )

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await auth.db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(desc(models.StockLonghubang.net_buy_amount))
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await auth.db.execute(query)
        items = result.scalars().all()

        data_list = []
        for item in items:
            data_list.append(
                {
                    "id": item.id,
                    "trade_date": item.trade_date.strftime("%Y-%m-%d")
                    if item.trade_date
                    else None,
                    "stock_code": item.stock_code,
                    "stock_name": item.stock_name,
                    "full_code": item.full_code,
                    "market": item.market,
                    "close_price": item.close_price,
                    "change_percent": item.change_percent,
                    "turnover_rate": item.turnover_rate,
                    "total_amount": item.total_amount,
                    "net_buy_amount": item.net_buy_amount,
                    "net_buy_ratio": item.net_buy_ratio,
                    "reason": item.reason,
                    "buy_amount_total": item.buy_amount_total,
                    "sell_amount_total": item.sell_amount_total,
                }
            )

        return SuccessResponse(
            {
                "items": data_list,
                "total": total,
                "page": page,
                "page_size": page_size,
            }
        )

    except Exception as e:
        logger.error(f"获取龙虎榜列表失败: {str(e)}")
        return ErrorResponse(f"获取龙虎榜列表失败: {str(e)}")


@router.get("/detail/{lhb_id}", summary="获取龙虎榜详情")
async def get_longhubang_detail(
    lhb_id: int,
    auth: Auth = Depends(OpenAuth()),
):
    """获取龙虎榜详情，包括买卖营业部明细"""
    try:
        query = select(models.StockLonghubang).filter(
            models.StockLonghubang.id == lhb_id
        )
        result = await auth.db.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            return ErrorResponse("龙虎榜数据不存在")

        detail_query = (
            select(models.StockLonghubangDetail)
            .filter(models.StockLonghubangDetail.longhubang_id == lhb_id)
            .order_by(
                models.StockLonghubangDetail.trade_type,
                desc(models.StockLonghubangDetail.net_amount),
            )
        )

        detail_result = await auth.db.execute(detail_query)
        details = detail_result.scalars().all()

        buy_details = []
        sell_details = []
        for detail in details:
            detail_data = {
                "id": detail.id,
                "broker_name": detail.broker_name,
                "broker_type": detail.broker_type,
                "buy_amount": detail.buy_amount,
                "sell_amount": detail.sell_amount,
                "net_amount": detail.net_amount,
            }
            if detail.trade_type == "buy":
                buy_details.append(detail_data)
            else:
                sell_details.append(detail_data)

        return SuccessResponse(
            {
                "id": item.id,
                "trade_date": item.trade_date.strftime("%Y-%m-%d")
                if item.trade_date
                else None,
                "stock_code": item.stock_code,
                "stock_name": item.stock_name,
                "full_code": item.full_code,
                "market": item.market,
                "close_price": item.close_price,
                "change_percent": item.change_percent,
                "turnover_rate": item.turnover_rate,
                "total_amount": item.total_amount,
                "net_buy_amount": item.net_buy_amount,
                "net_buy_ratio": item.net_buy_ratio,
                "reason": item.reason,
                "buy_amount_total": item.buy_amount_total,
                "sell_amount_total": item.sell_amount_total,
                "buy_details": buy_details,
                "sell_details": sell_details,
            }
        )

    except Exception as e:
        logger.error(f"获取龙虎榜详情失败: {str(e)}")
        return ErrorResponse(f"获取龙虎榜详情失败: {str(e)}")


@router.get("/dates", summary="获取龙虎榜日期列表")
async def get_longhubang_dates(
    limit: int = Query(30, ge=1, le=100, description="返回天数"),
    auth: Auth = Depends(OpenAuth()),
):
    """获取龙虎榜可用日期列表"""
    try:
        query = (
            select(models.StockLonghubang.trade_date)
            .distinct()
            .order_by(desc(models.StockLonghubang.trade_date))
            .limit(limit)
        )

        result = await auth.db.execute(query)
        dates = result.scalars().all()

        date_list = [
            d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d) for d in dates
        ]

        return SuccessResponse(date_list)

    except Exception as e:
        logger.error(f"获取龙虎榜日期列表失败: {str(e)}")
        return ErrorResponse(f"获取龙虎榜日期列表失败: {str(e)}")


@router.get("/stock/{stock_code}", summary="获取个股龙虎榜历史")
async def get_stock_longhubang_history(
    stock_code: str,
    days: int = Query(30, ge=1, le=365, description="查询天数"),
    auth: Auth = Depends(OpenAuth()),
):
    """获取指定股票的龙虎榜历史记录"""
    try:
        start_date = date.today() - timedelta(days=days)

        query = (
            select(models.StockLonghubang)
            .filter(
                models.StockLonghubang.stock_code == stock_code,
                models.StockLonghubang.trade_date >= start_date,
            )
            .order_by(desc(models.StockLonghubang.trade_date))
        )

        result = await auth.db.execute(query)
        items = result.scalars().all()

        data_list = []
        for item in items:
            data_list.append(
                {
                    "id": item.id,
                    "trade_date": item.trade_date.strftime("%Y-%m-%d")
                    if item.trade_date
                    else None,
                    "stock_code": item.stock_code,
                    "stock_name": item.stock_name,
                    "close_price": item.close_price,
                    "change_percent": item.change_percent,
                    "turnover_rate": item.turnover_rate,
                    "net_buy_amount": item.net_buy_amount,
                    "net_buy_ratio": item.net_buy_ratio,
                    "reason": item.reason,
                    "buy_amount_total": item.buy_amount_total,
                    "sell_amount_total": item.sell_amount_total,
                }
            )

        return SuccessResponse(data_list)

    except Exception as e:
        logger.error(f"获取个股龙虎榜历史失败: {str(e)}")
        return ErrorResponse(f"获取个股龙虎榜历史失败: {str(e)}")


@router.get("/statistics", summary="获取龙虎榜统计")
async def get_longhubang_statistics(
    trade_date: Optional[str] = Query(None, description="交易日期 YYYY-MM-DD"),
    auth: Auth = Depends(OpenAuth()),
):
    """获取龙虎榜统计数据"""
    try:
        if trade_date:
            td = datetime.strptime(trade_date, "%Y-%m-%d").date()
        else:
            subquery = select(func.max(models.StockLonghubang.trade_date))
            result = await auth.db.execute(subquery)
            td = result.scalar()

        if not td:
            return SuccessResponse(
                {
                    "trade_date": None,
                    "total_count": 0,
                    "up_count": 0,
                    "down_count": 0,
                    "limit_up_count": 0,
                    "limit_down_count": 0,
                    "total_net_buy": 0,
                }
            )

        base_query = select(models.StockLonghubang).filter(
            models.StockLonghubang.trade_date == td
        )
        count_query = select(func.count()).select_from(base_query.subquery())
        total_result = await auth.db.execute(count_query)
        total_count = total_result.scalar() or 0

        up_query = select(func.count()).select_from(
            base_query.filter(models.StockLonghubang.change_percent > 0).subquery()
        )
        up_result = await auth.db.execute(up_query)
        up_count = up_result.scalar() or 0

        down_query = select(func.count()).select_from(
            base_query.filter(models.StockLonghubang.change_percent < 0).subquery()
        )
        down_result = await auth.db.execute(down_query)
        down_count = down_result.scalar() or 0

        limit_up_query = select(func.count()).select_from(
            base_query.filter(models.StockLonghubang.change_percent >= 9.9).subquery()
        )
        limit_up_result = await auth.db.execute(limit_up_query)
        limit_up_count = limit_up_result.scalar() or 0

        limit_down_query = select(func.count()).select_from(
            base_query.filter(models.StockLonghubang.change_percent <= -9.9).subquery()
        )
        limit_down_result = await auth.db.execute(limit_down_query)
        limit_down_count = limit_down_result.scalar() or 0

        sum_query = select(func.sum(models.StockLonghubang.net_buy_amount)).select_from(
            base_query.subquery()
        )
        sum_result = await auth.db.execute(sum_query)
        total_net_buy = sum_result.scalar() or 0

        return SuccessResponse(
            {
                "trade_date": td.strftime("%Y-%m-%d")
                if hasattr(td, "strftime")
                else str(td),
                "total_count": total_count,
                "up_count": up_count,
                "down_count": down_count,
                "limit_up_count": limit_up_count,
                "limit_down_count": limit_down_count,
                "total_net_buy": float(total_net_buy) if total_net_buy else 0,
            }
        )

    except Exception as e:
        logger.error(f"获取龙虎榜统计失败: {str(e)}")
        return ErrorResponse(f"获取龙虎榜统计失败: {str(e)}")


@router.get("/broker/top", summary="获取活跃营业部排行")
async def get_top_brokers(
    trade_date: Optional[str] = Query(None, description="交易日期 YYYY-MM-DD"),
    limit: int = Query(20, ge=1, le=100, description="返回数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """获取龙虎榜活跃营业部排行"""
    try:
        if trade_date:
            td = datetime.strptime(trade_date, "%Y-%m-%d").date()
        else:
            subquery = select(func.max(models.StockLonghubang.trade_date))
            result = await auth.db.execute(subquery)
            td = result.scalar()

        if not td:
            return SuccessResponse([])

        query = (
            select(
                models.StockLonghubangDetail.broker_name,
                models.StockLonghubangDetail.broker_type,
                func.count(models.StockLonghubangDetail.id).label("appear_count"),
                func.sum(models.StockLonghubangDetail.buy_amount).label("total_buy"),
                func.sum(models.StockLonghubangDetail.sell_amount).label("total_sell"),
                func.sum(models.StockLonghubangDetail.net_amount).label("total_net"),
            )
            .filter(models.StockLonghubangDetail.trade_date == td)
            .group_by(
                models.StockLonghubangDetail.broker_name,
                models.StockLonghubangDetail.broker_type,
            )
            .order_by(desc("total_net"))
            .limit(limit)
        )

        result = await auth.db.execute(query)
        rows = result.all()

        data_list = []
        for row in rows:
            data_list.append(
                {
                    "broker_name": row.broker_name,
                    "broker_type": row.broker_type,
                    "appear_count": row.appear_count,
                    "total_buy": float(row.total_buy) if row.total_buy else 0,
                    "total_sell": float(row.total_sell) if row.total_sell else 0,
                    "total_net": float(row.total_net) if row.total_net else 0,
                }
            )

        return SuccessResponse(data_list)

    except Exception as e:
        logger.error(f"获取活跃营业部排行失败: {str(e)}")
        return ErrorResponse(f"获取活跃营业部排行失败: {str(e)}")
