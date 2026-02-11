#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/1/28
# @File           : code.py
# @IDE            : PyCharm
# @desc           : 验证码发送记录 Schema

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class CodeSendLogSimpleOut(BaseModel):
    """验证码发送记录简略输出"""

    id: int = Field(..., description="主键ID")
    user_id: int | None = Field(None, description="用户ID")
    contact: str = Field(..., description="联系方式（手机号或邮箱）")
    code: str = Field(..., description="验证码")
    code_type: str = Field(..., description="验证码类型：email-邮件，sms-短信")
    send_status: bool = Field(..., description="发送状态：True-成功，False-失败")
    send_time: DatetimeStr = Field(..., description="发送时间")
    expire_time: DatetimeStr = Field(..., description="失效时间")
    ip_address: str | None = Field(None, description="IP地址")
    scene: str | None = Field(None, description="发送场景：login-登录，register-注册，reset_password-重置密码")
    error_message: str | None = Field(None, description="错误信息")
    model_config = ConfigDict(from_attributes=True)


class CodeSendLogOut(CodeSendLogSimpleOut):
    """验证码发送记录详细输出"""

    # 由于基类已包含所有字段，这里不需要额外字段
    
    model_config = ConfigDict(from_attributes=True)