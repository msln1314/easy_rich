# backend/qmt-service/app/api/endpoints/factor_routes.py
"""
因子库API路由
"""
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, Body

from app.services.factor_service import factor_service
from app.models.factor_models import (
    FactorDefinition,
    FactorDefinitionListResponse,
    FactorValueListResponse,
    StockFactorValuesResponse,
    FactorICListResponse,
    FactorReturnListResponse,
    FactorScreenRequest,
    FactorScreenResponse,
    FactorCategory,
)

router = APIRouter()


@router.get("/definitions", response_model=FactorDefinitionListResponse, summary="获取因子定义列表")
async def get_factor_definitions(
    category: Optional[str] = Query(None, description="因子分类"),
    keyword: Optional[str] = Query(None, description="搜索关键词")
):
    """
    获取因子定义列表

    - **category**: 因子分类 (trend/momentum/volatility/volume/value/growth/quality/sentiment/custom)
    - **keyword**: 搜索关键词（因子名称、ID、描述）
    """
    return await factor_service.get_factor_definitions(category, keyword)


@router.get("/definitions/{factor_id}", response_model=FactorDefinition, summary="获取单个因子定义")
async def get_factor_definition(factor_id: str):
    """
    获取单个因子定义详情

    - **factor_id**: 因子ID
    """
    factor = await factor_service.get_factor_definition(factor_id)
    if not factor:
        raise HTTPException(status_code=404, detail=f"因子 {factor_id} 不存在")
    return factor


@router.post("/definitions", response_model=FactorDefinition, summary="创建自定义因子")
async def create_factor_definition(
    factor_id: str = Body(..., description="因子ID"),
    factor_name: str = Body(..., description="因子名称"),
    category: str = Body("custom", description="因子分类"),
    description: Optional[str] = Body(None, description="因子描述"),
    formula: Optional[str] = Body(None, description="计算公式"),
    params: Optional[List[dict]] = Body(None, description="参数配置"),
    unit: Optional[str] = Body(None, description="单位"),
    data_source: Optional[str] = Body(None, description="数据来源"),
    update_freq: str = Body("daily", description="更新频率")
):
    """
    创建自定义因子

    - **factor_id**: 因子ID（唯一标识）
    - **factor_name**: 因子名称
    - **category**: 因子分类
    - **description**: 因子描述
    - **formula**: 计算公式
    - **params**: 参数配置
    - **unit**: 单位
    - **data_source**: 数据来源
    - **update_freq**: 更新频率
    """
    try:
        factor = await factor_service.create_factor({
            "factor_id": factor_id,
            "factor_name": factor_name,
            "category": category,
            "description": description,
            "formula": formula,
            "params": params,
            "unit": unit,
            "data_source": data_source,
            "update_freq": update_freq,
        })
        return factor
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/definitions/{factor_id}", response_model=FactorDefinition, summary="更新因子定义")
async def update_factor_definition(
    factor_id: str,
    factor_name: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    formula: Optional[str] = Body(None),
    params: Optional[List[dict]] = Body(None),
    unit: Optional[str] = Body(None),
    is_active: Optional[bool] = Body(None)
):
    """
    更新因子定义

    - **factor_id**: 因子ID
    """
    update_data = {}
    if factor_name is not None:
        update_data["factor_name"] = factor_name
    if description is not None:
        update_data["description"] = description
    if formula is not None:
        update_data["formula"] = formula
    if params is not None:
        update_data["params"] = params
    if unit is not None:
        update_data["unit"] = unit
    if is_active is not None:
        update_data["is_active"] = is_active

    factor = await factor_service.update_factor(factor_id, update_data)
    if not factor:
        raise HTTPException(status_code=404, detail=f"因子 {factor_id} 不存在")
    return factor


@router.delete("/definitions/{factor_id}", summary="删除因子")
async def delete_factor_definition(factor_id: str):
    """
    删除因子（仅限自定义因子）

    - **factor_id**: 因子ID
    """
    try:
        deleted = await factor_service.delete_factor(factor_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"因子 {factor_id} 不存在")
        return {"message": "删除成功", "factor_id": factor_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sync", summary="从QMT同步因子库")
async def sync_factors_from_qmt():
    """
    从QMT同步因子库到本地数据库

    同步QMT支持的常用因子，包括：
    - 估值因子：PE、PB、PS、PCF、PEG
    - 成长因子：营收增长率、利润增长率、EPS增长率
    - 质量因子：ROE、ROA、毛利率、净利率、资产负债率
    - 技术因子：MA5/10/20/60、EMA12/26
    - 动量因子：RSI、MACD、KDJ
    - 波动因子：ATR、布林带
    - 成交量因子：成交量、成交额、换手率
    """
    result = await factor_service.sync_from_qmt()
    return {
        "message": f"同步完成，新增 {result.get('synced', 0)} 个因子",
        "synced": result.get("synced", 0),
        "total": result.get("total", 0)
    }


@router.get("/values/{factor_id}", response_model=FactorValueListResponse, summary="获取因子值")
async def get_factor_values(
    factor_id: str,
    stock_codes: List[str] = Query(..., description="股票代码列表"),
    date: Optional[str] = Query(None, description="日期，格式: YYYYMMDD")
):
    """
    获取指定因子的股票因子值

    - **factor_id**: 因子ID
    - **stock_codes**: 股票代码列表
    - **date**: 日期，不传则返回最新数据
    """
    return await factor_service.get_factor_values(factor_id, stock_codes, date)


@router.get("/stock/{stock_code}", response_model=StockFactorValuesResponse, summary="获取股票因子值")
async def get_stock_factor_values(
    stock_code: str,
    factor_ids: Optional[List[str]] = Query(None, description="因子ID列表，为空则返回全部"),
    date: Optional[str] = Query(None, description="日期，格式: YYYYMMDD")
):
    """
    获取单只股票的多个因子值

    - **stock_code**: 股票代码
    - **factor_ids**: 因子ID列表，为空则返回全部因子
    - **date**: 日期，不传则返回最新数据
    """
    return await factor_service.get_stock_factor_values(stock_code, factor_ids, date)


@router.get("/ic/{factor_id}", response_model=FactorICListResponse, summary="获取因子IC")
async def get_factor_ic(
    factor_id: str,
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    period: int = Query(20, ge=1, le=250, description="计算周期")
):
    """
    获取因子IC值（Information Coefficient）

    - **factor_id**: 因子ID
    - **start_date**: 开始日期
    - **end_date**: 结束日期
    - **period**: 计算周期天数
    """
    return await factor_service.get_factor_ic(factor_id, start_date, end_date, period)


@router.get("/returns/{factor_id}", response_model=FactorReturnListResponse, summary="获取因子收益")
async def get_factor_returns(
    factor_id: str,
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期")
):
    """
    获取因子收益数据

    - **factor_id**: 因子ID
    - **start_date**: 开始日期
    - **end_date**: 结束日期
    """
    return await factor_service.get_factor_returns(factor_id, start_date, end_date)


@router.post("/screen", response_model=FactorScreenResponse, summary="因子选股")
async def screen_stocks(request: FactorScreenRequest):
    """
    基于因子条件筛选股票

    请求体示例:
    ```json
    {
        "factors": [
            {"factor_id": "PE", "op": "lt", "value": 20},
            {"factor_id": "ROE", "op": "gt", "value": 10}
        ],
        "date": "20240101",
        "limit": 100
    }
    ```

    支持的操作符:
    - gt: 大于
    - lt: 小于
    - ge: 大于等于
    - le: 小于等于
    - eq: 等于
    """
    return await factor_service.screen_stocks(request)


@router.get("/categories", summary="获取因子分类列表")
async def get_factor_categories():
    """获取所有因子分类"""
    return [
        {"key": "trend", "name": "趋势因子", "description": "均线、趋势类指标"},
        {"key": "momentum", "name": "动量因子", "description": "RSI、KDJ、动量等"},
        {"key": "volatility", "name": "波动因子", "description": "ATR、波动率等"},
        {"key": "volume", "name": "成交量因子", "description": "量比、换手率等"},
        {"key": "value", "name": "价值因子", "description": "PE、PB、PS等"},
        {"key": "growth", "name": "成长因子", "description": "营收增长、利润增长等"},
        {"key": "quality", "name": "质量因子", "description": "ROE、ROA、毛利率等"},
        {"key": "sentiment", "name": "情绪因子", "description": "成交额、振幅等"},
        {"key": "custom", "name": "自定义因子", "description": "用户自定义因子"},
    ]