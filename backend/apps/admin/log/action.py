# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import models
from .crud import ActionLogDal
from apps.admin.auth.utils.current import AllUserAuth
from apps.admin.auth.utils.validation.auth import Auth
from .params.action import ActionParams
from sqlalchemy.orm import joinedload
router = APIRouter()


###########################################################
#    日志管理
###########################################################
@router.get("", summary="获取操作日志列表")
async def get_record_login(params: ActionParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    # model = models.action
    # v_join = [[IotDevice]]
    options = [joinedload(models.SysActionLog.device),joinedload(models.SysActionLog.user)]
    datas, count = await ActionLogDal(auth.db).get_datas(**params.dict(), v_return_count=True,v_options=options)
    return SuccessResponse(datas, count=count)

