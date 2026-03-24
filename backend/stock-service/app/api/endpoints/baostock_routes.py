# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/24
# @File           : baostock_routes.py
# @IDE            : PyCharm
# @desc           : 证券宝数据源API路由

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta

from app.services.baostock_source import baostock_source

router = APIRouter()


# ==================== 数据可用性检查 ====================

@router.get("/availability")
async def check_availability():
    """检查证券宝数据源是否可用"""
    return {
        "available": baostock_source.is_available(),
        "message": "证券宝数据源可用" if baostock_source.is_available() else "证券宝数据源不可用，请安装baostock包"
    }


# ==================== K线数据 ====================

@router.get("/kline/{stock_code}")
async def get_kline(
    stock_code: str,
    start_date: Optional[str] = Query(None, description="开始日期，格式YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式YYYY-MM-DD"),
    period: str = Query("d", description="周期: d-日线, w-周线, m-月线"),
    adjust: str = Query("2", description="复权类型: 1-后复权, 2-前复权, 3-不复权"),
    days: int = Query(100, description="最近N天（当start_date为空时生效）"),
):
    """
    获取股票历史K线数据

    Args:
        stock_code: 股票代码，如 000001
        start_date: 开始日期
        end_date: 结束日期
        period: 周期 d/w/m
        adjust: 复权类型 1-后复权, 2-前复权, 3-不复权
        days: 最近N天
    """
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    if not start_date:
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        klines = await baostock_source.get_history_kline_async(
            stock_code, start_date, end_date, period, adjust
        )
        return {
            "code": stock_code,
            "start_date": start_date,
            "end_date": end_date,
            "period": period,
            "adjust": adjust,
            "count": len(klines),
            "data": [
                {
                    "trade_date": k.trade_date,
                    "open": k.open,
                    "high": k.high,
                    "low": k.low,
                    "close": k.close,
                    "volume": k.volume,
                    "amount": k.amount,
                    "turnover": k.turnover,
                    "change_percent": k.change_percent,
                    "change_amount": k.change_amount,
                    "amplitude": k.amplitude,
                }
                for k in klines
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取K线数据失败: {str(e)}")


# ==================== 股票列表 ====================

@router.get("/stocks")
async def get_all_stocks(
    date: Optional[str] = Query(None, description="查询日期，格式YYYY-MM-DD")
):
    """获取全部股票列表"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        stocks = baostock_source.get_all_stocks(date)
        return {
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "count": len(stocks),
            "data": [
                {
                    "code": s.code,
                    "name": s.name,
                    "industry": s.industry,
                    "list_date": s.list_date,
                    "type": s.type,
                    "status": s.status,
                }
                for s in stocks
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票列表失败: {str(e)}")


@router.get("/stocks/by-industry")
async def get_stocks_by_industry(
    industry: str = Query(..., description="行业名称")
):
    """根据行业获取股票列表"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        codes = baostock_source.get_stock_list_by_industry(industry)
        return {
            "industry": industry,
            "count": len(codes),
            "data": codes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行业股票列表失败: {str(e)}")


# ==================== 行业分类 ====================

@router.get("/industries")
async def get_all_industries():
    """获取所有行业列表"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        industries = baostock_source.get_all_industries()
        return {
            "count": len(industries),
            "data": industries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行业列表失败: {str(e)}")


@router.get("/industries/classification")
async def get_industry_classification(
    stock_code: Optional[str] = Query(None, description="股票代码，为空则获取所有")
):
    """获取行业分类数据"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        classifications = baostock_source.get_industry_classification(stock_code)
        return {
            "count": len(classifications),
            "data": [
                {
                    "code": c.code,
                    "name": c.name,
                    "industry": c.industry,
                    "industry_classification": c.industry_classification,
                }
                for c in classifications
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行业分类失败: {str(e)}")


# ==================== 财务数据 ====================

@router.get("/financial/{stock_code}")
async def get_financial_indicator(
    stock_code: str,
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    year: Optional[str] = Query(None, description="年份"),
    quarter: Optional[int] = Query(None, description="季度1-4"),
):
    """获取财务指标数据"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        indicators = baostock_source.get_financial_indicator(
            stock_code, start_date, end_date, year, quarter
        )
        return {
            "code": stock_code,
            "count": len(indicators),
            "data": [
                {
                    "code": i.code,
                    "pub_date": i.pub_date,
                    "stat_date": i.stat_date,
                    "roe": i.roe,
                    "roe_dt": i.roe_dt,
                    "roa": i.roa,
                    "eps": i.eps,
                    "bvps": i.bvps,
                    "cfps": i.cfps,
                    "net_profit": i.net_profit,
                    "net_profit_yoy": i.net_profit_yoy,
                    "revenue": i.revenue,
                    "revenue_yoy": i.revenue_yoy,
                    "gross_margin": i.gross_margin,
                    "net_margin": i.net_margin,
                    "debt_ratio": i.debt_ratio,
                    "current_ratio": i.current_ratio,
                    "quick_ratio": i.quick_ratio,
                }
                for i in indicators
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取财务指标失败: {str(e)}")


# ==================== 分红送股 ====================

@router.get("/dividend/{stock_code}")
async def get_dividend(
    stock_code: str,
    year: Optional[str] = Query(None, description="年份"),
    year_type: str = Query("report", description="年份类型: report-公告年, oper-实施年"),
):
    """获取分红送股数据"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        dividends = baostock_source.get_dividend(stock_code, year, year_type)
        return {
            "code": stock_code,
            "count": len(dividends),
            "data": [
                {
                    "code": d.code,
                    "pub_date": d.pub_date,
                    "div_year": d.div_year,
                    "ann_date": d.ann_date,
                    "record_date": d.record_date,
                    "ex_date": d.ex_date,
                    "pay_date": d.pay_date,
                    "dividend": d.dividend,
                    "transfer": d.transfer,
                    "bonus": d.bonus,
                }
                for d in dividends
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取分红数据失败: {str(e)}")


# ==================== 复权因子 ====================

@router.get("/adjust-factor/{stock_code}")
async def get_adjust_factor(
    stock_code: str,
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
):
    """获取复权因子"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        factors = baostock_source.get_adjust_factor(stock_code, start_date, end_date)
        return {
            "code": stock_code,
            "count": len(factors),
            "data": [
                {
                    "code": f.code,
                    "date": f.date,
                    "fore_adjust": f.fore_adjust,
                    "back_adjust": f.back_adjust,
                }
                for f in factors
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取复权因子失败: {str(e)}")


# ==================== 指数数据 ====================

@router.get("/index/kline/{index_code}")
async def get_index_kline(
    index_code: str,
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    period: str = Query("d", description="周期: d-日线, w-周线, m-月线"),
    days: int = Query(100, description="最近N天"),
):
    """
    获取指数K线数据

    Args:
        index_code: 指数代码，如 sh.000001（上证指数）、sz.399001（深证成指）
    """
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    if not start_date:
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        klines = baostock_source.get_index_kline(index_code, start_date, end_date, period)
        return {
            "code": index_code,
            "start_date": start_date,
            "end_date": end_date,
            "period": period,
            "count": len(klines),
            "data": klines
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取指数K线失败: {str(e)}")


@router.get("/index/stocks/{index_code}")
async def get_index_stocks(
    index_code: str,
    date: Optional[str] = Query(None, description="查询日期"),
):
    """获取指数成份股"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        stocks = baostock_source.get_index_stocks(index_code, date)
        return {
            "index_code": index_code,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "count": len(stocks),
            "data": stocks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取指数成份股失败: {str(e)}")


# ==================== 交易日历 ====================

@router.get("/trade-dates")
async def get_trade_dates(
    start_date: str = Query(..., description="开始日期"),
    end_date: str = Query(..., description="结束日期"),
):
    """获取交易日历"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        dates = baostock_source.get_trade_dates(start_date, end_date)
        return {
            "start_date": start_date,
            "end_date": end_date,
            "count": len(dates),
            "data": dates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取交易日历失败: {str(e)}")


@router.get("/is-trade-date")
async def is_trade_date(
    date: str = Query(..., description="日期，格式YYYY-MM-DD")
):
    """判断是否为交易日"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        is_trade = baostock_source.is_trade_date(date)
        return {
            "date": date,
            "is_trade_date": is_trade
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"判断交易日失败: {str(e)}")


# ==================== 停复牌信息 ====================

@router.get("/suspend")
async def get_suspend_info(
    stock_code: Optional[str] = Query(None, description="股票代码"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
):
    """获取停复牌信息"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        suspends = baostock_source.get_suspend_info(stock_code, start_date, end_date)
        return {
            "count": len(suspends),
            "data": suspends
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取停复牌信息失败: {str(e)}")


# ==================== 业绩预告/快报 ====================

@router.get("/performance/forecast")
async def get_performance_forecast(
    stock_code: Optional[str] = Query(None, description="股票代码"),
    year: Optional[int] = Query(None, description="年份"),
    quarter: Optional[int] = Query(None, description="季度"),
):
    """获取业绩预告"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        forecasts = baostock_source.get_performance_forecast(stock_code, year, quarter)
        return {
            "count": len(forecasts),
            "data": forecasts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取业绩预告失败: {str(e)}")


@router.get("/performance/express")
async def get_performance_express(
    stock_code: Optional[str] = Query(None, description="股票代码"),
    year: Optional[int] = Query(None, description="年份"),
    quarter: Optional[int] = Query(None, description="季度"),
):
    """获取业绩快报"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        expresses = baostock_source.get_performance_express(stock_code, year, quarter)
        return {
            "count": len(expresses),
            "data": expresses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取业绩快报失败: {str(e)}")


# ==================== 增减持 ====================

@router.get("/hold-changes")
async def get_stock_hold_changes(
    stock_code: Optional[str] = Query(None, description="股票代码"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
):
    """获取增减持数据"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        changes = baostock_source.get_stock_hold_changes(stock_code, start_date, end_date)
        return {
            "count": len(changes),
            "data": changes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取增减持数据失败: {str(e)}")


# ==================== 估值指标 ====================

@router.get("/valuation/{stock_code}")
async def get_stock_valuation(
    stock_code: str,
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    days: int = Query(100, description="最近N天"),
):
    """获取估值指标 (PE/PB/PS/PCF)"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    if not start_date:
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        valuations = baostock_source.get_stock_valuation(stock_code, start_date, end_date)
        return {
            "code": stock_code,
            "start_date": start_date,
            "end_date": end_date,
            "count": len(valuations),
            "data": valuations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取估值指标失败: {str(e)}")


# ==================== 宏观数据 ====================

@router.get("/macro")
async def get_macro_economy(
    indicator: Optional[str] = Query(None, description="指标代码，为空则获取所有")
):
    """获取宏观经济数据"""
    if not baostock_source.is_available():
        raise HTTPException(status_code=503, detail="证券宝数据源不可用")

    try:
        data = baostock_source.get_macro_economy(indicator)
        return {
            "indicator": indicator,
            "count": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取宏观数据失败: {str(e)}")