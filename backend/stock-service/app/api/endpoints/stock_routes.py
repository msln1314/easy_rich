from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from app.models.stock_models import StockInfo, StockQuote, StockFinancial, StockFundFlow, StockHistory
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
        raise HTTPException(status_code=404, detail=f"获取个股融资融券信息失败: {str(e)}")

@router.get("/{stock_code}/history", response_model=List[StockHistory])
async def get_stock_history(
    stock_code: str,
    period: str = Query("daily", description="数据周期: daily(日线), weekly(周线), monthly(月线)"),
    start_date: Optional[str] = Query(None, description="开始日期，格式YYYYMMDD，如20210101"),
    end_date: Optional[str] = Query(None, description="结束日期，格式YYYYMMDD，如20210630")
):
    """获取个股历史行情数据"""
    try:
        result = await stock_service.get_stock_history(stock_code, period, start_date, end_date)
        if not result:
            raise HTTPException(status_code=404, detail=f"未找到股票代码 {stock_code} 的历史行情数据")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取个股历史行情数据失败: {str(e)}")