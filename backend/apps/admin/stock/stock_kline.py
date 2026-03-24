#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
股票日K线API接口
支持K线数据查询和手动同步
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc, and_
from typing import Optional
from datetime import date, timedelta

from apps.admin.auth.utils.current import OpenAuth, Auth
from apps.admin.stock.models.stock_daily import StockDaily
from utils.response import SuccessResponse, ErrorResponse
from apps.module_task.scheduler import main_kline_sync

router = APIRouter(prefix="/stock/kline", tags=["日K线"])


@router.get("/{stock_code}", summary="获取股票K线数据")
async def get_kline_data(
    stock_code: str,
    start_date: Optional[date] = Query(None, title="开始日期"),
    end_date: Optional[date] = Query(None, title="结束日期"),
    limit: int = Query(100, ge=1, le=500, title="返回数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取指定股票的日K线数据
    """
    try:
        db = auth.db

        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=limit * 2)

        query = (
            select(StockDaily)
            .where(
                and_(
                    StockDaily.stock_code == stock_code,
                    StockDaily.trade_date >= start_date,
                    StockDaily.trade_date <= end_date,
                )
            )
            .order_by(desc(StockDaily.trade_date))
            .limit(limit)
        )

        result = await db.execute(query)
        klines = result.scalars().all()

        items = [
            {
                "trade_date": k.trade_date,
                "open_price": k.open_price,
                "high_price": k.high_price,
                "low_price": k.low_price,
                "close_price": k.close_price,
                "volume": k.volume,
                "amount": k.amount,
                "amplitude": k.amplitude,
                "change_percent": k.change_percent,
                "change_amount": k.change_amount,
                "turnover_rate": k.turnover_rate,
            }
            for k in klines
        ]

        return SuccessResponse(
            {
                "stock_code": stock_code,
                "stock_name": klines[0].stock_name if klines else None,
                "total": len(items),
                "items": items,
            }
        )

    except Exception as e:
        return ErrorResponse(f"获取K线数据失败: {str(e)}")


@router.post("/sync", summary="同步K线数据")
async def sync_kline_data(
    stock_code: Optional[str] = Query(None, title="股票代码（不传则同步全部）"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    手动触发K线数据同步

    - 不传 stock_code：同步全部股票
    - 传入 stock_code：只同步指定股票
    """
    try:
        await main_kline_sync(stock_code)

        return SuccessResponse(
            {
                "is_success": True,
                "message": f"K线数据同步任务已启动",
                "stock_code": stock_code or "全部股票",
            }
        )

    except Exception as e:
        return ErrorResponse(f"同步K线数据失败: {str(e)}")


@router.get("/status/{stock_code}", summary="获取K线同步状态")
async def get_kline_status(
    stock_code: str,
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取指定股票的K线同步状态
    """
    try:
        db = auth.db

        # 查询最后一条记录
        query = (
            select(StockDaily)
            .where(StockDaily.stock_code == stock_code)
            .order_by(desc(StockDaily.trade_date))
            .limit(1)
        )
        result = await db.execute(query)
        last_record = result.scalar_one_or_none()

        # 查询总记录数
        count_query = select(StockDaily).where(StockDaily.stock_code == stock_code)
        count_result = await db.execute(count_query)
        total_count = len(count_result.scalars().all())

        if last_record:
            return SuccessResponse(
                {
                    "stock_code": stock_code,
                    "stock_name": last_record.stock_name,
                    "last_trade_date": last_record.trade_date,
                    "total_records": total_count,
                    "data_source": last_record.data_source,
                }
            )
        else:
            return SuccessResponse(
                {
                    "stock_code": stock_code,
                    "stock_name": None,
                    "last_trade_date": None,
                    "total_records": 0,
                    "data_source": None,
                    "message": "该股票暂无K线数据",
                }
            )

    except Exception as e:
        return ErrorResponse(f"获取K线状态失败: {str(e)}")
