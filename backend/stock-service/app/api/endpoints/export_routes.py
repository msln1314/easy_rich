# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : export_routes.py
# @IDE            : PyCharm
# @desc           : 数据导出API路由

from fastapi import APIRouter, Query, HTTPException, Body
from fastapi.responses import Response
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.services.export_service import export_service

router = APIRouter()


@router.get("/stock-list", summary="导出股票列表")
async def export_stock_list(
    format: str = Query("excel", description="导出格式: excel/csv/json"),
):
    """导出全部A股股票列表"""
    try:
        data = await export_service.export_stock_list(format)
        filename = f"stock_list_{datetime.now().strftime('%Y%m%d')}{export_service.get_file_extension(format)}"
        return Response(
            content=data,
            media_type=export_service.get_content_type(format),
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock-history/{stock_code}", summary="导出股票历史数据")
async def export_stock_history(
    stock_code: str,
    period: str = Query("daily", description="周期: daily/weekly/monthly"),
    start_date: Optional[str] = Query(None, description="开始日期YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期YYYYMMDD"),
    format: str = Query("excel", description="导出格式: excel/csv/json"),
):
    """导出指定股票的历史K线数据"""
    try:
        data = await export_service.export_stock_history(
            stock_code, period, start_date, end_date, format
        )
        filename = f"{stock_code}_history_{datetime.now().strftime('%Y%m%d')}{export_service.get_file_extension(format)}"
        return Response(
            content=data,
            media_type=export_service.get_content_type(format),
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/custom", summary="导出自定义数据")
async def export_custom_data(
    data: List[Dict[str, Any]] = Body(..., description="要导出的数据"),
    format: str = Query("excel", description="导出格式: excel/csv/json"),
):
    """导出自定义JSON数据"""
    try:
        export_data = await export_service.export_custom_data(data, format)
        filename = f"custom_export_{datetime.now().strftime('%Y%m%d%H%M%S')}{export_service.get_file_extension(format)}"
        return Response(
            content=export_data,
            media_type=export_service.get_content_type(format),
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
