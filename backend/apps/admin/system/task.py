# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse

from apps.admin.auth.utils.current import AllUserAuth, Auth
from .params import TaskParams
from . import schemas, crud

router = APIRouter()





###########################################################
#    定时任务管理
###########################################################
@router.get("", summary="获取定时任务列表")
async def get_tasks(
        p: TaskParams = Depends(),
        auth: Auth = Depends(AllUserAuth())
):

    datas, count = await crud.TaskDal(auth.db).get_tasks(**p.dict())
    return SuccessResponse(datas, count=count)


@router.post("", summary="添加定时任务")
async def post_tasks(
        data: schemas.TaskCreate,
        auth: Auth = Depends(AllUserAuth())
):
    result = await crud.TaskDal(auth.db).create_task(data)
    return SuccessResponse(result)


@router.put("/{_id}", summary="更新定时任务")
async def put_tasks(
        _id: int,
        data: schemas.TaskUpdate,
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.TaskDal(auth.db).put_task(_id, data))


@router.delete("/{_id}", summary="删除单个定时任务")
async def delete_task(
        _id: int,
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.TaskDal(auth.db).delete_task(_id))



@router.get("/{_id}", summary="获取定时任务详情")
async def get_task(
        _id: int,
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.TaskDal(auth.db).get_task(_id, v_schema=schemas.TaskOut))


@router.post("/{_id}/run", summary="执行一次定时任务")
async def run_once_task(
    _id: int,
    auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.TaskDal(auth.db).run_once_task(_id))


###########################################################
#    定时任务分组管理
###########################################################
@router.get("/group/options", summary="获取定时任务分组选择项列表")
async def get_task_group_options(auth: Auth = Depends(AllUserAuth())):
 
    schema = schemas.TaskGroupOut
    return SuccessResponse(await crud.TaskGroupDal(auth.db).get_datas(limit=0,v_schema=schema))


