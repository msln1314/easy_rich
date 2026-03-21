#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/21
# @File           : stock_selection.py
# @IDE            : PyCharm
# @desc           : 选股信号API接口

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy import select, desc, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import date, datetime

from apps.admin.auth.utils.current import OpenAuth, Auth
from apps.admin.stock.models.stock_selection_signal import StockSelectionSignal
from apps.admin.stock.services.selection_signal_service import sync_selection_signals
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger

router = APIRouter(prefix="/stock/selection", tags=["选股信号"])


@router.get("", summary="获取选股信号列表")
async def get_selection_signals(
    signal_date: Optional[date] = Query(None, description="信号日期，默认今天"),
    recommend: Optional[str] = Query(
        None, description="推荐信号: strong_buy/buy/hold/sell/strong_sell"
    ),
    min_score: Optional[float] = Query(None, ge=0, le=100, description="最低评分"),
    max_score: Optional[float] = Query(None, ge=0, le=100, description="最高评分"),
    ma_signal: Optional[int] = Query(
        None, ge=-1, le=1, description="均线信号: 1金叉/-1死叉/0无"
    ),
    macd_signal: Optional[int] = Query(
        None, ge=-1, le=1, description="MACD信号: 1金叉/-1死叉/0无"
    ),
    kdj_signal: Optional[int] = Query(
        None, ge=-1, le=1, description="KDJ信号: 1金叉/-1死叉/0无"
    ),
    rsi_signal: Optional[int] = Query(
        None, ge=-1, le=1, description="RSI信号: 1超卖/-1超买/0无"
    ),
    volume_signal: Optional[int] = Query(
        None, ge=-1, le=1, description="成交量信号: 1放量/-1缩量/0无"
    ),
    industry: Optional[str] = Query(None, description="行业筛选"),
    market: Optional[str] = Query(None, description="市场筛选: SH/SZ"),
    stock_code: Optional[str] = Query(None, description="股票代码"),
    stock_name: Optional[str] = Query(None, description="股票名称(模糊搜索)"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取选股信号列表

    支持多条件筛选：
    - 按推荐信号筛选
    - 按评分范围筛选
    - 按技术信号筛选（MA/MACD/KDJ/RSI/成交量）
    - 按行业/市场筛选
    """
    try:
        db = auth.db
        query_date = signal_date or date.today()

        query = select(StockSelectionSignal).filter(
            StockSelectionSignal.signal_date == query_date
        )

        if recommend:
            query = query.filter(StockSelectionSignal.recommend == recommend)

        if min_score is not None:
            query = query.filter(StockSelectionSignal.total_score >= min_score)

        if max_score is not None:
            query = query.filter(StockSelectionSignal.total_score <= max_score)

        if ma_signal is not None:
            query = query.filter(StockSelectionSignal.ma_signal == ma_signal)

        if macd_signal is not None:
            query = query.filter(StockSelectionSignal.macd_signal == macd_signal)

        if kdj_signal is not None:
            query = query.filter(StockSelectionSignal.kdj_signal == kdj_signal)

        if rsi_signal is not None:
            query = query.filter(StockSelectionSignal.rsi_signal == rsi_signal)

        if volume_signal is not None:
            query = query.filter(StockSelectionSignal.volume_signal == volume_signal)

        if industry:
            query = query.filter(StockSelectionSignal.industry == industry)

        if market:
            query = query.filter(StockSelectionSignal.market == market)

        if stock_code:
            query = query.filter(StockSelectionSignal.stock_code == stock_code)

        if stock_name:
            query = query.filter(
                StockSelectionSignal.stock_name.like(f"%{stock_name}%")
            )

        query = query.order_by(desc(StockSelectionSignal.total_score))

        total_query = select(StockSelectionSignal).filter(
            StockSelectionSignal.signal_date == query_date
        )
        if recommend:
            total_query = total_query.filter(
                StockSelectionSignal.recommend == recommend
            )

        count_query = select(StockSelectionSignal.id).filter(
            StockSelectionSignal.signal_date == query_date
        )
        if recommend:
            count_query = count_query.filter(
                StockSelectionSignal.recommend == recommend
            )

        from sqlalchemy import func

        count_result = await db.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar()

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await db.execute(query)
        signals = result.scalars().all()

        items = []
        for s in signals:
            items.append(
                {
                    "id": s.id,
                    "stock_code": s.stock_code,
                    "stock_name": s.stock_name,
                    "full_code": s.full_code,
                    "market": s.market,
                    "industry": s.industry,
                    "signal_date": s.signal_date,
                    "current_price": s.current_price,
                    "change_percent": s.change_percent,
                    "ma_signal": s.ma_signal,
                    "macd_signal": s.macd_signal,
                    "kdj_signal": s.kdj_signal,
                    "rsi_signal": s.rsi_signal,
                    "volume_signal": s.volume_signal,
                    "total_score": s.total_score,
                    "score_rank": s.score_rank,
                    "recommend": s.recommend,
                    "signal_strength": s.signal_strength,
                    "confidence": s.confidence,
                    "data_time": s.data_time,
                }
            )

        return SuccessResponse(
            {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "signal_date": query_date,
            }
        )

    except Exception as e:
        logger.error(f"获取选股信号列表失败: {str(e)}")
        return ErrorResponse(f"获取选股信号列表失败: {str(e)}")


@router.get("/buy-signals", summary="获取买入信号股票")
async def get_buy_signals(
    signal_date: Optional[date] = Query(None, description="信号日期"),
    min_score: Optional[float] = Query(50, ge=0, le=100, description="最低评分"),
    limit: int = Query(50, ge=1, le=200, description="返回数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取买入信号股票列表

    返回 recommend 为 strong_buy 或 buy 的股票
    """
    try:
        db = auth.db
        query_date = signal_date or date.today()

        query = (
            select(StockSelectionSignal)
            .filter(
                StockSelectionSignal.signal_date == query_date,
                StockSelectionSignal.recommend.in_(["strong_buy", "buy"]),
                StockSelectionSignal.total_score >= min_score,
            )
            .order_by(desc(StockSelectionSignal.total_score))
            .limit(limit)
        )

        result = await db.execute(query)
        signals = result.scalars().all()

        items = []
        for s in signals:
            items.append(
                {
                    "stock_code": s.stock_code,
                    "stock_name": s.stock_name,
                    "current_price": s.current_price,
                    "change_percent": s.change_percent,
                    "total_score": s.total_score,
                    "score_rank": s.score_rank,
                    "recommend": s.recommend,
                    "signal_strength": s.signal_strength,
                    "ma_signal": s.ma_signal,
                    "macd_signal": s.macd_signal,
                    "kdj_signal": s.kdj_signal,
                    "rsi_signal": s.rsi_signal,
                    "volume_signal": s.volume_signal,
                    "industry": s.industry,
                }
            )

        return SuccessResponse(items)

    except Exception as e:
        logger.error(f"获取买入信号失败: {str(e)}")
        return ErrorResponse(f"获取买入信号失败: {str(e)}")


@router.get("/multi-filter", summary="多因子筛选")
async def multi_factor_filter(
    signal_date: Optional[date] = Query(None, description="信号日期"),
    require_macd_golden: bool = Query(False, description="必须MACD金叉"),
    require_kdj_golden: bool = Query(False, description="必须KDJ金叉"),
    require_ma_golden: bool = Query(False, description="必须均线金叉"),
    require_volume_increase: bool = Query(False, description="必须放量"),
    require_rsi_oversold: bool = Query(False, description="必须RSI超卖"),
    min_score: Optional[float] = Query(None, ge=0, le=100, description="最低评分"),
    industry: Optional[str] = Query(None, description="行业"),
    market: Optional[str] = Query(None, description="市场"),
    limit: int = Query(50, ge=1, le=200, description="返回数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    多因子筛选股票

    可组合多个技术信号条件进行筛选
    """
    try:
        db = auth.db
        query_date = signal_date or date.today()

        query = select(StockSelectionSignal).filter(
            StockSelectionSignal.signal_date == query_date
        )

        if require_macd_golden:
            query = query.filter(StockSelectionSignal.macd_signal == 1)

        if require_kdj_golden:
            query = query.filter(StockSelectionSignal.kdj_signal == 1)

        if require_ma_golden:
            query = query.filter(StockSelectionSignal.ma_signal == 1)

        if require_volume_increase:
            query = query.filter(StockSelectionSignal.volume_signal == 1)

        if require_rsi_oversold:
            query = query.filter(StockSelectionSignal.rsi_signal == 1)

        if min_score is not None:
            query = query.filter(StockSelectionSignal.total_score >= min_score)

        if industry:
            query = query.filter(StockSelectionSignal.industry == industry)

        if market:
            query = query.filter(StockSelectionSignal.market == market)

        query = query.order_by(desc(StockSelectionSignal.total_score)).limit(limit)

        result = await db.execute(query)
        signals = result.scalars().all()

        items = []
        for s in signals:
            items.append(
                {
                    "stock_code": s.stock_code,
                    "stock_name": s.stock_name,
                    "current_price": s.current_price,
                    "total_score": s.total_score,
                    "recommend": s.recommend,
                    "ma_signal": s.ma_signal,
                    "macd_signal": s.macd_signal,
                    "kdj_signal": s.kdj_signal,
                    "rsi_signal": s.rsi_signal,
                    "volume_signal": s.volume_signal,
                    "industry": s.industry,
                }
            )

        return SuccessResponse(items)

    except Exception as e:
        logger.error(f"多因子筛选失败: {str(e)}")
        return ErrorResponse(f"多因子筛选失败: {str(e)}")


@router.get("/{stock_code}", summary="获取单只股票选股信号")
async def get_stock_signal(
    stock_code: str,
    signal_date: Optional[date] = Query(None, description="信号日期"),
    auth: Auth = Depends(OpenAuth()),
):
    """获取单只股票的选股信号详情"""
    try:
        db = auth.db
        query_date = signal_date or date.today()

        query = select(StockSelectionSignal).filter(
            StockSelectionSignal.stock_code == stock_code,
            StockSelectionSignal.signal_date == query_date,
        )

        result = await db.execute(query)
        signal = result.scalar_one_or_none()

        if not signal:
            return ErrorResponse(f"未找到股票 {stock_code} 的信号数据")

        import json

        signal_detail = {}
        if signal.signal_detail:
            try:
                signal_detail = json.loads(signal.signal_detail)
            except:
                pass

        return SuccessResponse(
            {
                "stock_code": signal.stock_code,
                "stock_name": signal.stock_name,
                "full_code": signal.full_code,
                "market": signal.market,
                "industry": signal.industry,
                "signal_date": signal.signal_date,
                "current_price": signal.current_price,
                "change_percent": signal.change_percent,
                "volume": signal.volume,
                "amount": signal.amount,
                "ma_signal": signal.ma_signal,
                "macd_signal": signal.macd_signal,
                "kdj_signal": signal.kdj_signal,
                "rsi_signal": signal.rsi_signal,
                "boll_signal": signal.boll_signal,
                "volume_signal": signal.volume_signal,
                "ma5": signal.ma5,
                "ma10": signal.ma10,
                "ma20": signal.ma20,
                "dif": signal.dif,
                "dea": signal.dea,
                "macd": signal.macd,
                "k_value": signal.k_value,
                "d_value": signal.d_value,
                "j_value": signal.j_value,
                "rsi_value": signal.rsi_value,
                "macd_score": signal.macd_score,
                "kdj_score": signal.kdj_score,
                "rsi_score": signal.rsi_score,
                "ma_score": signal.ma_score,
                "volume_score": signal.volume_score,
                "trend_score": signal.trend_score,
                "potential_score": signal.potential_score,
                "total_score": signal.total_score,
                "score_rank": signal.score_rank,
                "recommend": signal.recommend,
                "signal_strength": signal.signal_strength,
                "confidence": signal.confidence,
                "volatility": signal.volatility,
                "max_drawdown": signal.max_drawdown,
                "signal_detail": signal_detail,
                "data_time": signal.data_time,
            }
        )

    except Exception as e:
        logger.error(f"获取股票信号失败: {str(e)}")
        return ErrorResponse(f"获取股票信号失败: {str(e)}")


@router.post("/sync", summary="手动同步选股信号")
async def sync_signals(
    limit: int = Body(500, description="处理股票数量"),
    auth: Auth = Depends(OpenAuth()),
):
    """手动触发选股信号生成"""
    try:
        result = await sync_selection_signals(auth.db, limit)
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"同步选股信号失败: {str(e)}")
        return ErrorResponse(f"同步选股信号失败: {str(e)}")


@router.get("/statistics/overview", summary="获取信号统计概览")
async def get_signal_statistics(
    signal_date: Optional[date] = Query(None, description="信号日期"),
    auth: Auth = Depends(OpenAuth()),
):
    """获取当日信号统计概览"""
    try:
        db = auth.db
        query_date = signal_date or date.today()

        from sqlalchemy import func

        total_query = (
            select(func.count())
            .select_from(StockSelectionSignal)
            .filter(StockSelectionSignal.signal_date == query_date)
        )
        total_result = await db.execute(total_query)
        total = total_result.scalar()

        recommend_query = (
            select(StockSelectionSignal.recommend, func.count().label("count"))
            .filter(StockSelectionSignal.signal_date == query_date)
            .group_by(StockSelectionSignal.recommend)
        )

        recommend_result = await db.execute(recommend_query)
        recommend_stats = {row.recommend: row.count for row in recommend_result}

        score_ranges = [
            ("high", 80, 100),
            ("good", 60, 80),
            ("medium", 40, 60),
            ("low", 20, 40),
            ("poor", 0, 20),
        ]
        score_stats = {}
        for name, min_s, max_s in score_ranges:
            count_query = (
                select(func.count())
                .select_from(StockSelectionSignal)
                .filter(
                    StockSelectionSignal.signal_date == query_date,
                    StockSelectionSignal.total_score >= min_s,
                    StockSelectionSignal.total_score < max_s,
                )
            )
            count_result = await db.execute(count_query)
            score_stats[name] = count_result.scalar()

        return SuccessResponse(
            {
                "signal_date": query_date,
                "total": total,
                "recommend_stats": recommend_stats,
                "score_stats": score_stats,
            }
        )

    except Exception as e:
        logger.error(f"获取信号统计失败: {str(e)}")
        return ErrorResponse(f"获取信号统计失败: {str(e)}")
