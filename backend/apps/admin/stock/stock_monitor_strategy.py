# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2025/02/15
# @File : stock_monitor_strategy.py
# @IDE : PyCharm
# @desc : 股票监听策略接口文件

from fastapi import APIRouter, Depends, Body
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, Auth
from .params import StockMonitorStrategyParams
from . import schemas, crud
from core.dependencies import IdList


router = APIRouter()


###########################################################
# 股票监听策略管理
###########################################################


@router.post("", summary="创建股票监听策略")
async def create_monitor_strategy(
    data: schemas.StockMonitorStrategyCreate, auth: Auth = Depends(AllUserAuth())
):
    """创建股票监听策略"""
    strategy = await crud.StockMonitorStrategyDal(auth.db).create_data(data=data)
    return SuccessResponse(strategy)


@router.get("", summary="获取股票监听策略列表，分页")
async def get_monitor_strategy_list(
    params: StockMonitorStrategyParams = Depends(), auth: Auth = Depends(AllUserAuth())
):
    """获取股票监听策略列表
    普通用户只能看到自己的数据，管理员可以看到所有数据
    """
    params_dict = params.dict()

    if not auth.user.is_staff and params_dict.get("user_id") is None:
        params_dict["user_id"] = auth.user.id

    schema = schemas.StockMonitorStrategyOut
    datas, count = await crud.StockMonitorStrategyDal(auth.db).get_datas(
        **params_dict, v_schema=schema, v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@router.post("/export/excel", summary="导出股票监听策略为excel")
async def export_query_list(
    header: list = Body(..., title="表头与对应字段"),
    params: StockMonitorStrategyParams = Depends(),
    auth: Auth = Depends(FullAdminAuth(permissions=["stock_monitor_strategy.export"])),
):
    """导出股票监听策略为excel"""
    return SuccessResponse(
        await crud.StockMonitorStrategyDal(auth.db).export_query_list(header, params)
    )


@router.delete("", summary="批量删除股票监听策略", description="硬删除")
async def delete_monitor_strategy(
    ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())
):
    """批量删除股票监听策略
    普通用户只能删除自己的数据
    """
    if not auth.user.is_staff:
        for data_id in ids.ids:
            data = await crud.StockMonitorStrategyDal(auth.db).get_data(data_id)
            if data.user_id != auth.user.id:
                return SuccessResponse("无权限删除其他用户的数据")

    await crud.StockMonitorStrategyDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.get("/options", summary="获取启用的监听策略列表")
async def get_active_strategies(
    user_id: int | None = None, auth: Auth = Depends(AllUserAuth())
):
    """获取启用的监听策略列表
    普通用户只能看到自己的数据，管理员可以看到所有数据
    """
    if not auth.user.is_staff:
        user_id = auth.user.id

    datas = await crud.StockMonitorStrategyDal(auth.db).get_active_strategies(user_id)
    return SuccessResponse(datas)


@router.get("/statistics", summary="获取策略统计信息")
async def get_statistics(
    user_id: int | None = None, auth: Auth = Depends(AllUserAuth())
):
    """获取策略统计信息"""
    if not auth.user.is_staff:
        user_id = auth.user.id

    statistics = await crud.StockMonitorStrategyDal(auth.db).get_statistics(user_id)
    return SuccessResponse(statistics)


@router.get("/by_stock/{stock_code}", summary="根据股票代码获取监听策略")
async def get_strategies_by_stock_code(
    stock_code: str, auth: Auth = Depends(AllUserAuth())
):
    """根据股票代码获取监听策略"""
    datas = await crud.StockMonitorStrategyDal(auth.db).get_by_stock_code(stock_code)
    return SuccessResponse(datas)


@router.get("/{data_id}", summary="获取股票监听策略详情")
async def get_monitor_strategy_detail(
    data_id: int, auth: Auth = Depends(AllUserAuth())
):
    """获取股票监听策略详情
    普通用户只能查看自己的数据
    """
    data = await crud.StockMonitorStrategyDal(auth.db).get_data(data_id)
    if not auth.user.is_staff and data.user_id != auth.user.id:
        return SuccessResponse(None)
    return SuccessResponse(data)


@router.put("/{data_id}", summary="更新股票监听策略")
async def put_monitor_strategy(
    data_id: int,
    data: schemas.StockMonitorStrategyUpdate,
    auth: Auth = Depends(AllUserAuth()),
):
    """更新股票监听策略
    普通用户只能更新自己的数据
    """
    existing_data = await crud.StockMonitorStrategyDal(auth.db).get_data(data_id)
    if not auth.user.is_staff and existing_data.user_id != auth.user.id:
        return SuccessResponse(None)

    strategy = await crud.StockMonitorStrategyDal(auth.db).put_data(data_id, data)
    return SuccessResponse(strategy)


@router.put("/{data_id}/active", summary="更新策略的启用状态")
async def update_active_status(
    data_id: int,
    is_active: int = Body(..., embed=True),
    auth: Auth = Depends(AllUserAuth()),
):
    """更新策略的启用状态
    普通用户只能更新自己的数据
    :param data_id: 策略ID
    :param is_active: 是否启用：1启用 0禁用
    """
    existing_data = await crud.StockMonitorStrategyDal(auth.db).get_data(data_id)
    if not auth.user.is_staff and existing_data.user_id != auth.user.id:
        return SuccessResponse("无权限操作")

    await crud.StockMonitorStrategyDal(auth.db).update_active_status(data_id, is_active)
    return SuccessResponse("更新成功")


@router.put("/{data_id}/priority", summary="更新策略的优先级")
async def update_priority(
    data_id: int,
    priority: int = Body(..., embed=True, ge=1, le=3),
    auth: Auth = Depends(AllUserAuth()),
):
    """更新策略的优先级
    普通用户只能更新自己的数据
    :param data_id: 策略ID
    :param priority: 优先级：1高 2中 3低
    """
    existing_data = await crud.StockMonitorStrategyDal(auth.db).get_data(data_id)
    if not auth.user.is_staff and existing_data.user_id != auth.user.id:
        return SuccessResponse("无权限操作")

    await crud.StockMonitorStrategyDal(auth.db).db.execute(
        update(crud.StockMonitorStrategyDal(auth.db).model)
        .where(crud.StockMonitorStrategyDal(auth.db).model.id == data_id)
        .values(priority=priority)
    )
    await crud.StockMonitorStrategyDal(auth.db).db.commit()
    return SuccessResponse("更新成功")
