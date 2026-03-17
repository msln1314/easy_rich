from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.models.technical_models import ChipDistribution
from app.services.technical_service import TechnicalService
from app.services.technical_indicator_service import technical_indicator_service

router = APIRouter()
technical_service = TechnicalService()


@router.get("/chip-distribution", response_model=List[ChipDistribution])
async def get_chip_distribution(
    symbol: str = Query(..., description="股票代码，如'000001'"),
    adjust: str = Query(
        "",
        description="复权类型，可选值为'qfq'(前复权)、'hfq'(后复权)、''(不复权)，默认为不复权",
    ),
):
    """获取股票筹码分布数据"""
    try:
        result = await technical_service.get_chip_distribution(symbol, adjust)
        if not result:
            raise HTTPException(
                status_code=404, detail=f"未找到股票代码 {symbol} 的筹码分布数据"
            )
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"获取股票筹码分布数据失败: {str(e)}"
        )


# ========== 技术指标计算接口 ==========


@router.get("/macd/{stock_code}", summary="计算MACD指标")
async def calculate_macd(
    stock_code: str, days: int = Query(60, ge=10, le=250, description="计算天数")
):
    """计算MACD指标，返回DIF、DEA、MACD柱及买卖信号"""
    try:
        result = await technical_indicator_service.calculate_macd(stock_code, days=days)
        return {
            "stock_code": stock_code,
            "data": [r.__dict__ for r in result],
            "count": len(result),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kdj/{stock_code}", summary="计算KDJ指标")
async def calculate_kdj(
    stock_code: str, days: int = Query(60, ge=10, le=250, description="计算天数")
):
    """计算KDJ指标，返回K、D、J值及买卖信号"""
    try:
        result = await technical_indicator_service.calculate_kdj(stock_code, days=days)
        return {
            "stock_code": stock_code,
            "data": [r.__dict__ for r in result],
            "count": len(result),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rsi/{stock_code}", summary="计算RSI指标")
async def calculate_rsi(
    stock_code: str, days: int = Query(60, ge=10, le=250, description="计算天数")
):
    """计算RSI指标，返回RSI6、RSI12、RSI24及超买超卖信号"""
    try:
        result = await technical_indicator_service.calculate_rsi(stock_code, days=days)
        return {
            "stock_code": stock_code,
            "data": [r.__dict__ for r in result],
            "count": len(result),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/boll/{stock_code}", summary="计算布林带指标")
async def calculate_boll(
    stock_code: str, days: int = Query(60, ge=10, le=250, description="计算天数")
):
    """计算布林带指标，返回上轨、中轨、下轨及带宽"""
    try:
        result = await technical_indicator_service.calculate_boll(stock_code, days=days)
        return {
            "stock_code": stock_code,
            "data": [r.__dict__ for r in result],
            "count": len(result),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ma/{stock_code}", summary="计算均线指标")
async def calculate_ma(
    stock_code: str, days: int = Query(60, ge=10, le=250, description="计算天数")
):
    """计算均线指标，返回MA5、MA10、MA20、MA60及趋势判断"""
    try:
        result = await technical_indicator_service.calculate_ma(stock_code, days=days)
        return {
            "stock_code": stock_code,
            "data": [r.__dict__ for r in result],
            "count": len(result),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/volume/{stock_code}", summary="计算成交量指标")
async def calculate_volume(
    stock_code: str, days: int = Query(60, ge=10, le=250, description="计算天数")
):
    """计算成交量指标，返回成交量、均量、OBV及放量缩量信号"""
    try:
        result = await technical_indicator_service.calculate_volume(
            stock_code, days=days
        )
        return {
            "stock_code": stock_code,
            "data": [r.__dict__ for r in result],
            "count": len(result),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/{stock_code}", summary="综合技术分析")
async def analyze_all(stock_code: str):
    """综合技术分析，结合MACD、KDJ、RSI、BOLL、MA、成交量给出综合评分和买卖建议"""
    try:
        result = await technical_indicator_service.analyze_all(stock_code)
        return result.__dict__
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
