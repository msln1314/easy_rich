# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from .crud import LoginLogDal
from apps.admin.auth.utils.current import AllUserAuth
from apps.admin.auth.utils.validation.auth import Auth
from .params.login import LoginParams
from .schemas import LoginLogSimpleOut
router = APIRouter()


###########################################################
#    日志管理
###########################################################


@router.get("", summary="获取登录日志列表")
async def get_record_login(p: LoginParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await LoginLogDal(auth.db).get_datas(**p.dict(), v_return_count=True, v_schema=LoginLogSimpleOut)
    return SuccessResponse(datas, count=count)

@router.get("/analysis/user/login/distribute", summary="获取用户登录分布情况列表")
async def get_user_login_distribute(auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await LoginLogDal(auth.db).get_user_distribute())
