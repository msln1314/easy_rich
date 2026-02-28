# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_monitor_condition.py
# @IDE            : PyCharm
# @desc           : 股票监控配置接口文件

from fastapi import APIRouter, Depends, Body
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, Auth
from .params import StockMonitorConditionParams
from . import schemas, crud
from core.dependencies import IdList


router = APIRouter()


###########################################################
#    股票监控配置管理
###########################################################


@router.post("", summary="创建股票监控配置")
async def create_monitor_condition(data: schemas.StockMonitorConditionCreate, auth: Auth = Depends(AllUserAuth())):
    """
    创建股票监控配置
    """
    condition = await crud.StockMonitorConditionDal(auth.db).create_data(data=data)
    return SuccessResponse(condition)


@router.get("", summary="获取股票监控配置列表，分页")
async def get_monitor_condition_list(params: StockMonitorConditionParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    """
    获取股票监控配置列表
    普通用户只能看到自己的数据，管理员可以看到所有数据
    """
    condition_dict = params.dict()
    
    # 如果不是管理员（is_staff），只能看到自己的数据
    if not auth.user.is_staff and condition_dict.get('user_id') is None:
        condition_dict['user_id'] = auth.user.id
    
    schema = schemas.StockMonitorConditionOut
    datas, count = await crud.StockMonitorConditionDal(auth.db).get_datas(
        **condition_dict,
        v_schema=schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@router.post("/export/excel", summary="导出股票监控配置为excel")
async def export_query_list(
        header: list = Body(..., title="表头与对应字段"),
        params: StockMonitorConditionParams = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["stock_monitor_condition.export"]))
):
    """
    导出股票监控配置为excel
    """
    return SuccessResponse(await crud.StockMonitorConditionDal(auth.db).export_query_list(header, params))


@router.delete("", summary="批量删除股票监控配置", description="硬删除")
async def delete_monitor_condition(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    """
    批量删除股票监控配置
    普通用户只能删除自己的数据
    """
    # 如果不是管理员，检查是否只删除自己的数据
    if not auth.user.is_staff:
        for data_id in ids.ids:
            data = await crud.StockMonitorConditionDal(auth.db).get_data(data_id)
            if data.user_id != auth.user.id:
                return SuccessResponse("无权限删除其他用户的数据")

    await crud.StockMonitorConditionDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.get("/options", summary="获取启用的监控条件列表")
async def get_active_conditions(user_id: int | None = None, auth: Auth = Depends(AllUserAuth())):
    """
    获取启用的监控条件列表
    普通用户只能看到自己的数据，管理员可以看到所有数据
    :param user_id: 用户ID，可选，不传则根据用户权限决定
    """
    # 如果不是管理员（is_staff），只能看到自己的数据
    if not auth.user.is_staff:
        user_id = auth.user.id
    datas = await crud.StockMonitorConditionDal(auth.db).get_active_conditions(user_id)
    return SuccessResponse(datas)


@router.get("/{data_id}", summary="获取股票监控配置详情")
async def get_monitor_condition_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    """
    获取股票监控配置详情
    普通用户只能查看自己的数据
    """
    data = await crud.StockMonitorConditionDal(auth.db).get_data(data_id)
    # 如果不是管理员，检查是否是自己的数据
    if not auth.user.is_staff and data.user_id != auth.user.id:
        return SuccessResponse(None)
    return SuccessResponse(data)


@router.put("/{data_id}", summary="更新股票监控配置")
async def put_monitor_condition(data_id: int, data: schemas.StockMonitorConditionUpdate, auth: Auth = Depends(AllUserAuth())):
    """
    更新股票监控配置
    普通用户只能更新自己的数据
    """
    # 检查权限
    existing_data = await crud.StockMonitorConditionDal(auth.db).get_data(data_id)
    if not auth.user.is_staff and existing_data.user_id != auth.user.id:
        return SuccessResponse(None)
    condition = await crud.StockMonitorConditionDal(auth.db).put_data(data_id, data)
    return SuccessResponse(condition)


@router.put("/{data_id}/active", summary="更新监控条件的启用状态")
async def update_active_status(data_id: int, is_active: int = Body(..., embed=True), auth: Auth = Depends(AllUserAuth())):
    """
    更新监控条件的启用状态
    普通用户只能更新自己的数据
    :param data_id: 条件ID
    :param is_active: 是否启用：1启用 0禁用
    """
    # 检查权限
    existing_data = await crud.StockMonitorConditionDal(auth.db).get_data(data_id)
    if not auth.user.is_staff and existing_data.user_id != auth.user.id:
        return SuccessResponse("无权限操作")
    await crud.StockMonitorConditionDal(auth.db).update_active_status(data_id, is_active)
    return SuccessResponse("更新成功")
