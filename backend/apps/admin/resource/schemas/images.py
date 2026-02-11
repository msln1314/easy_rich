#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/8/25 14:49
# @File           : images.py
# @IDE            : PyCharm
# @desc           : 简要说明


from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr
from apps.admin.system.schemas import UserSimpleOut


class Images(BaseModel):
    filename: str
    image_url: str

    create_user_id: int


class ImagesSimpleOut(Images):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: DatetimeStr
    updated_at: DatetimeStr


class ImagesOut(ImagesSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    create_user: UserSimpleOut
