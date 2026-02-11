# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_analysis.py
# @IDE            : PyCharm
# @desc           : 股票分析接口文件

from fastapi import APIRouter, Depends, Body
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, Auth
from .params import StockAnalysisParams
from . import schemas, crud
from core.dependencies import IdList
from services.stock_service import StockService

router = APIRouter()


###########################################################
#    股票分析管理
###########################################################


@router.post("", summary="创建股票分析")
async def create_stock_analysis(data: schemas.StockAnalysisCreate, auth: Auth = Depends(AllUserAuth())):
    """
    创建股票分析
    """
    service = StockService()
    result = await service.get_stock_info(data.stock_code)
    stock_info = result["data"]
    data.stock_name = stock_info.get("name")
    data.stock_industry = stock_info.get("industry")
    data.analysis_price = stock_info.get("current_price")
    data.open_price = stock_info.get("open")
    data.high_price = stock_info.get("high")
    data.low_price = stock_info.get("low")
    data.analysis_change_percent = stock_info.get("change_percent")
    data.analysis_turnover_rate = stock_info.get("turnover_rate")
    data.analysis_volume_ratio = stock_info.get("volume_ratio")
    data.volume = stock_info.get("volume")
    data.amount = stock_info.get("turnover")
    data.user_id = auth.user.id
    data.stock_code = stock_info.get("market") + stock_info.get("code")
    analysis = await crud.StockAnalysisDal(auth.db).create_data(data=data,v_schema=schemas.StockAnalysisOut)
    return SuccessResponse(analysis)


@router.get("", summary="获取股票分析列表，分页")
async def get_stock_analysis_list(params: StockAnalysisParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    """
    获取股票分析列表
    """
    analysis_dict = params.dict()
    datas, count = await crud.StockAnalysisDal(auth.db).get_datas(
        **analysis_dict,
        v_return_count=True,
        v_schema=schemas.StockAnalysisOut
    )
    return SuccessResponse(datas, count=count)


@router.post("/export/excel", summary="导出股票分析为excel")
async def export_query_list(
        header: list = Body(..., title="表头与对应字段"),
        params: StockAnalysisParams = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["stock_analysis.export"]))
):
    """
    导出股票分析为excel
    """
    params.limit = 1000000
    analysis_dict = params.dict()
    datas = await crud.StockAnalysisDal(auth.db).get_datas(
        **analysis_dict,
        v_return_count=False
    )
    return SuccessResponse(await crud.StockAnalysisDal(auth.db).export_xlsx(header, datas))


@router.delete("", summary="批量删除股票分析", description="硬删除")
async def delete_stock_analysis(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    """
    批量删除股票分析
    """
    await crud.StockAnalysisDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新股票分析")
async def put_stock_analysis(data_id: int, data: schemas.StockAnalysisUpdate, auth: Auth = Depends(AllUserAuth())):
    """
    更新股票分析
    """
    analysis = await crud.StockAnalysisDal(auth.db).put_data(data_id, data)
    return SuccessResponse(analysis)


@router.get("/{data_id}", summary="获取股票分析详情")
async def get_stock_analysis_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    """
    获取股票分析详情
    """
    data = await crud.StockAnalysisDal(auth.db).get_data(data_id, v_schema=schemas.StockAnalysisOut)

    return SuccessResponse(data)


@router.get("/stock/{stock_code}", summary="根据股票代码获取分析列表")
async def get_analysis_by_stock_code(stock_code: str, limit: int = 10, auth: Auth = Depends(AllUserAuth())):
    """
    根据股票代码获取分析列表
    :param stock_code: 股票代码
    :param limit: 限制数量，默认10
    """
    datas = await crud.StockAnalysisDal(auth.db).get_by_stock_code(stock_code, limit)
    return SuccessResponse(datas)


@router.get("/result/{analysis_result}", summary="根据分析结果获取列表")
async def get_analysis_by_result(analysis_result: str, auth: Auth = Depends(AllUserAuth())):
    """
    根据分析结果获取列表
    :param analysis_result: 分析结果（看涨/看跌/中性）
    """
    datas = await crud.StockAnalysisDal(auth.db).get_by_analysis_result(analysis_result)
    return SuccessResponse(datas)


@router.get("/valid/{is_valid}", summary="获取有效的分析记录")
async def get_valid_analyses(is_valid: int = 1, auth: Auth = Depends(AllUserAuth())):
    """
    获取有效的分析记录
    :param is_valid: 是否有效，默认1（有效）
    """
    datas = await crud.StockAnalysisDal(auth.db).get_valid_analyses(is_valid)
    return SuccessResponse(datas)


@router.put("/{analysis_id}/verify", summary="验证分析结果")
async def verify_analysis(
    analysis_id: int,
    data: dict = Body(..., description="验证数据"),
    auth: Auth = Depends(AllUserAuth())
):
    """
    验证分析结果
    :param analysis_id: 分析ID
    :param data: 验证数据 { is_valid: 1, verification_result: "正确" }
    """
    is_valid = data.get('is_valid')
    verification_result = data.get('verification_result')
    await crud.StockAnalysisDal(auth.db).verify_analysis(analysis_id, verification_result, is_valid)
    return SuccessResponse("验证成功")


@router.put("/{analysis_id}/send", summary="更新分析发送状态")
async def update_send_status(analysis_id: int, is_send: int = Body(..., embed=True), auth: Auth = Depends(AllUserAuth())):
    """
    更新分析发送状态
    :param analysis_id: 分析ID
    :param is_send: 是否发送
    """
    await crud.StockAnalysisDal(auth.db).update_send_status(analysis_id, is_send)
    return SuccessResponse("更新成功")


@router.get("/user/{user_id}", summary="根据用户ID获取分析列表")
async def get_analysis_by_user(user_id: int, auth: Auth = Depends(AllUserAuth())):
    """
    根据用户ID获取分析列表
    :param user_id: 用户ID
    """
    datas = await crud.StockAnalysisDal(auth.db).get_by_user_id(user_id)
    return SuccessResponse(datas)
