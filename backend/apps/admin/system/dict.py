# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends, Body, UploadFile, Form, Request
from utils.response import SuccessResponse, ErrorResponse

from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, OpenAuth,Auth
from .params import DictTypeParams, DictDetailParams, TaskParams
from . import schemas, crud, models
from core.dependencies import IdList


router = APIRouter()



###########################################################
#    字典类型管理
###########################################################
@router.get("/types", summary="获取字典类型列表")
async def get_dict_types(p: DictTypeParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.DictTypeDal(auth.db).get_datas(**p.dict(), v_return_count=True,v_schema=schemas.DictTypeSimpleOut)
    return SuccessResponse(datas, count=count)


@router.post("/types", summary="创建字典类型")
async def create_dict_types(data: schemas.DictType, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DictTypeDal(auth.db).create_data(data=data))


@router.delete("/types", summary="批量删除字典类型")
async def delete_dict_types(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DictTypeDal(auth.db).delete_datas(ids=ids.ids)
    return SuccessResponse("删除成功")


@router.post("/type/dicts", summary="获取多个字典类型下的字典元素列表")
async def post_type_dicts(
        auth: Auth = Depends(AllUserAuth()),
        dict_types: list[str] = Body(None, title="字典元素列表", description="查询字典元素列表")
):
    print(dict_types,"dict")
    datas = await crud.DictTypeDal(auth.db).get_dict_type_dicts(dict_types)
    return SuccessResponse(datas)


@router.get("/types/options", summary="获取字典类型选择项")
async def get_dicts_options(auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DictTypeDal(auth.db).get_select_datas())


@router.put("/types/{data_id}", summary="更新字典类型")
async def put_dict_types(data_id: int, data: schemas.DictType, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DictTypeDal(auth.db).put_data(data_id, data))


@router.get("/types/{data_id}", summary="获取字典类型详细")
async def get_dict_type(data_id: int, auth: Auth = Depends(AllUserAuth())):
    schema = schemas.DictTypeSimpleOut
    return SuccessResponse(await crud.DictTypeDal(auth.db).get_data(data_id, v_schema=schema))





###########################################################
#    字典元素管理
###########################################################
@router.post("", summary="创建字典元素")
async def create_dict(data: schemas.Dict, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DictDal(auth.db).create_data(data=data))


@router.get("", summary="获取单个字典类型下的字典元素列表，分页")
async def get_dict(params: DictDetailParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.DictDal(auth.db).get_datas(**params.dict(), v_return_count=True,v_schema=schemas.DictSimpleOut)
    return SuccessResponse(datas, count=count)


@router.delete("", summary="批量删除字典元素", description="硬删除")
async def delete_dict(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DictDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新字典元素")
async def put_dict(data_id: int, data: schemas.Dict, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DictDal(auth.db).put_data(data_id, data))


@router.get("/{data_id}", summary="获取字典元素详情")
async def get_dict_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    schema = schemas.DictSimpleOut
    return SuccessResponse(await crud.DictDal(auth.db).get_data(data_id, v_schema=schema))


