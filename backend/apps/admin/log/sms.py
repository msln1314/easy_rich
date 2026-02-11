# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from .crud import SMSSendLogDal
from apps.admin.auth.utils.current import AllUserAuth
from apps.admin.auth.utils.validation.auth import Auth
from .params.sms import SMSParams

router = APIRouter()


###########################################################
#    日志管理
###########################################################

@router.get("/send/list", summary="获取短信发送列表")
async def get_sms_send_list(p: SMSParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await SMSSendLogDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)

