from fastapi import APIRouter, HTTPException, Query

from app.models.index_models import IndexQuote
from app.services.index_service import IndexService

router = APIRouter()
index_service = IndexService()

@router.get("/quotes")
async def get_index_quotes(symbol: str = Query("沪深重要指数", description="指数类型，如'沪深重要指数'")):
    """
    获取指数实时行情列表

    返回格式:
    {
        "items": [IndexQuote, ...],
        "source": "数据源标识"
    }
    """
    try:
        result, source = await index_service.get_index_quotes(symbol)
        if not result:
            raise HTTPException(status_code=404, detail=f"未找到指数类型 {symbol} 的行情数据")
        return {"items": result, "source": source}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取指数行情列表失败: {str(e)}")

@router.get("/{index_code}", response_model=IndexQuote)
async def get_index_quote(index_code: str):
    """获取单个指数实时行情"""
    try:
        result, _ = await index_service.get_index_quotes()
        # 查找匹配的指数
        for quote in result:
            if quote.code == index_code or quote.code.replace('.', '') == index_code.replace('.', ''):
                return quote
        raise HTTPException(status_code=404, detail=f"未找到指数代码 {index_code} 的行情数据")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取指数行情失败: {str(e)}")