# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/08
# @File           : stock_group.py
# @IDE            : PyCharm
# @desc           : 股票分组接口文件

from fastapi import APIRouter, Depends, Body, Query
from utils.response import SuccessResponse, ErrorResponse
from apps.admin.auth.utils.current import AllUserAuth, Auth
from . import schemas, crud
from core.dependencies import IdList
from typing import List


router = APIRouter()


###########################################################
#    股票分组管理
###########################################################


@router.post("", summary="创建股票分组")
async def create_group(data: schemas.StockGroupCreate, auth: Auth = Depends(AllUserAuth())):
    """
    创建股票分组
    """
    # 检查分组名称是否已存在
    existing = await crud.StockGroupDal(auth.db).get_by_name(auth.user.id, data.name)
    if existing:
        return ErrorResponse(f"分组名称 '{data.name}' 已存在")

    # 从会话中获取 user_id
    data.user_id = auth.user.id
    group = await crud.StockGroupDal(auth.db).create_data(data=data, v_schema=schemas.StockGroupOut)
 
    return SuccessResponse(group)


@router.get("/tree", summary="获取用户分组树")
async def get_group_tree(auth: Auth = Depends(AllUserAuth())):
    """
    获取用户的分组树
    """
    tree = await crud.StockGroupDal(auth.db).get_tree_by_user_id(auth.user.id)
    return SuccessResponse(tree)


@router.get("/list", summary="获取用户分组列表")
async def get_group_list(auth: Auth = Depends(AllUserAuth())):
    """
    获取用户的分组列表
    """
    groups = await crud.StockGroupDal(auth.db).get_by_user_id(auth.user.id)
    return SuccessResponse(groups)


@router.get("", summary="获取分组详情")
async def get_group_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    """
    获取分组详情
    :param data_id: 分组ID
    """
    data = await crud.StockGroupDal(auth.db).get_data(data_id)
    return SuccessResponse(data)


@router.put("/{data_id}", summary="更新股票分组")
async def put_group(data_id: int, data: schemas.StockGroupUpdate, auth: Auth = Depends(AllUserAuth())):
    """
    更新股票分组
    :param data_id: 分组ID
    """
    group = await crud.StockGroupDal(auth.db).put_data(data_id, data)
    return SuccessResponse(group)


@router.delete("", summary="批量删除股票分组", description="软删除")
async def delete_groups(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    """
    批量删除股票分组
    """
    await crud.StockGroupDal(auth.db).delete_datas(ids.ids, v_soft=True)
    return SuccessResponse("删除成功")


@router.put("/{data_id}/status", summary="更新分组状态")
async def update_group_status(
    data_id: int,
    status: int = Body(..., embed=True, description="状态：0禁用 1启用"),
    auth: Auth = Depends(AllUserAuth())
):
    """
    更新分组状态
    :param data_id: 分组ID
    :param status: 状态
    """
    await crud.StockGroupDal(auth.db).update_status(data_id, status)
    return SuccessResponse("更新成功")
