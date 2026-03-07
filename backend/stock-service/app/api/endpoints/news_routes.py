from fastapi import APIRouter, HTTPException, Query
from typing import List
from enum import Enum

from app.models.news_models import InteractiveQuestion, GlobalFinanceNews, CLSTelegraph
from app.services.news_service import NewsService

router = APIRouter()
news_service = NewsService()

@router.get("/interactive/questions", response_model=List[InteractiveQuestion])
async def get_interactive_questions(
    symbol: str = Query(..., description="股票代码，如002594")
):
    """获取互动易提问数据"""
    try:
        result = await news_service.get_interactive_questions(symbol)
        if not result:
            raise HTTPException(status_code=404, detail=f"未找到股票 {symbol} 的互动易提问数据")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取互动易提问数据失败: {str(e)}")

@router.get("/global-finance", response_model=List[GlobalFinanceNews])
async def get_global_finance_news():
    """获取全球财经快讯数据（东方财富-全球财经快讯）"""
    try:
        result = await news_service.get_global_finance_news()
        if not result:
            raise HTTPException(status_code=404, detail="未获取到全球财经快讯数据")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取全球财经快讯数据失败: {str(e)}")


class CLSSymbolType(str, Enum):
    """财联社电报类型枚举"""
    ALL = "全部"
    IMPORTANT = "重点"


@router.get("/cls-telegraph", response_model=List[CLSTelegraph])
async def get_cls_telegraph(
    symbol: CLSSymbolType = Query(CLSSymbolType.ALL, description="类型: 全部或重点")
):
    """获取财联社电报数据"""
    try:
        result = await news_service.get_cls_telegraph(symbol)
        if not result:
            raise HTTPException(status_code=404, detail=f"未获取到财联社电报数据: {symbol}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取财联社电报数据失败: {str(e)}")