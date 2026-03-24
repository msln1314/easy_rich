# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/24
# @File           : stock_aggregate_routes.py
# @IDE            : PyCharm
# @desc           : 股票聚合查询API - 整合多维度数据

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

from app.services.stock_service import stock_service
from app.services.technical_indicator_service import technical_indicator_service
from app.services.pattern_service import pattern_service
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/overview/{stock_code}", summary="获取股票聚合概览")
async def get_stock_overview(stock_code: str) -> Dict[str, Any]:
    """
    获取股票聚合数据概览

    包含：基本信息、实时行情、板块归属、资金流向
    """
    logger.info(f"获取股票聚合概览: {stock_code}")

    try:
        # 并行获取基础数据
        basic_info_task = stock_service.get_stock_info(stock_code)
        quote_task = stock_service.get_stock_quote(stock_code)
        sectors_task = stock_service.get_stock_sectors(stock_code)
        fund_flow_task = stock_service.get_stock_fund_flow(stock_code)

        basic_info, quote, sectors, fund_flow = await asyncio.gather(
            basic_info_task, quote_task, sectors_task, fund_flow_task,
            return_exceptions=True
        )

        result = {
            "stock_code": stock_code,
            "update_time": datetime.now().isoformat(),
            "basic_info": basic_info if not isinstance(basic_info, Exception) else None,
            "quote": quote if not isinstance(quote, Exception) else None,
            "sectors": sectors if not isinstance(sectors, Exception) else None,
            "fund_flow": fund_flow if not isinstance(fund_flow, Exception) else None,
        }

        return result

    except Exception as e:
        logger.error(f"获取股票聚合概览失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/full/{stock_code}", summary="获取股票完整聚合数据")
async def get_stock_full_data(stock_code: str) -> Dict[str, Any]:
    """
    获取股票完整聚合数据

    包含：基本信息、行情、板块、资金流、技术指标、形态识别、财务、公告、研报、评级等
    """
    logger.info(f"获取股票完整聚合数据: {stock_code}")

    try:
        # 并行获取所有数据
        tasks = {
            "basic_info": stock_service.get_stock_info(stock_code),
            "quote": stock_service.get_stock_quote(stock_code),
            "sectors": stock_service.get_stock_sectors(stock_code),
            "fund_flow": stock_service.get_stock_fund_flow(stock_code),
            "margin": stock_service.get_stock_margin(stock_code),
            "financial": stock_service.get_stock_financial(stock_code),
            "technical": technical_indicator_service.analyze_all(stock_code),
            "patterns": pattern_service.detect_all_patterns(stock_code),
            "notices": stock_service.get_stock_notices(stock_code),
            "reports": stock_service.get_stock_report(stock_code),
            "rating": stock_service.get_stock_rating(stock_code),
            "pledge": stock_service.get_share_pledge(stock_code),
            "unlock": stock_service.get_unlock_schedule(stock_code),
        }

        # 执行所有任务
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        # 组装结果
        result = {
            "stock_code": stock_code,
            "update_time": datetime.now().isoformat(),
        }

        for (key, _), value in zip(tasks.items(), results):
            if isinstance(value, Exception):
                result[key] = {"error": str(value), "data": None}
                logger.warning(f"获取 {key} 失败: {str(value)}")
            else:
                result[key] = value

        # 添加数据摘要
        result["summary"] = _generate_summary(result)

        return result

    except Exception as e:
        logger.error(f"获取股票完整聚合数据失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/realtime/{stock_code}", summary="获取实时聚合数据")
async def get_realtime_data(stock_code: str) -> Dict[str, Any]:
    """
    获取实时聚合数据（高频更新）

    包含：实时行情、五档盘口、资金流
    """
    logger.info(f"获取实时聚合数据: {stock_code}")

    try:
        quote_task = stock_service.get_stock_quote(stock_code)
        quote_detail_task = stock_service.get_quote_detail(stock_code)
        fund_flow_task = stock_service.get_stock_fund_flow(stock_code)

        quote, quote_detail, fund_flow = await asyncio.gather(
            quote_task, quote_detail_task, fund_flow_task,
            return_exceptions=True
        )

        return {
            "stock_code": stock_code,
            "update_time": datetime.now().isoformat(),
            "quote": quote if not isinstance(quote, Exception) else None,
            "quote_detail": quote_detail if not isinstance(quote_detail, Exception) else None,
            "fund_flow": fund_flow if not isinstance(fund_flow, Exception) else None,
        }

    except Exception as e:
        logger.error(f"获取实时聚合数据失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/technical/{stock_code}", summary="获取技术分析聚合数据")
async def get_technical_data(
    stock_code: str,
    days: int = Query(60, ge=10, le=120, description="历史数据天数")
) -> Dict[str, Any]:
    """
    获取技术分析聚合数据

    包含：MACD、KDJ、RSI、BOLL、MA、形态识别
    """
    logger.info(f"获取技术分析聚合数据: {stock_code}")

    try:
        # 并行获取技术指标
        macd_task = technical_indicator_service.calculate_macd(stock_code, days=days)
        kdj_task = technical_indicator_service.calculate_kdj(stock_code, days=days)
        rsi_task = technical_indicator_service.calculate_rsi(stock_code, days=days)
        boll_task = technical_indicator_service.calculate_boll(stock_code, days=days)
        ma_task = technical_indicator_service.calculate_ma(stock_code, days=days)
        volume_task = technical_indicator_service.calculate_volume(stock_code, days=days)
        analysis_task = technical_indicator_service.analyze_all(stock_code)
        pattern_task = pattern_service.detect_all_patterns(stock_code)

        results = await asyncio.gather(
            macd_task, kdj_task, rsi_task, boll_task, ma_task,
            volume_task, analysis_task, pattern_task,
            return_exceptions=True
        )

        return {
            "stock_code": stock_code,
            "update_time": datetime.now().isoformat(),
            "macd": [r.__dict__ for r in results[0]] if not isinstance(results[0], Exception) and results[0] else [],
            "kdj": [r.__dict__ for r in results[1]] if not isinstance(results[1], Exception) and results[1] else [],
            "rsi": [r.__dict__ for r in results[2]] if not isinstance(results[2], Exception) and results[2] else [],
            "boll": [r.__dict__ for r in results[3]] if not isinstance(results[3], Exception) and results[3] else [],
            "ma": [r.__dict__ for r in results[4]] if not isinstance(results[4], Exception) and results[4] else [],
            "volume": [r.__dict__ for r in results[5]] if not isinstance(results[5], Exception) and results[5] else [],
            "analysis": results[6].__dict__ if not isinstance(results[6], Exception) else None,
            "patterns": [r.__dict__ for r in results[7]] if not isinstance(results[7], Exception) and results[7] else [],
        }

    except Exception as e:
        logger.error(f"获取技术分析聚合数据失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fund/{stock_code}", summary="获取资金相关聚合数据")
async def get_fund_data(stock_code: str) -> Dict[str, Any]:
    """
    获取资金相关聚合数据

    包含：资金流向、融资融券、股权质押、解禁计划
    """
    logger.info(f"获取资金相关聚合数据: {stock_code}")

    try:
        fund_flow_task = stock_service.get_stock_fund_flow(stock_code)
        margin_task = stock_service.get_stock_margin(stock_code)
        pledge_task = stock_service.get_share_pledge(stock_code)
        unlock_task = stock_service.get_unlock_schedule(stock_code)

        results = await asyncio.gather(
            fund_flow_task, margin_task, pledge_task, unlock_task,
            return_exceptions=True
        )

        return {
            "stock_code": stock_code,
            "update_time": datetime.now().isoformat(),
            "fund_flow": results[0] if not isinstance(results[0], Exception) else None,
            "margin": results[1] if not isinstance(results[1], Exception) else None,
            "pledge": results[2] if not isinstance(results[2], Exception) else None,
            "unlock_schedule": results[3] if not isinstance(results[3], Exception) else None,
        }

    except Exception as e:
        logger.error(f"获取资金相关聚合数据失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info/{stock_code}", summary="获取资讯相关聚合数据")
async def get_info_data(stock_code: str) -> Dict[str, Any]:
    """
    获取资讯相关聚合数据

    包含：公告、研报、评级
    """
    logger.info(f"获取资讯相关聚合数据: {stock_code}")

    try:
        notices_task = stock_service.get_stock_notices(stock_code)
        reports_task = stock_service.get_stock_report(stock_code)
        rating_task = stock_service.get_stock_rating(stock_code)

        results = await asyncio.gather(
            notices_task, reports_task, rating_task,
            return_exceptions=True
        )

        return {
            "stock_code": stock_code,
            "update_time": datetime.now().isoformat(),
            "notices": results[0] if not isinstance(results[0], Exception) else [],
            "reports": results[1] if not isinstance(results[1], Exception) else [],
            "rating": results[2] if not isinstance(results[2], Exception) else None,
        }

    except Exception as e:
        logger.error(f"获取资讯相关聚合数据失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def _generate_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    """生成数据摘要"""
    summary = {
        "has_basic_info": data.get("basic_info") is not None,
        "has_quote": data.get("quote") is not None,
        "has_technical": data.get("technical") is not None,
        "has_patterns": bool(data.get("patterns")),
        "has_fund_flow": data.get("fund_flow", {}).get("main_net_inflow") is not None,
        "has_reports": bool(data.get("reports")),
        "signal_count": 0,
        "pattern_count": 0,
    }

    # 统计信号数量
    analysis = data.get("technical")
    if analysis:
        signals = [
            analysis.macd_signal,
            analysis.kdj_signal,
            analysis.rsi_signal,
            analysis.ma_trend,
            analysis.volume_signal
        ]
        summary["signal_count"] = sum(1 for s in signals if s and s not in ["hold", "neutral", "unknown", "normal"])

    # 统计形态数量
    patterns = data.get("patterns", [])
    summary["pattern_count"] = len(patterns) if patterns else 0

    return summary