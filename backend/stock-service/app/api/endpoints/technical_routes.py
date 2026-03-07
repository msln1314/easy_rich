from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.models.technical_models import ChipDistribution
from app.services.technical_service import TechnicalService

router = APIRouter()
technical_service = TechnicalService()

@router.get("/chip-distribution", response_model=List[ChipDistribution])
async def get_chip_distribution(
    symbol: str = Query(..., description="股票代码，如'000001'"),
    adjust: str = Query("", description="复权类型，可选值为'qfq'(前复权)、'hfq'(后复权)、''(不复权)，默认为不复权")
):
    """获取股票筹码分布数据"""
    try:
        result = await technical_service.get_chip_distribution(symbol, adjust)
        if not result:
            raise HTTPException(status_code=404, detail=f"未找到股票代码 {symbol} 的筹码分布数据")
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票筹码分布数据失败: {str(e)}")