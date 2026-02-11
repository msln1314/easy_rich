# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : task.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from apps.admin.log.crud import TaskLogDal
from apps.admin.log.schemas import TaskLogOut
from apps.admin.log.params.task import TaskLogParams
from apps.admin.auth.utils.current import AllUserAuth
from apps.admin.auth.utils.validation.auth import Auth

router = APIRouter()


###########################################################
#    定时任务调度日志
###########################################################
@router.get("", summary="获取定时任务调度日志列表")
async def get_task_records(
        p: TaskLogParams = Depends(),
        auth: Auth = Depends(AllUserAuth())
):
    datas, count = await TaskLogDal(auth.db).get_datas(
        **p.dict(),
        v_schema=TaskLogOut,
        v_return_count=True

    )
    return SuccessResponse(datas, count=count)




