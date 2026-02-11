#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:18
# @File           : sms_send_log.py
# @IDE            : PyCharm
# @desc           : 短信发送日志数据库操作

from sqlalchemy.ext.asyncio import AsyncSession
from .. import models, schemas
from core.crud import DalBase


class SMSSendLogDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SMSSendLogDal, self).__init__()
        self.db = db
        self.model = models.VadminSMSSendLog
        self.schema = schemas.SMSSendLogSimpleOut