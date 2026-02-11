# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/08
# @File           : my_stock.py
# @IDE            : PyCharm
# @desc           : 我的自选股接口文件

from fastapi import APIRouter, Depends, Body, Query
from utils.response import SuccessResponse, ErrorResponse
from apps.admin.auth.utils.current import AllUserAuth, Auth
from . import schemas, crud
from core.dependencies import IdList
from typing import List


router = APIRouter()


###########################################################
#    我的自选股管理
###########################################################


@router.get("", summary="获取我的自选股列表")
async def get_my_stocks(
    group_id: int | None = Query(None, description="分组ID"),
    auth: Auth = Depends(AllUserAuth())
):
    """
    获取我的自选股列表
    :param group_id: 分组ID（可选）
    """
    stocks = await crud.SysUserStockGroupDal(auth.db).get_my_stocks(auth.user.id, group_id)
    return SuccessResponse(stocks)


@router.post("", summary="添加股票到分组")
async def add_stock_to_group(
    data: schemas.SysUserStockGroupCreate,
    auth: Auth = Depends(AllUserAuth())
):
    """
    添加股票到分组
    :param data: 关联数据
    """
    await crud.SysUserStockGroupDal(auth.db).add_stock_to_group(auth.user.id, data.group_id, data.stock_id)
    return SuccessResponse("添加成功")


@router.post("/batch", summary="批量添加股票到分组")
async def batch_add_stocks_to_group(
    group_id: int = Body(..., description="分组ID"),
    stock_ids: List[int] = Body(..., description="股票ID列表"),
    auth: Auth = Depends(AllUserAuth())
):
    """
    批量添加股票到分组
    :param group_id: 分组ID
    :param stock_ids: 股票ID列表
    """

    await crud.SysUserStockGroupDal(auth.db).add_stocks_to_group(auth.user.id, group_id, stock_ids)
    return SuccessResponse(f"成功添加 {len(stock_ids)} 只股票到分组")


@router.delete("", summary="从分组中移除股票")
async def remove_stock_from_group(
    group_id: int | None = Body(None, description="分组ID（可选，不传则移除所有分组中的股票）"),
    stock_id: int | None = Body(None, description="股票ID（可选，不传则移除分组中的所有股票）"),
    auth: Auth = Depends(AllUserAuth())
):
    """
    从分组中移除股票
    :param group_id: 分组ID（可选）
    :param stock_id: 股票ID（可选）
    """
    await crud.SysUserStockGroupDal(auth.db).remove_stock_from_group(auth.user.id, group_id, stock_id)
    return SuccessResponse("移除成功")


@router.put("/move", summary="移动股票到其他分组")
async def move_stock_to_group(
    from_group_id: int = Body(..., embed=True, description="原分组ID"),
    to_group_id: int = Body(..., embed=True, description="目标分组ID"),
    stock_id: int = Body(..., embed=True, description="股票ID"),
    auth: Auth = Depends(AllUserAuth())
):
    """
    移动股票到其他分组
    :param from_group_id: 原分组ID
    :param to_group_id: 目标分组ID
    :param stock_id: 股票ID
    """
    await crud.SysUserStockGroupDal(auth.db).move_stock_to_group(auth.user.id, from_group_id, to_group_id, stock_id)
    return SuccessResponse("移动成功")


@router.get("/count", summary="获取各分组股票数量")
async def get_stock_count_by_group(
    auth: Auth = Depends(AllUserAuth())
):
    """
    获取各分组股票数量
    """
    counts = await crud.SysUserStockGroupDal(auth.db).get_stock_count_by_group(auth.user.id)
    return SuccessResponse(counts)
