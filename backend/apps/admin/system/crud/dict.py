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

from utils.excel.import_manage import ImportManage, FieldType
from utils.excel.write_xlsx import WriteXlsx
from utils.send_email import EmailSender
from utils.sms.reset_passwd import ResetPasswordSMS
from utils.tools import test_password
from apps.admin.system import models, schemas
from application.settings import settings
from utils.excel.excel_manage import ExcelManage
import copy
from utils import status
from utils.wx.oauth import WXOAuth
from datetime import datetime



class DictTypeDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DictTypeDal, self).__init__()
        self.db = db
        self.model = models.SysDictType
        self.schema = schemas.DictTypeSimpleOut

    async def get_dict_type_dicts(self, dict_types: list[str]) -> dict:
        """
        获取多个字典类型下的字典元素列表
        """
        data = {}
        options = [joinedload(self.model.dicts)]
        objs = await DictTypeDal(self.db).get_datas(
            limit=0,
            v_return_objs=True,
            v_options=options,
            dict_type=("in", dict_types)
        )
        for obj in objs:
            if obj.dicts:
                data[obj.dict_type] = [schemas.DictSimpleOut.model_validate(i).model_dump() for i in obj.dicts]
            else:
                data[obj.dict_type] = []
        return data

    async def get_select_datas(self) -> list:
        """获取选择数据，全部数据"""
        sql = select(self.model)
        queryset = await self.db.execute(sql)
        return [schemas.DictTypeOptionsOut.model_validate(i).model_dump() for i in queryset.scalars().all()]


class DictDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DictDal, self).__init__()
        self.db = db
        self.model = models.SysDict
        self.schema = schemas.DictSimpleOut

