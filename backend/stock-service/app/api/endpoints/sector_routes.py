from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models.sector_models import (
    ConceptBoard,
    IndustryBoard,
    BoardSpot,
    ConceptBoardSpot,
    IndustryBoardSpot,
    ConceptBoardConstituent,
    IndustryBoardConstituent,
    SectorLeader,
    SectorRealtimeStatus,
    SectorRotationHistory,
    RotationPrediction,
    SectorFactor,
)
from app.services.sector_service import SectorService

router = APIRouter()
sector_service = SectorService()


@router.get("/concept", response_model=List[ConceptBoard])
async def get_concept_boards():
    """获取概念板块列表及实时行情（优先 AKShare，失败时降级到 Tushare）"""
    try:
        return await sector_service.get_concept_boards()
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"获取概念板块列表失败: {str(e)}")


# 使用更具体的路径，避免与 /concept/{board_code} 冲突
@router.get("/concept/by-name/spot", response_model=ConceptBoardSpot)
async def get_concept_board_spot_by_name(
    name: str = Query(..., description="概念板块名称，如'可燃冰'"),
):
    """获取概念板块实时行情详情（通过名称）"""
    try:
        # 直接调用获取实时行情详情的方法，传入板块名称
        result = await sector_service.get_concept_board_spot(name)
        if not result:
            raise HTTPException(
                status_code=404, detail=f"未找到板块名称 {name} 的实时行情数据"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"获取概念板块实时行情详情失败: {str(e)}"
        )


# 使用更具体的路径，避免与 /concept/{board_code} 冲突
@router.get(
    "/concept/by-symbol/constituents", response_model=List[ConceptBoardConstituent]
)
async def get_concept_board_constituents(
    symbol: str = Query(..., description="板块名称或代码，如'融资融券'或'BK0655'"),
):
    """获取概念板块成份股"""
    try:
        # 直接传递参数给服务方法，不需要额外处理
        # AKShare的接口支持直接使用板块名称或代码
        result = await sector_service.get_concept_board_constituents(symbol)
        if not result:
            raise HTTPException(
                status_code=404, detail=f"未找到板块 {symbol} 的成份股数据"
            )
        return result
    except ValueError as e:
        # 捕获并处理ValueError异常
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # 捕获并处理其他异常
        raise HTTPException(status_code=500, detail=f"获取概念板块成份股失败: {str(e)}")


# 使用更具体的路径，避免与 /concept/{board_code} 冲突
@router.get("/concept/by-params/info", response_model=ConceptBoard)
async def get_concept_board_info(
    code: Optional[str] = Query(None, description="概念板块代码，如'BK0715'"),
    name: Optional[str] = Query(None, description="概念板块名称，如'可燃冰'"),
):
    """获取概念板块基本信息"""
    if not code and not name:
        raise HTTPException(status_code=400, detail="必须提供板块代码或板块名称")

    # 使用一个默认的板块代码，当通过名称查找时会被覆盖
    board_code = code if code else "default"

    result = await sector_service.get_concept_board(board_code, name)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"未找到概念板块: {'代码=' + code if code else '名称=' + name}",
        )

    return result


@router.get("/concept/{board_code}", response_model=ConceptBoard)
async def get_concept_board(board_code: str):
    """获取单个概念板块的实时行情"""
    try:
        result = await sector_service.get_concept_board(board_code)
        if result is None:
            raise HTTPException(
                status_code=404, detail=f"未找到板块代码 {board_code} 的数据"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取概念板块失败: {str(e)}")


@router.get("/concept/{board_code}/spot", response_model=ConceptBoardSpot)
async def get_concept_board_spot_by_code(board_code: str):
    """获取概念板块实时行情详情（通过代码）"""
    try:
        result = await sector_service.get_concept_board_spot_by_code(board_code)
        if result is None:
            raise HTTPException(
                status_code=404, detail=f"未找到板块代码 {board_code} 的实时行情数据"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"获取概念板块实时行情详情失败: {str(e)}"
        )


@router.get(
    "/concept/{board_code}/constituents", response_model=List[ConceptBoardConstituent]
)
async def get_concept_board_constituents_by_code(board_code: str):
    """通过板块代码获取概念板块成份股"""
    try:
        return await sector_service.get_concept_board_constituents(board_code)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"获取概念板块成份股失败: {str(e)}")


@router.get("/industry", response_model=List[IndustryBoard])
async def get_industry_boards():
    """获取行业板块列表及实时行情（优先 AKShare，失败时降级到 Tushare）"""
    try:
        return await sector_service.get_industry_boards()
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"获取行业板块列表失败: {str(e)}")


# 使用更具体的路径，避免与 /industry/{board_code} 冲突
@router.get("/industry/by-name/spot", response_model=IndustryBoardSpot)
async def get_industry_board_spot(
    board_name: str = Query(..., description="板块名称，如'银行'"),
):
    """获取行业板块实时行情详情"""
    try:
        result = await sector_service.get_industry_board_spot(board_name)
        if not result:
            raise HTTPException(
                status_code=404, detail=f"未找到板块 {board_name} 的实时行情数据"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"获取行业板块实时行情详情失败: {str(e)}"
        )


# 使用更具体的路径，避免与 /industry/{board_code} 冲突
@router.get(
    "/industry/by-symbol/constituents", response_model=List[IndustryBoardConstituent]
)
async def get_industry_board_constituents(
    symbol: str = Query(..., description="板块名称或代码，如'小金属'或'BK1027'"),
):
    """获取行业板块成份股"""
    try:
        return await sector_service.get_industry_board_constituents(symbol)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"获取行业板块成份股失败: {str(e)}")


@router.get("/industry/{board_code}", response_model=IndustryBoard)
async def get_industry_board(board_code: str):
    """获取单个行业板块的实时行情"""
    try:
        result = await sector_service.get_industry_board(board_code)
        if result is None:
            raise HTTPException(
                status_code=404, detail=f"未找到板块代码 {board_code} 的数据"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行业板块失败: {str(e)}")


@router.get("/industry/{board_code}/spot", response_model=IndustryBoardSpot)
async def get_industry_board_spot_by_code(board_code: str):
    """获取行业板块实时行情详情（通过代码）"""
    try:
        result = await sector_service.get_industry_board_spot_by_code(board_code)
        if result is None:
            raise HTTPException(
                status_code=404, detail=f"未找到板块代码 {board_code} 的实时行情数据"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"获取行业板块实时行情详情失败: {str(e)}"
        )


@router.get(
    "/industry/{board_code}/constituents", response_model=List[IndustryBoardConstituent]
)
async def get_industry_board_constituents_by_code(board_code: str):
    """通过板块代码获取行业板块成份股"""
    try:
        return await sector_service.get_industry_board_constituents(board_code)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"获取行业板块成份股失败: {str(e)}")


# ============ 板块轮动增强接口 ============


@router.get("/leaders", response_model=List[SectorLeader])
async def get_sector_leaders(
    sector_type: str = Query("industry", description="板块类型: industry 或 concept"),
    limit: int = Query(50, description="返回数量限制"),
):
    """获取板块龙头股排行"""
    try:
        return await sector_service.get_sector_leaders(sector_type, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取板块龙头股排行失败: {str(e)}")


@router.get("/industry/{board_code}/leader", response_model=SectorLeader)
async def get_industry_sector_leader(board_code: str):
    """获取行业板块龙头股"""
    try:
        result = await sector_service.get_sector_leader_by_code(board_code, "industry")
        if not result:
            raise HTTPException(
                status_code=404, detail=f"未找到板块代码 {board_code} 的龙头股数据"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行业板块龙头股失败: {str(e)}")


@router.get("/concept/{board_code}/leader", response_model=SectorLeader)
async def get_concept_sector_leader(board_code: str):
    """获取概念板块龙头股"""
    try:
        result = await sector_service.get_sector_leader_by_code(board_code, "concept")
        if not result:
            raise HTTPException(
                status_code=404, detail=f"未找到板块代码 {board_code} 的龙头股数据"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取概念板块龙头股失败: {str(e)}")


@router.get("/realtime", response_model=List[SectorRealtimeStatus])
async def get_sector_realtime(
    sector_type: str = Query("industry", description="板块类型: industry 或 concept"),
):
    """获取板块实时状态（用于监控）"""
    try:
        return await sector_service.get_sector_realtime_status(sector_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取板块实时状态失败: {str(e)}")


@router.get(
    "/rotation/history/{board_code}", response_model=List[SectorRotationHistory]
)
async def get_sector_rotation_history(
    board_code: str,
    sector_type: str = Query("industry", description="板块类型: industry 或 concept"),
    start_date: Optional[str] = Query(None, description="开始日期 YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYYMMDD"),
):
    """获取板块历史行情数据"""
    try:
        return await sector_service.get_sector_rotation_history(
            board_code, sector_type, start_date, end_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取板块历史行情失败: {str(e)}")


@router.get("/factors", response_model=List[SectorFactor])
async def get_sector_factors(
    sector_type: str = Query("industry", description="板块类型: industry 或 concept"),
    limit: int = Query(30, description="返回数量限制"),
):
    """获取板块多因子数据"""
    try:
        return await sector_service.get_sector_factors(sector_type, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取板块多因子数据失败: {str(e)}")


@router.get("/rotation/predict", response_model=RotationPrediction)
async def predict_sector_rotation(
    sector_type: str = Query("industry", description="板块类型: industry 或 concept"),
):
    """预测板块轮动"""
    try:
        return await sector_service.predict_rotation(sector_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预测板块轮动失败: {str(e)}")
