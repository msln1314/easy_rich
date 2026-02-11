# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from .crud import OperationLogDal
from apps.admin.auth.utils.current import AllUserAuth
from apps.admin.auth.utils.validation.auth import Auth
from .params.operation import OperationParams

router = APIRouter()


###########################################################
#    日志管理
###########################################################


@router.get("", summary="获取操作日志列表")
async def get_record_operation(
        p: OperationParams = Depends(),
        # db: AsyncIOMotorDatabase = Depends(AllUserAuth),
        auth: Auth = Depends(AllUserAuth())
):
    count = await OperationLogDal(auth.db).get_count(**p.to_count())
    datas = await OperationLogDal(auth.db).get_datas(**p.dict())
    return SuccessResponse(datas, count=count)

