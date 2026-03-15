# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_watchlist.py
# @IDE            : PyCharm
# @desc           : 股票关注列表接口文件

from fastapi import APIRouter, Depends, Body
from sqlalchemy import func
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, Auth
from .params import StockWatchlistParams
from . import schemas, crud
from core.dependencies import IdList


router = APIRouter()


###########################################################
#    股票关注列表管理
###########################################################


@router.post("", summary="创建股票关注")
async def create_watchlist(data: schemas.StockWatchlistCreate, auth: Auth = Depends(AllUserAuth())):
    """
    创建股票关注
    """
    watchlist = await crud.StockWatchlistDal(auth.db).create_data(data=data)
    return SuccessResponse(watchlist)


@router.get("", summary="获取股票关注列表，分页")
async def get_watchlist_list(params: StockWatchlistParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    """
    获取股票关注列表
    """
    watchlist_dict = params.dict()
    schema = schemas.StockWatchlistOut

    # 处理日期范围过滤
    v_where = []
    start_date = watchlist_dict.pop('start_date', None)
    end_date = watchlist_dict.pop('end_date', None)

    dal = crud.StockWatchlistDal(auth.db)
    if start_date:
        v_where.append(func.date(dal.model.date_at) >= start_date)
    if end_date:
        v_where.append(func.date(dal.model.date_at) <= end_date)

    datas, count = await dal.get_datas(
        **watchlist_dict,
        v_schema=schema,
        v_return_count=True,
        v_where=v_where if v_where else None
    )
    return SuccessResponse(datas, count=count)


@router.post("/export/excel", summary="导出股票关注列表为excel")
async def export_query_list(
        header: list = Body(..., title="表头与对应字段"),
        params: StockWatchlistParams = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["stock_watchlist.export"]))
):
    """
    导出股票关注列表为excel
    """
    return SuccessResponse(await crud.StockWatchlistDal(auth.db).export_query_list(header, params))


@router.delete("", summary="批量删除股票关注", description="硬删除")
async def delete_watchlist(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    """
    批量删除股票关注
    """
    await crud.StockWatchlistDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新股票关注")
async def put_watchlist(data_id: int, data: schemas.StockWatchlistUpdate, auth: Auth = Depends(AllUserAuth())):
    """
    更新股票关注
    """
    watchlist = await crud.StockWatchlistDal(auth.db).put_data(data_id, data)
    return SuccessResponse(watchlist)


@router.get("/{data_id}", summary="获取股票关注详情")
async def get_watchlist_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    """
    获取股票关注详情
    """
    data = await crud.StockWatchlistDal(auth.db).get_data(data_id)
    return SuccessResponse(data)


@router.get("/user/{user_id}", summary="根据用户ID获取关注列表")
async def get_watchlist_by_user(user_id: int, is_active: int = 1, auth: Auth = Depends(AllUserAuth())):
    """
    根据用户ID获取关注列表
    :param user_id: 用户ID
    :param is_active: 是否关注中，默认1（关注中）
    """
    datas = await crud.StockWatchlistDal(auth.db).get_by_user_id(user_id, is_active)
    return SuccessResponse(datas)


@router.get("/user/{user_id}/stock/{stock_code}", summary="根据用户ID和股票代码获取关注记录")
async def get_watchlist_by_user_and_stock(user_id: int, stock_code: str, auth: Auth = Depends(AllUserAuth())):
    """
    根据用户ID和股票代码获取关注记录
    :param user_id: 用户ID
    :param stock_code: 股票代码
    """
    data = await crud.StockWatchlistDal(auth.db).get_by_user_and_stock(user_id, stock_code)
    return SuccessResponse(data)


@router.put("/cancel", summary="取消关注")
async def cancel_follow(user_id: int = Body(..., embed=True), stock_code: str = Body(..., embed=True), auth: Auth = Depends(AllUserAuth())):
    """
    取消关注
    :param user_id: 用户ID
    :param stock_code: 股票代码
    """
    await crud.StockWatchlistDal(auth.db).cancel_follow(user_id, stock_code)
    return SuccessResponse("取消关注成功")


@router.put("/{data_id}/stats", summary="更新关注统计数据")
async def update_watch_stats(data_id: int, stats_data: dict = Body(...), auth: Auth = Depends(AllUserAuth())):
    """
    更新关注统计数据
    :param data_id: 记录ID
    :param stats_data: 统计数据
    """
    await crud.StockWatchlistDal(auth.db).update_watch_stats(data_id, stats_data)
    return SuccessResponse("更新成功")


@router.get("/active/{user_id}", summary="获取用户的所有活跃关注记录")
async def get_active_watchlist(user_id: int, auth: Auth = Depends(AllUserAuth())):
    """
    获取用户的所有活跃关注记录
    :param user_id: 用户ID
    """
    datas = await crud.StockWatchlistDal(auth.db).get_active_watchlist_by_user(user_id)
    return SuccessResponse(datas)


@router.get("/tags/list", summary="获取所有标签列表")
async def get_tags_list(auth: Auth = Depends(AllUserAuth())):
    """
    获取所有标签列表
    """
    tags = await crud.StockWatchlistDal(auth.db).get_all_tags()
    return SuccessResponse(tags)
