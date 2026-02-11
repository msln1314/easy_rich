#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/3/21 17:54 
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 简要说明


from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr


class SMSSendRecord(BaseModel):
    phone: str
    status: bool = True
    user_id: int | None = None
    content: str | None = None
    desc: str | None = None
    scene: str | None = None


class SMSSendRecordSimpleOut(SMSSendRecord):
    id: int
    created_at: DatetimeStr
    updated_at: DatetimeStr

    model_config = ConfigDict(from_attributes=True)
