from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.models.index_models import IndexQuote
from app.services.index_service import IndexService

router = APIRouter()
index_service = IndexService()

@router.get("/quotes", response_model=List[IndexQuote])
async def get_index_quotes(symbol: str = Query("沪深重要指数", description="指数类型，如'沪深重要指数'")):
    """获取指数实时行情列表"""
    try:
        result = await index_service.get_index_quotes(symbol)
        if not result:
            raise HTTPException(status_code=404, detail=f"未找到指数类型 {symbol} 的行情数据")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取指数行情列表失败: {str(e)}")

@router.get("/{index_code}", response_model=IndexQuote)
async def get_index_quote(index_code: str):
    """获取单个指数实时行情"""
    try:
        result = await index_service.get_index_quote(index_code)
        if result is None:
            raise HTTPException(status_code=404, detail=f"未找到指数代码 {index_code} 的行情数据")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取指数行情失败: {str(e)}")