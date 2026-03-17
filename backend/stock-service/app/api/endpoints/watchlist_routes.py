# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : watchlist_routes.py
# @IDE            : PyCharm
# @desc           : 自选股管理API路由

from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional

from app.services.watchlist_service import watchlist_service

router = APIRouter()


@router.post("/stocks", summary="添加自选股")
async def add_stock(
    stock_code: str = Body(..., description="股票代码"),
    stock_name: str = Body(..., description="股票名称"),
    group: str = Body("default", description="分组名称"),
    notes: str = Body("", description="备注"),
    tags: List[str] = Body([], description="标签列表"),
):
    """添加股票到自选股列表"""
    try:
        result = await watchlist_service.add_stock(
            stock_code, stock_name, group, notes, tags
        )
        return {"success": True, "data": result.__dict__}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/stocks/{stock_code}", summary="删除自选股")
async def remove_stock(stock_code: str):
    """从自选股列表删除股票"""
    try:
        success = await watchlist_service.remove_stock(stock_code)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stocks", summary="获取所有自选股")
async def get_all_stocks():
    """获取所有自选股列表"""
    try:
        result = await watchlist_service.get_all_stocks()
        return {"data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stocks/group/{group}", summary="按分组获取自选股")
async def get_stocks_by_group(group: str):
    """获取指定分组的自选股"""
    try:
        result = await watchlist_service.get_stocks_by_group(group)
        return {
            "group": group,
            "data": [r.__dict__ for r in result],
            "count": len(result),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/groups", summary="创建分组")
async def create_group(name: str = Body(..., embed=True, description="分组名称")):
    """创建新的自选股分组"""
    try:
        result = await watchlist_service.create_group(name)
        return {"success": True, "data": result.__dict__}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/groups/{name}", summary="删除分组")
async def delete_group(name: str):
    """删除自选股分组"""
    try:
        success = await watchlist_service.delete_group(name)
        return {"success": success}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/groups", summary="获取所有分组")
async def get_all_groups():
    """获取所有自选股分组"""
    try:
        result = await watchlist_service.get_all_groups()
        return {"data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/stocks/{stock_code}/move", summary="移动股票到分组")
async def move_stock(
    stock_code: str, group: str = Body(..., embed=True, description="目标分组")
):
    """将股票移动到指定分组"""
    try:
        success = await watchlist_service.move_stock(stock_code, group)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/stocks/{stock_code}/notes", summary="更新备注")
async def update_notes(
    stock_code: str, notes: str = Body(..., embed=True, description="备注内容")
):
    """更新股票备注"""
    try:
        success = await watchlist_service.update_notes(stock_code, notes)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stocks/{stock_code}/tags", summary="添加标签")
async def add_tag(
    stock_code: str, tag: str = Body(..., embed=True, description="标签")
):
    """为股票添加标签"""
    try:
        success = await watchlist_service.add_tag(stock_code, tag)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/stocks/{stock_code}/tags/{tag}", summary="删除标签")
async def remove_tag(stock_code: str, tag: str):
    """删除股票标签"""
    try:
        success = await watchlist_service.remove_tag(stock_code, tag)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tags/{tag}", summary="按标签搜索")
async def search_by_tag(tag: str):
    """按标签搜索自选股"""
    try:
        result = await watchlist_service.search_by_tag(tag)
        return {"tag": tag, "data": [r.__dict__ for r in result], "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
