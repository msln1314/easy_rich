#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:18
# @File           : operation_log.py
# @IDE            : PyCharm
# @desc           : 操作日志数据库操作

from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from .. import models, schemas
from core.crud import DalBase
from core.mongo_manage import MongoManage


class OperationLogDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(OperationLogDal, self).__init__()
        self.db = db
        # self.collection = db["operation_record"]
        self.model = models.SysOpertationLog
        self.schema = schemas.OperationLogSimpleOut
        self.is_object_id = True