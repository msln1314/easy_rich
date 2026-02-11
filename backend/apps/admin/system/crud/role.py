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
from apps.admin.system.params import UserParams
from utils.tools import test_password
from apps.admin.system import models, schemas
from .menu import MenuDal
from .user import UserDal
from application.settings import settings
from utils.excel.excel_manage import ExcelManage
from apps.admin.system import crud as sys_crud
import copy
from utils import status
from utils.wx.oauth import WXOAuth
from datetime import datetime



class RoleDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RoleDal, self).__init__()
        self.db = db
        self.model = models.SysRole
        self.schema = schemas.RoleSimpleOut

    async def create_data(
            self,
            data: schemas.RoleIn,
            menus: list[models.SysMenu],
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
        obj = self.model(**data.model_dump(exclude={'menu_ids', 'dept_ids'}))
        if menus:
            for menu in menus:
                obj.menus.add(menu)
        # print(data,"daaaaaaaaaaaaaaaaaaaa")
        # if data.dept_ids:
        #     depts = await DeptDal(db=self.db).get_datas(limit=0, id=("in", data.dept_ids), v_return_objs=True)
        #     for dept in depts:
        #         obj.depts.add(dept)
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.RoleIn,
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
        obj = await self.get_data(data_id, v_options=[joinedload(self.model.menus)])
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            if key == "menu_ids":
                if value:
                    menus = await MenuDal(db=self.db).get_datas(limit=0, id=("in", value), v_return_objs=True)
                    if obj.menus:
                        obj.menus.clear()
                    for menu in menus:
                        obj.menus.add(menu)
                continue
            elif key == "user_ids":
                if value:
                    users = await UserDal(db=self.db).get_datas(limit=0, id=("in", value), v_return_objs=True)
                    if obj.users:
                        obj.users.clear()
                    for user in users:
                        obj.users.add(user)
                continue
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def get_role_menu_tree(self, role_id: int) -> list:
        role = await self.get_data(role_id, v_options=[joinedload(self.model.menus)])
        return [i.id for i in role.menus]

    async def get_select_datas(self) -> list:
        """
        获取选择数据，全部数据
        :return:
        """
        sql = select(self.model)
        queryset = await self.db.scalars(sql)
        return [schemas.RoleOptionsOut.model_validate(i).model_dump() for i in queryset.all()]

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
        """
        删除多个角色，硬删除
        如果存在用户关联则无法删除
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        user_count = await UserDal(self.db).get_count(v_join=[["roles"]], v_where=[models.SysRole.id.in_(ids)])
        if user_count > 0:
            raise CustomException("无法删除存在用户关联的角色", code=400)
        return await super(RoleDal, self).delete_datas(ids, v_soft, **kwargs)

