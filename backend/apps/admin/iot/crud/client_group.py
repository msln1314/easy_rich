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
from utils.tools import find_node_and_subtree
# from utils.file.aliyun_oss import AliyunOSS, BucketConf

from utils.excel.import_manage import ImportManage, FieldType
from utils.excel.write_xlsx import WriteXlsx
from utils.send_email import EmailSender
from utils.sms.reset_passwd import ResetPasswordSMS
from utils.tools import test_password
from apps.admin.iot import models, schemas
from application.settings import settings
from utils.excel.excel_manage import ExcelManage
from apps.admin.system import crud as sys_crud
import copy
from utils import status
from utils.wx.oauth import WXOAuth
from datetime import datetime

class ClientGroupDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ClientGroupDal, self).__init__()
        self.db = db
        self.model = models.IotClientGroup
        self.schema = schemas.ClientGroupSimpleOut

    async def get_tree_list(self, mode: int) -> list:
        """
        1：获取部门树列表
        2：获取部门树选择项，添加/修改部门时使用
        3：获取部门树列表，用户添加部门权限时使用
        :param mode:
        :return:
        """
        if mode == 3:
            sql = select(self.model).where(self.model.status == 0, self.model.is_delete == false())
        else:
            sql = select(self.model).where(self.model.is_delete == false())
        queryset = await self.db.scalars(sql)
        datas = list(queryset.all())

        roots = filter(lambda i: not i.parent_id, datas)
        if mode == 1:
            groups = self.generate_tree_list(datas, roots)
        elif mode == 2 or mode == 3:
            groups = self.generate_tree_options(datas, roots)
        else:
            raise CustomException("获取分组失败，无可用选项", code=400)
        return self.group_order(groups)

    def generate_tree_list(self, groups: list[models.IotClientGroup], nodes: filter) -> list:
        """
        生成部门树列表
        :param depts: 总部门列表
        :param nodes: 每层节点部门列表
        :return:
        """
        data = []
        for root in nodes:
            router = schemas.ClientGroupTreeListOut.model_validate(root)
            sons = filter(lambda i: i.parent_id == root.id, groups)
            router.children = self.generate_tree_list(groups, sons)
            data.append(router.model_dump())
        return data

    async def get_child_ids(self, root_id: int) -> list:
        """
        生成获取子部门id
        :param groups: 总部门列表
        :param rootId: 每层节点部门列表
        :return:
        """


        datas = await self.get_tree_list(mode=1)
        print(datas,"datas")
        trees,ids = find_node_and_subtree(datas, root_id)
        return ids
    def generate_tree_options(self, groups: list[models.IotClientGroup], nodes: filter) -> list:
        """
        生成部门树选择项
        :param depts: 总部门列表
        :param nodes: 每层节点部门列表
        :return:
        """
        data = []
        for root in nodes:
            router = {"value": root.id, "label": root.name, "order": root.order}
            sons = filter(lambda i: i.parent_id == root.id, groups)
            router["children"] = self.generate_tree_options(groups, sons)
            data.append(router)
        return data

    @classmethod
    def group_order(cls, datas: list, order: str = "order", children: str = "children") -> list:
        """
        部门排序
        :param datas:
        :param order:
        :param children:
        :return:
        """
        result = sorted(datas, key=lambda group: group[order])
        for item in result:
            if item[children]:
                item[children] = sorted(item[children], key=lambda group: group[order])
        return result
