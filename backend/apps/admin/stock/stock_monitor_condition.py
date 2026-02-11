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
    """
    condition_dict = params.dict()
    datas, count = await crud.StockMonitorConditionDal(auth.db).get_datas(
        **condition_dict,
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
    params.limit = 1000000
    condition_dict = params.dict()
    datas = await crud.StockMonitorConditionDal(auth.db).get_datas(
        **condition_dict,
        v_return_count=False
    )
    return SuccessResponse(await crud.StockMonitorConditionDal(auth.db).export_xlsx(header, datas))


@router.delete("", summary="批量删除股票监控配置", description="硬删除")
async def delete_monitor_condition(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    """
    批量删除股票监控配置
    """
    await crud.StockMonitorConditionDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新股票监控配置")
async def put_monitor_condition(data_id: int, data: schemas.StockMonitorConditionUpdate, auth: Auth = Depends(AllUserAuth())):
    """
    更新股票监控配置
    """
    condition = await crud.StockMonitorConditionDal(auth.db).put_data(data_id, data)
    return SuccessResponse(condition)


@router.get("/{data_id}", summary="获取股票监控配置详情")
async def get_monitor_condition_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    """
    获取股票监控配置详情
    """
    data = await crud.StockMonitorConditionDal(auth.db).get_data(data_id)
    return SuccessResponse(data)


@router.get("/active", summary="获取启用的监控条件")
async def get_active_conditions(user_id: int | None = None, auth: Auth = Depends(AllUserAuth())):
    """
    获取启用的监控条件
    :param user_id: 用户ID，可选，不传则获取所有用户的
    """
    datas = await crud.StockMonitorConditionDal(auth.db).get_active_conditions(user_id)
    return SuccessResponse(datas)


@router.put("/{condition_id}/active", summary="更新监控条件的启用状态")
async def update_active_status(condition_id: int, is_active: int = Body(..., embed=True), auth: Auth = Depends(AllUserAuth())):
    """
    更新监控条件的启用状态
    :param condition_id: 条件ID
    :param is_active: 是否启用：1启用 0禁用
    """
    await crud.StockMonitorConditionDal(auth.db).update_active_status(condition_id, is_active)
    return SuccessResponse("更新成功")


@router.get("/user/{user_id}", summary="根据用户ID获取监控条件列表")
async def get_conditions_by_user(user_id: int, auth: Auth = Depends(AllUserAuth())):
    """
    根据用户ID获取监控条件列表
    :param user_id: 用户ID
    """
    datas = await crud.StockMonitorConditionDal(auth.db).get_by_user_id(user_id)
    return SuccessResponse(datas)
