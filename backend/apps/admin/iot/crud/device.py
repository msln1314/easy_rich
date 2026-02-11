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
from .client import ClientDal
from core.validator import vaild_ip

# from utils.file.aliyun_oss import AliyunOSS, BucketConf

from utils.excel.import_manage import ImportManage, FieldType
from utils.excel.write_xlsx import WriteXlsx
from utils.send_email import EmailSender
from utils.sms.reset_passwd import ResetPasswordSMS
from  apps.admin.iot.params import ClientGroupParams,ClientParams,ProductParams
from utils.tools import test_password
from apps.admin.iot import models, schemas
from application.settings import settings
from utils.excel.excel_manage import ExcelManage
from apps.admin.system import crud as sys_crud
import copy
from utils import status
from utils.wx.oauth import WXOAuth
from datetime import datetime
class DeviceDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DeviceDal, self).__init__()
        self.db = db
        self.model = models.IotDevice
        self.schema = schemas.DeviceSimpleOut

    async def get_select_datas(self,params) -> list:
        """
        获取选择数据，全部数据
        :return:
        """
        sql = select(self.model)
        queryset = await self.db.scalars(sql)
        return [schemas.DeviceSimpleOut.model_validate(i).model_dump() for i in queryset.all()]


    async def create_data(
            self,
            data: schemas.Device,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建数据
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        """
        obj = self.model(**data.model_dump())

        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.Device,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新单个数据
        :param data_id:
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        """
        options = [joinedload(self.model.product)]
        obj = await self.get_data(data_id,v_options=options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            setattr(obj, key, value)
        await self.flush(obj)
        print(obj.__dict__,"dict")
        return await self.out_dict(obj, None, v_return_obj, v_schema)


    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
        """
        删除多个设备，硬删除
        如果存在关联则无法删除
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        client_count = await ClientDal(self.db).get_count(v_where=[models.IotClient.device_id.in_(ids)])
        if client_count > 0:
            raise CustomException("无法删除存在客户端关联的设备", code=400)
        return await super(DeviceDal, self).delete_datas(ids, v_soft, **kwargs)


