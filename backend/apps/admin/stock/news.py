# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : news.py
# @IDE            : PyCharm
# @desc           : 新闻信息接口文件

from fastapi import APIRouter, Depends, Body, Request
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, Auth, OpenAuth
from .params import NewsParams
from . import schemas, crud
from core.dependencies import IdList


router = APIRouter()


###########################################################
#    新闻信息管理
###########################################################


@router.post("", summary="创建新闻信息")
async def create_news(data: schemas.NewsCreate, auth: Auth = Depends(AllUserAuth())):
    """
    创建新闻信息
    """
    news = await crud.NewsDal(auth.db).create_data(data=data)
    return SuccessResponse(news)


@router.get("", summary="获取新闻信息列表，分页")
async def get_news_list(params: NewsParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    """
    获取新闻信息列表
    """
    news_dict = params.dict()
    schema = schemas.NewsOut
    datas, count = await crud.NewsDal(auth.db).get_datas(
        **news_dict,
        v_schema=schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@router.post("/export/excel", summary="导出新闻查询列表为excel")
async def export_query_list(
        header: list = Body(..., title="表头与对应字段"),
        params: NewsParams = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["news.export"]))
):
    """
    导出新闻查询列表为excel
    """
    return SuccessResponse(await crud.NewsDal(auth.db).export_query_list(header, params))


@router.delete("", summary="批量删除新闻信息", description="硬删除")
async def delete_news(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    """
    批量删除新闻信息
    """
    await crud.NewsDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新新闻信息")
async def put_news(data_id: int, data: schemas.NewsUpdate, auth: Auth = Depends(AllUserAuth())):
    """
    更新新闻信息
    """
    news = await crud.NewsDal(auth.db).put_data(data_id, data)
    return SuccessResponse(news)


@router.get("/{data_id}", summary="获取新闻信息详情")
async def get_news_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    """
    获取新闻信息详情
    """
    data = await crud.NewsDal(auth.db).get_data(data_id)
    return SuccessResponse(data)


@router.put("/{news_id}/send", summary="更新新闻发送状态")
async def update_news_send_status(news_id: int, is_send: int = Body(..., embed=True), auth: Auth = Depends(AllUserAuth())):
    """
    更新新闻发送状态
    """
    await crud.NewsDal(auth.db).update_is_send([news_id], is_send)
    return SuccessResponse("更新成功")


@router.get("/send/{is_send}", summary="根据发送状态获取新闻列表")
async def get_news_by_send_status(is_send: int, auth: Auth = Depends(AllUserAuth())):
    """
    根据发送状态获取新闻列表
    :param is_send: 发送状态 0未发送 1已发送
    """
    datas = await crud.NewsDal(auth.db).get_by_is_send(is_send)
    return SuccessResponse(datas)


@router.get("/category/{category}", summary="根据分类获取新闻列表")
async def get_news_by_category(category: str, auth: Auth = Depends(AllUserAuth())):
    """
    根据分类获取新闻列表
    :param category: 分类
    """
    datas = await crud.NewsDal(auth.db).get_by_category(category)
    return SuccessResponse(datas)


@router.put("/{news_id}/analyze", summary="更新新闻分析状态")
async def update_news_analyze_status(news_id: int, analyze_data: dict = Body(...), auth: Auth = Depends(AllUserAuth())):
    """
    更新新闻分析状态和分析结果
    """
    await crud.NewsDal(auth.db).update_analyze_status(news_id, analyze_data)
    return SuccessResponse("更新成功")
