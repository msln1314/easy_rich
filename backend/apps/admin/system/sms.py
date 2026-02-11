# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from redis.asyncio import Redis
from fastapi import APIRouter, Depends, Body, UploadFile, Form, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession
# from application.settings import ALIYUN_OSS
from core.database import db_getter, redis_getter, mongo_getter
# from utils.file.aliyun_oss import AliyunOSS, BucketConf
from utils.file.file_manage import FileManage
from utils.response import SuccessResponse, ErrorResponse
from utils.sms.code import CodeSMS

from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, OpenAuth,Auth
from .params import DictTypeParams, DictDetailParams, TaskParams

from sqlalchemy.orm import joinedload
from . import schemas, crud, models
from core.dependencies import IdList
from .params import UserParams, RoleParams, DeptParams

router = APIRouter()





###########################################################
#    短信服务管理
###########################################################
@router.post("/send", summary="发送短信验证码（阿里云服务）")
async def sms_send(phone: str, rd: Redis = Depends(redis_getter), auth: Auth = Depends(OpenAuth())):
    user = await crud.UserDal(auth.db).get_data(phone=phone, v_return_none=True)
    if not user:
        return ErrorResponse("手机号不存在！")
    sms = CodeSMS(phone, rd)
    return SuccessResponse(await sms.main_async())


###########################################################
#    系统配置管理
###########################################################
@router.post("/settings/tabs", summary="获取系统配置标签列表")
async def get_settings_tabs(classifys: list[str] = Body(...), auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.SettingsTabDal(auth.db).get_datas(limit=0, classify=("in", classifys)))


@router.get("/settings/tabs/values", summary="获取系统配置标签下的信息")
async def get_settings_tabs_values(tab_id: int, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.SettingsDal(auth.db).get_tab_values(tab_id=tab_id))


@router.put("/settings/tabs/values", summary="更新系统配置信息")
async def put_settings_tabs_values(
        request: Request,
        datas: dict = Body(...),
        auth: Auth = Depends(FullAdminAuth())
):
    return SuccessResponse(await crud.SettingsDal(auth.db).update_datas(datas, request))


@router.get("/settings/base/config", summary="获取系统基础配置", description="每次进入系统中时使用")
async def get_setting_base_config(db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.SettingsDal(db).get_base_config())


@router.get("/settings/privacy", summary="获取隐私协议")
async def get_settings_privacy(auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse((await crud.SettingsDal(auth.db).get_data(config_key="web_privacy")).config_value)


@router.get("/settings/agreement", summary="获取用户协议")
async def get_settings_agreement(auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse((await crud.SettingsDal(auth.db).get_data(config_key="web_agreement")).config_value)

