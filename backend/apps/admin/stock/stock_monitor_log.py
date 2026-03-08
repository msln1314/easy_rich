# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2025/02/15
# @File : stock_monitor_log.py
# @IDE : PyCharm
# @desc : 股票监听推送日志接口文件

from fastapi import APIRouter, Depends, Body, Query
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, Auth
from .params import StockMonitorLogParams
from . import schemas, crud
from core.dependencies import IdList
from datetime import datetime


router = APIRouter()


###########################################################
# 股票监听推送日志管理
###########################################################


@router.get("", summary="获取股票监听日志列表，分页")
async def get_monitor_log_list(
    params: StockMonitorLogParams = Depends(), auth: Auth = Depends(AllUserAuth())
):
    """获取股票监听日志列表
    普通用户只能看到自己的数据，管理员可以看到所有数据
    """
    params_dict = params.dict()

    if not auth.user.is_staff and params_dict.get("user_id") is None:
        params_dict["user_id"] = auth.user.id

    schema = schemas.StockMonitorLogOut
    datas, count = await crud.StockMonitorLogDal(auth.db).get_datas(
        **params_dict, v_schema=schema, v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@router.post("/export/excel", summary="导出股票监听日志为excel")
async def export_query_list(
    header: list = Body(..., title="表头与对应字段"),
    params: StockMonitorLogParams = Depends(),
    auth: Auth = Depends(FullAdminAuth(permissions=["stock_monitor_log.export"])),
):
    """导出股票监听日志为excel"""
    return SuccessResponse(
        await crud.StockMonitorLogDal(auth.db).export_query_list(header, params)
    )


@router.delete("", summary="批量删除股票监听日志", description="硬删除")
async def delete_monitor_log(
    ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())
):
    """批量删除股票监听日志
    普通用户只能删除自己的数据
    """
    if not auth.user.is_staff:
        for data_id in ids.ids:
            data = await crud.StockMonitorLogDal(auth.db).get_data(data_id)
            if data.user_id != auth.user.id:
                return SuccessResponse("无权限删除其他用户的数据")

    await crud.StockMonitorLogDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.get("/statistics", summary="获取日志统计信息")
async def get_statistics(
    user_id: int | None = None,
    days: int = Query(7, ge=1, le=365, title="统计天数"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取日志统计信息"""
    if not auth.user.is_staff:
        user_id = auth.user.id

    statistics = await crud.StockMonitorLogDal(auth.db).get_statistics(user_id, days)
    return SuccessResponse(statistics)


@router.get("/recent", summary="获取最近24小时日志")
async def get_recent_logs(
    hours: int = Query(24, ge=1, le=168, title="小时数"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取最近的日志"""
    if not auth.user.is_staff:
        user_id = auth.user.id
    else:
        user_id = None

    logs = await crud.StockMonitorLogDal(auth.db).get_recent_logs(user_id, hours)
    return SuccessResponse(logs)


@router.get("/by_strategy/{strategy_id}", summary="根据策略ID获取日志")
async def get_logs_by_strategy(
    strategy_id: int,
    limit: int = Query(100, ge=1, le=500, title="返回数量"),
    auth: Auth = Depends(AllUserAuth()),
):
    """根据策略ID获取日志"""
    logs = await crud.StockMonitorLogDal(auth.db).get_logs_by_strategy_id(
        strategy_id, limit
    )
    return SuccessResponse(logs)


@router.get("/by_stock/{stock_code}", summary="根据股票代码获取日志")
async def get_logs_by_stock(
    stock_code: str,
    limit: int = Query(100, ge=1, le=500, title="返回数量"),
    auth: Auth = Depends(AllUserAuth()),
):
    """根据股票代码获取日志"""
    logs = await crud.StockMonitorLogDal(auth.db).get_logs_by_stock_code(
        stock_code, limit
    )
    return SuccessResponse(logs)


@router.put("/{log_id}/notify_status", summary="更新推送状态")
async def update_notify_status(
    log_id: int,
    data: schemas.StockMonitorLogUpdate,
    auth: Auth = Depends(AllUserAuth()),
):
    """更新推送状态"""
    existing_data = await crud.StockMonitorLogDal(auth.db).get_data(log_id)
    if not auth.user.is_staff and existing_data.user_id != auth.user.id:
        return SuccessResponse("无权限操作")

    await crud.StockMonitorLogDal(auth.db).update_notify_status(
        log_id, data.notify_status, data.notify_result, data.error_message
    )
    return SuccessResponse("更新成功")


@router.delete("/old", summary="清理旧日志")
async def delete_old_logs(
    days: int = Query(30, ge=7, le=365, title="保留天数"),
    auth: Auth = Depends(FullAdminAuth(permissions=["stock_monitor_log.delete"])),
):
    """删除指定天数之前的日志"""
    count = await crud.StockMonitorLogDal(auth.db).delete_old_logs(days)
    return SuccessResponse(f"已删除 {count} 条旧日志")
