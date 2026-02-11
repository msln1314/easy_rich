#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : user.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from core.data_types import Phone, DatetimeStr, Email
from .role import RoleSimpleOut
from .dept import DeptSimpleOut
from apps.admin.iot.schemas.client_group import ClientGroupSimpleOut


class User(BaseModel):
    name: str | None = None
    phone: Phone = None
    email: Email = None
    nickname: str | None = None
    avatar: str | None = None
    is_active: bool | None = True
    is_staff: bool | None = True
    is_admin: bool | None = False
    dept_id: int | None = False
    gender: str | None = "0"
    is_wx_server_openid: bool | None = False


class UserIn(User):
    """
    创建用户
    """
    role_ids: list[int] = []
    iot_group_ids: list[int] = []
    # roles: list[RoleSimpleOut] = []
    password: str | None = ""


class UserUpdateBaseInfo(BaseModel):
    """
    更新用户基本信息
    """
    name: str
    phone: Phone
    email: Email | None = None
    nickname: str | None = None
    gender: str | None = "0"


class UserUpdate(User):
    """.
    更新用户详细信息
    """
    name: str | None = None
    email: Email | None = None
    nickname: str | None = None
    avatar: str | None = None
    is_active: bool | None = True
    is_staff: bool|None = False
    is_admin: bool | None = False
    gender: str | None = "0"
    role_ids: list[int] = []
    iot_group_ids: list[int] = []
    dept_id: int|None = None



class UserSimpleOut(User):
    model_config = ConfigDict(from_attributes=True)

    id: int
    updated_at: DatetimeStr
    created_at: DatetimeStr
    is_reset_password: bool | None = None
    last_login: DatetimeStr | None = None
    last_ip: str | None = None


class UserOut(UserSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    roles: list[RoleSimpleOut] = []
    # iot_groups : list[ClientGroupSimpleOut] = []
    dept: DeptSimpleOut | None = None


class ResetPwd(BaseModel):
    password: str
    password_two: str

    @field_validator('password_two')
    def check_passwords_match(cls, v, info: FieldValidationInfo):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('两次密码不一致!')
        return v
