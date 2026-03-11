#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/10
# @File           : stock_index.py
# @IDE            : PyCharm
# @desc           : 大盘指数 API 接口

from datetime import datetime, date, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select

from apps.admin.auth.utils.current import OpenAuth, Auth
from apps.admin.stock import crud
from apps.admin.stock import models, schemas
from apps.admin.stock.services.stock_service import (
    StockIndexService,
    MarketSummaryService,
    StockRankingService,
)
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger

router = APIRouter(prefix="/stock/index", tags=["大盘指数"])


@router.get("/quote", summary="获取指数实时行情")
async def get_index_quote(auth: Auth = Depends(OpenAuth())):
    """
    获取主要指数实时行情
    上证指数、深证成指、创业板指、科创50

    流程：
    1. 调用 StockIndexService 从 akshare 获取最新行情
    2. 存入 stock_index 表
    3. 返回最新数据
    """
    try:
        # 1. 从 akshare 获取最新行情
        index_items = StockIndexService.get_index_quote()

        if not index_items:
            return ErrorResponse("获取指数行情失败，请稍后重试")

        # 2. 存入数据库
        dal = crud.StockIndexDal(auth.db)
        today = date.today()
        now = datetime.now()

        for item in index_items:
            # 构造数据
            data = {
                "index_code": item["index_code"],
                "index_name": item["index_name"],
                "close_price": item.get("current_price"),
                "change_percent": item.get("change_percent"),
                "change_amount": item.get("change_amount"),
                "volume": item.get("volume"),
                "amount": item.get("amount"),
                "data_date": today,
                "data_time": now,
                "data_source": "akshare",
            }

            # 查询是否存在当日数据
            existing = await dal.get_data(
                select(models.StockIndex).filter(
                    models.StockIndex.index_code == item["index_code"],
                    models.StockIndex.data_date == today,
                ),
                v_return_none=True
            )

            if existing:
                # 更新
                for key, value in data.items():
                    if key not in ["index_code", "data_date"]:
                        setattr(existing, key, value)
                await dal.flush(existing)
            else:
                # 新增
                await dal.create_data(data=data, v_return_obj=False)

        # 3. 返回最新数据
        items = [
            schemas.StockIndexQuoteOut(
                index_code=item["index_code"],
                index_name=item["index_name"],
                close_price=item.get("current_price"),
                change_percent=item.get("change_percent"),
                change_amount=item.get("change_amount"),
                volume=item.get("volume"),
                amount=item.get("amount"),
            )
            for item in index_items
        ]

        return SuccessResponse(
            schemas.IndexQuoteResponse(items=items, update_time=now)
        )

    except Exception as e:
        logger.error(f"获取指数行情失败: {str(e)}")
        return ErrorResponse(f"获取指数行情失败: {str(e)}")


@router.get("/history", summary="获取指数历史走势")
async def get_index_history(
    index_code: str = Query(..., description="指数代码，如 000001.SH"),
    start_date: Optional[str] = Query(None, description="开始日期 YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYYMMDD"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取指数历史K线数据

    流程：
    1. 优先从数据库读取
    2. 如果数据库没有数据，从 akshare 获取并存储
    """
    try:
        dal = crud.StockIndexDal(auth.db)

        # 解析日期
        if not end_date:
            end_dt = datetime.now().date()
        else:
            end_dt = datetime.strptime(end_date, "%Y%m%d").date()

        if not start_date:
            start_dt = (datetime.now() - timedelta(days=300)).date()
        else:
            start_dt = datetime.strptime(start_date, "%Y%m%d").date()

        # 从数据库获取历史数据
        history_data = await dal.get_history_by_code(
            index_code=index_code,
            start_date=start_dt,
            end_date=end_dt,
        )

        # 如果数据库有数据，直接返回
        if history_data:
            items = [
                {
                    "date": h.data_date.strftime("%Y-%m-%d") if hasattr(h.data_date, 'strftime') else str(h.data_date),
                    "open": h.open_price,
                    "high": h.high_price,
                    "low": h.low_price,
                    "close": h.close_price,
                    "volume": h.volume,
                    "amount": h.amount,
                }
                for h in history_data
            ]
            return SuccessResponse(items)

        # 数据库无数据，从 akshare 获取
        ak_code = index_code.replace(".SH", "").replace(".SZ", "")
        if index_code.endswith(".SH"):
            ak_code = f"sh{ak_code}"
        elif index_code.endswith(".SZ"):
            ak_code = f"sz{ak_code}"

        history_items = StockIndexService.get_index_history(
            index_code=ak_code,
            start_date=start_dt.strftime("%Y%m%d"),
            end_date=end_dt.strftime("%Y%m%d"),
        )

        if not history_items:
            return SuccessResponse([])

        # 存入数据库
        for item in history_items:
            data = {
                "index_code": index_code,
                "open_price": item.get("open"),
                "high_price": item.get("high"),
                "low_price": item.get("low"),
                "close_price": item.get("close"),
                "volume": item.get("volume"),
                "amount": item.get("amount"),
                "data_date": datetime.strptime(item["date"], "%Y-%m-%d").date(),
                "data_source": "akshare",
            }
            await dal.create_data(data=data, v_return_obj=False)

        return SuccessResponse(history_items)

    except Exception as e:
        logger.error(f"获取指数历史失败: {str(e)}")
        return ErrorResponse(f"获取指数历史失败: {str(e)}")


@router.get("/market/summary", summary="获取市场汇总数据")
async def get_market_summary(auth: Auth = Depends(OpenAuth())):
    """
    获取市场汇总数据
    - 主要指数行情
    - 涨跌统计
    - 成交数据
    - 涨跌停统计

    流程：
    1. 调用 MarketSummaryService 获取实时数据
    2. 返回汇总结果
    """
    try:
        # 调用 service 获取市场汇总数据
        summary_data = MarketSummaryService.get_market_summary()

        if not summary_data:
            return ErrorResponse("获取市场汇总数据失败")

        # 转换指数数据
        index_items = []
        for idx in summary_data.get("indices", []):
            index_items.append(
                schemas.StockIndexQuoteOut(
                    index_code=idx.get("index_code", ""),
                    index_name=idx.get("index_name", ""),
                    close_price=idx.get("current_price"),
                    change_percent=idx.get("change_percent"),
                    change_amount=idx.get("change_amount"),
                    volume=idx.get("volume"),
                    amount=idx.get("amount"),
                )
            )

        summary = schemas.MarketSummaryOut(
            indices=index_items,
            total_stocks=summary_data.get("total_stocks", 0),
            up_stocks=summary_data.get("up_stocks", 0),
            down_stocks=summary_data.get("down_stocks", 0),
            flat_stocks=summary_data.get("flat_stocks", 0),
            total_amount=summary_data.get("total_amount", 0),
            total_volume=summary_data.get("total_volume", 0),
            limit_up_count=summary_data.get("limit_up_count", 0),
            limit_down_count=summary_data.get("limit_down_count", 0),
            trade_date=date.today(),
            update_time=datetime.now(),
        )

        return SuccessResponse(summary)

    except Exception as e:
        logger.error(f"获取市场汇总失败: {str(e)}")
        return ErrorResponse(f"获取市场汇总失败: {str(e)}")


@router.get("/realtime/rankings", summary="获取实时排行")
async def get_realtime_rankings(
    limit: int = Query(20, ge=1, le=50, description="每类排行数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取实时涨跌幅、换手率、成交量、成交额排行

    流程：
    1. 调用 StockRankingService 获取实时排行数据
    2. 返回排行结果（不存储，实时性要求高）
    """
    try:
        service = StockRankingService()

        # 获取各类排行
        change_ranking = service.get_change_percent_ranking(limit)
        turnover_ranking = service.get_turnover_ranking(limit)
        volume_ranking = service.get_volume_ranking(limit)
        amount_ranking = service.get_amount_ranking(limit)

        # 转换为 Pydantic 模型
        def to_items(data):
            return [schemas.StockRankingItemOut(**item) for item in data]

        return SuccessResponse(
            schemas.RealtimeRankingsOut(
                change_percent_ranking=to_items(change_ranking),
                turnover_ranking=to_items(turnover_ranking),
                volume_ranking=to_items(volume_ranking),
                amount_ranking=to_items(amount_ranking),
                update_time=datetime.now(),
            )
        )

    except Exception as e:
        logger.error(f"获取实时排行失败: {str(e)}")
        return ErrorResponse(f"获取实时排行失败: {str(e)}")


@router.get("/fund-flow", summary="获取资金流向")
async def get_fund_flow(
    period: str = Query("daily", description="周期: daily/weekly/monthly"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取市场资金流向数据
    """
    try:
        return SuccessResponse({
            "message": "资金流向功能开发中",
            "period": period,
        })

    except Exception as e:
        logger.error(f"获取资金流向失败: {str(e)}")
        return ErrorResponse(f"获取资金流向失败: {str(e)}")