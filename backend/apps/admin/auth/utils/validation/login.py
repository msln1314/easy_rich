#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/11/9 10:15
# @File           : login.py
# @IDE            : PyCharm
# @desc           : 登录验证装饰器

from datetime import datetime, timedelta
from fastapi import Request
from pydantic import BaseModel, field_validator
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from application.settings import settings
from apps.admin.system import crud, schemas, models
from apps.admin.log.models.login import SysLoginLog
from core.validator import valid_phone

class LoginForm(BaseModel):
    username: str  # 可以是手机号或邮箱
    password: str
    method: str = '0'  # 认证方式，0：密码登录，1：短信登录，2：微信一键登录
    platform: str = '0'  # 登录平台，0：PC端管理系统，1：移动端管理系统


class WXLoginForm(BaseModel):
    phone: str | None = None
    code: str
    method: str = '2'  # 认证方式，0：密码登录，1：短信登录，2：微信一键登录
    platform: str = '1'  # 登录平台，0：PC端管理系统，1：移动端管理系统


class LoginResult(BaseModel):
    status: bool | None = False
    user: schemas.UserOut | None = None
    msg: str | None = None

    class Config:
        arbitrary_types_allowed = True


class LoginValidation:

    """
    验证用户登录时提交的数据是否有效
    """

    def __init__(self, func):
        self.func = func

    async def __call__(self, data: LoginForm, db: AsyncSession, request: Request) -> LoginResult:
        self.result = LoginResult()
        if data.platform not in ["0", "1"] or data.method not in ["0", "1"]:
            self.result.msg = "无效参数"
            return self.result

        # 尝试通过手机号或邮箱查询用户
        user = await self._get_user_by_username(data.username, db)
        if not user:
            self.result.msg = "该账号不存在！"
            return self.result

        result = await self.func(self, data=data, user=user, db=db, request=request)

        # 基于数据库的登录错误计数（不使用Redis）
        if not result.status:
            self.result.msg = result.msg
            if not settings.DEMO:
                # 查询最近24小时内的登录错误次数
                # 计算24小时前的时间
                twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
                
            
                
                # 查询最近24小时内的登录错误次数
                from sqlalchemy import select
                query = select(
                    func.count(SysLoginLog.id).label('error_count')
                ).where(
                    SysLoginLog.username == data.username,
                    SysLoginLog.created_at >= twenty_four_hours_ago,
                    SysLoginLog.status == False  # 登录失败
                )
                error_count = await db.scalar(query)
                
                if error_count >= settings.DEFAULT_AUTH_ERROR_MAX_NUMBER:
                    # 如果达到最大错误次数，冻结用户
                    user.is_active = False
                    await db.flush()
        elif not user.is_active:
            self.result.msg = "此账号已被冻结！"
        elif data.platform in ["0", "1"] and not (user.is_staff or user.is_admin):
            self.result.msg = "此账号无权限！"
        else:
            self.result.msg = "OK"
            self.result.status = True
            self.result.user = schemas.UserSimpleOut.model_validate(user)
            await crud.UserDal(db).update_login_info(user, request.client.host)
        return self.result

    async def _get_user_by_username(self, username: str, db: AsyncSession):
        """
        通过手机号或邮箱查询用户
        :param username: 手机号或邮箱
        :param db: 数据库会话
        :return: 用户对象
        """
        
        # 尝试通过手机号或邮箱查询用户
        return await crud.UserDal(db).get_data(
            v_where=[
                (models.SysUser.phone == username) | (models.SysUser.email == username)
            ],
            v_return_none=True
        )
        
        
