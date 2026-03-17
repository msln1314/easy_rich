from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from app.models.stock_models import (
    StockInfo,
    StockQuote,
    StockFinancial,
    StockFundFlow,
    StockHistory,
)
from app.services.stock_service import StockService

router = APIRouter()
stock_service = StockService()


@router.get("/list", response_model=List[dict])
async def get_all_stock_list():
    """获取所有A股股票列表"""
    try:
        return await stock_service.get_all_stock_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票列表失败: {str(e)}")


@router.get("/{stock_code}/info", response_model=StockInfo)
async def get_stock_info(stock_code: str):
    """获取个股基本信息"""
    try:
        return await stock_service.get_stock_info(stock_code)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"获取个股信息失败: {str(e)}")


@router.get("/{stock_code}/quote", response_model=StockQuote)
async def get_stock_quote(stock_code: str):
    """获取个股实时行情"""
    try:
        return await stock_service.get_stock_quote(stock_code)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"获取个股行情失败: {str(e)}")


@router.get("/{stock_code}/financial", response_model=StockFinancial)
async def get_stock_financial(stock_code: str):
    """获取个股财务信息"""
    try:
        return await stock_service.get_stock_financial(stock_code)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"获取个股财务信息失败: {str(e)}")


@router.get("/{stock_code}/fund-flow", response_model=StockFundFlow)
async def get_stock_fund_flow(stock_code: str):
    """获取个股资金流向"""
    try:
        return await stock_service.get_stock_fund_flow(stock_code)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"获取个股资金流向失败: {str(e)}")


@router.get("/{stock_code}/margin", response_model=dict)
async def get_stock_margin(stock_code: str):
    """获取个股融资融券信息"""
    try:
        return await stock_service.get_stock_margin(stock_code)
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"获取个股融资融券信息失败: {str(e)}"
        )


@router.get("/{stock_code}/history", response_model=List[StockHistory])
async def get_stock_history(
    stock_code: str,
    period: str = Query(
        "daily", description="数据周期: daily(日线), weekly(周线), monthly(月线)"
    ),
    start_date: Optional[str] = Query(
        None, description="开始日期，格式YYYYMMDD，如20210101"
    ),
    end_date: Optional[str] = Query(
        None, description="结束日期，格式YYYYMMDD，如20210630"
    ),
):
    """获取个股历史行情数据"""
    try:
        result = await stock_service.get_stock_history(
            stock_code, period, start_date, end_date
        )
        if not result:
            raise HTTPException(
                status_code=404, detail=f"未找到股票代码 {stock_code} 的历史行情数据"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"获取个股历史行情数据失败: {str(e)}"
        )


# ========== 扩展接口 ==========


@router.get("/{stock_code}/minute", summary="获取分时数据")
async def get_minute_data(
    stock_code: str,
    period: str = Query("1", description="分钟周期: 1/5/15/30/60"),
    adjust: str = Query("", description="复权类型: qfq(前复权)/hfq(后复权)/空(不复权)"),
):
    """获取分时K线数据"""
    try:
        result = await stock_service.get_minute_data(stock_code, period, adjust)
        return {
            "stock_code": stock_code,
            "period": period,
            "data": result,
            "count": len(result),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}/quote-detail", summary="获取五档买卖盘")
async def get_quote_detail(stock_code: str):
    """获取五档买卖盘详情"""
    try:
        result = await stock_service.get_quote_detail(stock_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}/sectors", summary="获取所属板块")
async def get_stock_sectors(stock_code: str):
    """获取股票所属行业和概念板块"""
    try:
        result = await stock_service.get_stock_sectors(stock_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}/suspend", summary="获取停复牌信息")
async def get_suspend_info(stock_code: str):
    """获取股票停复牌状态"""
    try:
        result = await stock_service.get_suspend_info(stock_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}/notices", summary="获取股票公告")
async def get_stock_notices(
    stock_code: str, page: int = Query(1, ge=1, description="页码")
):
    """获取股票公告列表"""
    try:
        result = await stock_service.get_stock_notices(stock_code, page)
        return {"stock_code": stock_code, "data": result, "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}/pledge", summary="获取股权质押")
async def get_share_pledge(stock_code: str):
    """获取股权质押数据"""
    try:
        result = await stock_service.get_share_pledge(stock_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}/unlock", summary="获取限售解禁")
async def get_unlock_schedule(stock_code: str):
    """获取限售解禁计划"""
    try:
        result = await stock_service.get_unlock_schedule(stock_code)
        return {"stock_code": stock_code, "data": result, "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}/adjust-factor", summary="获取复权因子")
async def get_adjust_factor(stock_code: str):
    """获取复权因子"""
    try:
        result = await stock_service.get_adjust_factor(stock_code)
        return {"stock_code": stock_code, "data": result, "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", summary="搜索股票")
async def search_stock(
    keyword: str = Query(..., description="搜索关键词(股票代码或名称)"),
    limit: int = Query(20, ge=1, le=100, description="返回数量"),
):
    """搜索股票"""
    try:
        result = await stock_service.search_stock(keyword, limit)
        return {"keyword": keyword, "data": result, "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}/rating", summary="获取股票评级")
async def get_stock_rating(stock_code: str):
    """获取机构评级"""
    try:
        result = await stock_service.get_stock_rating(stock_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}/report", summary="获取研报")
async def get_stock_report(stock_code: str):
    """获取研报列表"""
    try:
        result = await stock_service.get_stock_report(stock_code)
        return {"stock_code": stock_code, "data": result, "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}/realtime", summary="获取实时行情(快速)")
async def get_realtime_quote(stock_code: str):
    """获取实时行情(新浪接口，响应更快)"""
    try:
        result = await stock_service.get_realtime_quote(stock_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
