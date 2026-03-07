from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime

from app.models.sentiment_models import MarginDetail, StockHotRank, StockHotUpRank, StockHotKeyword
from app.services.sentiment_service import SentimentService

router = APIRouter()
sentiment_service = SentimentService()

@router.get("/margin/details", response_model=List[MarginDetail])
async def get_margin_details(
    trade_date: str = Query(..., description="交易日期，格式为YYYYMMDD，如20230922")
):
    """获取融资融券明细数据（上海和深圳市场合并）"""
    try:
        # 验证日期格式
        try:
            datetime.strptime(trade_date, "%Y%m%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，应为YYYYMMDD，如20230922")
        
        result = await sentiment_service.get_margin_details(trade_date)
        if not result:
            raise HTTPException(status_code=404, detail=f"未找到 {trade_date} 的融资融券明细数据")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取融资融券明细数据失败: {str(e)}")

@router.get("/stock/hot-rank", response_model=List[StockHotRank])
async def get_stock_hot_rank():
    """获取股票热度排名数据（东方财富网-人气榜-A股）"""
    try:
        result = await sentiment_service.get_stock_hot_rank()
        if not result:
            raise HTTPException(status_code=404, detail="未获取到股票热度排名数据")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票热度排名数据失败: {str(e)}")

@router.get("/stock/hot-up-rank", response_model=List[StockHotUpRank])
async def get_stock_hot_up_rank():
    """获取股票飙升榜数据（东方财富网-个股人气榜-飙升榜）"""
    try:
        result = await sentiment_service.get_stock_hot_up_rank()
        if not result:
            raise HTTPException(status_code=404, detail="未获取到股票飙升榜数据")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票飙升榜数据失败: {str(e)}")

@router.get("/stock/hot-keywords", response_model=List[StockHotKeyword])
async def get_stock_hot_keywords(
    symbol: str = Query(..., description="股票代码，如SZ000665")
):
    """获取股票热门关键词数据（东方财富网-个股人气榜-热门关键词）"""
    try:
        result = await sentiment_service.get_stock_hot_keywords(symbol)
        if not result:
            raise HTTPException(status_code=404, detail=f"未找到股票 {symbol} 的热门关键词数据")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票热门关键词数据失败: {str(e)}")