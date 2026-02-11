#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/8/8 11:02
# @File           : auth_util.py
# @IDE            : PyCharm
# @desc           : 简要说明

from datetime import datetime, timedelta
from fastapi import Request
from application.settings import settings

import jwt
from .validation import LoginValidation, LoginForm, LoginResult
from apps.admin.system import models
from utils.sms.code_manager import CodeManager

class LoginManage:
    """
    登录认证工具
    """

    @LoginValidation
    async def password_login(self, data: LoginForm, user: models.SysUser, db=None, request=None, **kwargs) -> LoginResult:
        """
        验证用户密码
        """
        result = models.SysUser.verify_password(data.password, user.password)
        if result:
            return LoginResult(status=True, msg="验证成功")
        return LoginResult(status=False, msg="手机号或密码错误")

    @LoginValidation
    async def sms_login(self, data: LoginForm, user: models.SysUser, db=None, request=None, **kwargs) -> LoginResult:
        """
        验证用户短信验证码（使用数据库验证）
        """
        if not db:
            return LoginResult(status=False, msg="数据库会话不能为空")
        
        # 使用CodeManager验证短信验证码
        code_manager = CodeManager(data.username, db=db)
        result = await code_manager.verify_code(data.password)
        if result:
            return LoginResult(status=True, msg="验证成功")
        return LoginResult(status=False, msg="验证码错误")

    @staticmethod
    def create_token(payload: dict, expires: timedelta = None):
        """
        创建一个生成新的访问令牌的工具函数。

        pyjwt：https://github.com/jpadilla/pyjwt/blob/master/docs/usage.rst
        jwt 博客：https://geek-docs.com/python/python-tutorial/j_python-jwt.html

        #TODO 传入的时间为UTC时间datetime.datetime类型，但是在解码时获取到的是本机时间的时间戳
        """
        if expires:
            expire = datetime.utcnow() + expires
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
print(11)