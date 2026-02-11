#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据库 增删改查操作

import json
import os
from enum import Enum

from motor.motor_asyncio import AsyncIOMotorDatabase
from application.settings import settings
from core.database import redis_getter
from core.mongo_manage import MongoManage
from utils.file.file_manage import FileManage
from fastapi import Request
from typing import Any
from redis.asyncio import Redis
from fastapi import UploadFile
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.exception import CustomException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, false,update,func
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from core.validator import valid_phone
# from utils.file.aliyun_oss import AliyunOSS, BucketConf
from apps.admin.system import models, schemas
import copy
from utils import status
from utils.wx.oauth import WXOAuth
from datetime import datetime
from application.settings import settings

REDIS_DB_ENABLE = settings.REDIS_DB_ENABLE
STATIC_ROOT = settings.STATIC_ROOT
class SettingsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SettingsDal, self).__init__()
        self.db = db
        self.model = models.SysSetting
        self.schema = schemas.SettingsSimpleOut

    async def get_tab(name):
        """
        获取系统配置标签
        """
        return await self.get_data(tab_name=name, v_return_objs=True)
    
    async def get_tab_values(self, tab_id: int) -> dict:
        """
        获取系统配置标签下的信息
        """
        datas = await self.get_datas(limit=0, tab_id=tab_id, v_return_objs=True)
        result = {}
        for data in datas:
            if not data.disabled:
                result[data.config_key] = data.config_value
        return result

    async def update_datas(self, datas: dict, request: Request) -> None:
        """
        更新系统配置信息

        更新ico图标步骤：先将文件上传到本地，然后点击提交后，获取到文件地址，将上传的新文件覆盖原有文件
        原因：ico图标的路径是在前端的index.html中固定的，所以目前只能改变图片，不改变路径
        """
        for key, value in datas.items():
            if key == "web_ico":
                continue
            elif key == "web_ico_local_path":
                if not value:
                    continue
                ico = await self.get_data(config_key="web_ico", tab_id=1)
                web_ico = datas.get("web_ico")
                if ico.config_value == web_ico:
                    continue
                # 将上传的ico路径替换到static/system/favicon.ico文件
                await FileManage.async_copy_file(value, os.path.join(STATIC_ROOT, "system/favicon.ico"))
                sql = update(self.model).where(self.model.config_key == "web_ico").values(config_value=web_ico)
                await self.db.execute(sql)
            else:
                sql = update(self.model).where(self.model.config_key == str(key)).values(config_value=value)
                await self.db.execute(sql)
        if "wx_server_app_id" in datas and REDIS_DB_ENABLE:
            rd = redis_getter(request)
            await rd.client().set("wx_server", json.dumps(datas))
        elif "sms_access_key" in datas and REDIS_DB_ENABLE:
            rd = redis_getter(request)
            await rd.client().set('aliyun_sms', json.dumps(datas))

    async def get_base_config(self) -> dict:
        """
        获取系统基本信息
        """
        ignore_configs = ["wx_server_app_id", "wx_server_app_secret"]
        datas = await self.get_datas(limit=0, tab_id=("in", ["1", "9"]), disabled=False, v_return_objs=True)
        result = {}
        for config in datas:
            if config.config_key not in ignore_configs:
                result[config.config_key] = config.config_value
        return result


class SettingsTabDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SettingsTabDal, self).__init__(db, models.SysSettingTab, schemas.SettingsTabSimpleOut)

    async def get_classify_tab_values(self, classify: list[str], hidden: bool | None = False) -> dict:
        """
        获取系统配置分类下的标签信息
        """
        model = models.SysSettingTab
        options = [joinedload(model.settings)]
        datas = await self.get_datas(
            limit=0,
            v_options=options,
            classify=("in", classify),
            disabled=False,
            v_return_objs=True,
            hidden=hidden
        )
        return self.__generate_values(datas)

    async def get_tab_name_values(self, tab_names: list[str], hidden: bool | None = False) -> dict:
        """
        获取系统配置标签下的标签信息
        """
        model = models.SysSettingTab
        options = [joinedload(model.settings)]
        datas = await self.get_datas(
            limit=0,
            v_options=options,
            tab_name=("in", tab_names),
            status=True,
            v_return_objs=True,
            hidden=hidden
        )
        return self.__generate_values(datas)

    @classmethod
    def __generate_values(cls, datas: list[models.SysSettingTab]) -> dict:
        """
        生成字典值
        """
        return {
            tab.tab_name: {
                item.config_key: item.config_value
                for item in tab.settings
                if not item.disabled
            }
            for tab in datas
        }

