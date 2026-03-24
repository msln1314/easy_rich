# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : stock_base_info.py
# @IDE            : PyCharm
# @desc           : 股票基本信息接口文件
from asyncio import Server

from core.logger import logger
from fastapi import APIRouter, Depends, Body, Request, Query
from utils.response import ErrorResponse, SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, Auth, OpenAuth
from .params import StockBaseInfoParams, StockParams, HistoricalParams
from . import schemas, crud
from .models import StockBasicInfo
from core.dependencies import IdList
from core.exception import CustomException
from services.stock_service import StockService
from datetime import datetime

router = APIRouter()


###########################################################
#    股票基本信息管理
###########################################################


# @router.get("/syncak", summary="从akshare同步股票基本信息")
# async def sync_stock_from_akshare(auth: Auth = Depends(OpenAuth())):
#     """
#     从akshare同步股票基本信息
#     """
#     dal = crud.StockBaseInfoDal(auth.db)
#     result = await dal.sync_from_akshare()
#     # auth.db.commit()
#     return SuccessResponse(result)


@router.post("", summary="创建股票基本信息")
async def create_stock(
    data: schemas.StockBaseInfoCreate, auth: Auth = Depends(AllUserAuth())
):
    stock = await crud.StockBaseInfoDal(auth.db).create_data(data=data)
    return SuccessResponse(stock)


@router.get("/info", summary="获取股票基本信息")
async def get_stock_info(
    stock_code: str = Query(..., description="股票代码"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取单个股票基本信息（包含字段描述）"""

    service = StockService()
    result = await service.get_stock_info(stock_code)

    if not result:
        return ErrorResponse(f"未找到股票 {stock_code} 的基本信息")
    return SuccessResponse(result)


@router.get("/history", summary="获取股票历史数据")
async def get_history_data(
    stock_code: str = Query(..., description="股票代码"),
    start_date: str | None = Query(None, description="开始日期"),
    end_date: str | None = Query(None, description="结束日期"),
    auth: Auth = Depends(AllUserAuth()),
):
    """获取单个股票历史数据（包含字段描述）"""

    # 处理日期范围
    start_date = start_date or "2024-01-01"
    end_date = end_date or datetime.now().strftime("%Y-%m-%d")
    service = StockService()
    result = await service.get_historical_data(stock_code, start_date, end_date)

    if not result:
        return ErrorResponse(f"未找到股票 {stock_code} 的历史数据")

    return SuccessResponse(result)


@router.get("/{data_id}", summary="获取股票基本信息详情")
async def get_stock_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    data = await crud.StockBaseInfoDal(auth.db).get_data(data_id)
    return SuccessResponse(data)


@router.get("", summary="获取股票基本信息列表，分页")
async def get_stocks(
    params: StockBaseInfoParams = Depends(), auth: Auth = Depends(AllUserAuth())
):
    stock_dict = params.dict()
    v_where = []
    if params.keywords:
        v_where.append(
            (
                StockBasicInfo.full_code.like("%" + params.keywords + "%")
                | StockBasicInfo.stock_name.like("%" + params.keywords + "%")
            )
        )
        stock_dict.pop("keywords")
    datas, count = await crud.StockBaseInfoDal(auth.db).get_datas(
        **stock_dict,
        v_where=v_where,
        v_return_count=True,
        v_schema=schemas.StockBaseInfoOut,
    )
    return SuccessResponse(datas, count=count)


@router.post("/export/excel", summary="导出股票查询列表为excel")
async def export_query_list(
    header: list = Body(..., title="表头与对应字段"),
    params: StockBaseInfoParams = Depends(),
    auth: Auth = Depends(FullAdminAuth(permissions=["stock.export"])),
):
    params.limit = 1000000
    stock_dict = params.dict()
    datas = await crud.StockBaseInfoDal(auth.db).get_datas(
        **stock_dict, v_return_count=False
    )
    return SuccessResponse(
        await crud.StockBaseInfoDal(auth.db).export_xlsx(header, datas)
    )


@router.delete("", summary="批量删除股票基本信息", description="硬删除")
async def delete_stocks(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.StockBaseInfoDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新股票基本信息")
async def put_stock(
    data_id: int, data: schemas.StockBaseInfoUpdate, auth: Auth = Depends(AllUserAuth())
):
    stock = await crud.StockBaseInfoDal(auth.db).put_data(data_id, data)
    return SuccessResponse(stock)
