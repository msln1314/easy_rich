#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/1/28
# @File           : code.py
# @IDE            : PyCharm
# @desc           : 验证码发送记录模型

from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime


class SysCodeSendLog(BaseModel):
    __tablename__ = "sys_code_send_log"
    __table_args__ = ({'comment': '验证码发送记录表'})

    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("sys_user.id", ondelete='CASCADE'), nullable=True, comment="用户ID")
    contact: Mapped[str] = mapped_column(String(100), comment="联系方式（手机号或邮箱）")
    code: Mapped[str] = mapped_column(String(10), comment="验证码")
    code_type: Mapped[str] = mapped_column(String(20), comment="验证码类型：email-邮件，sms-短信")
    send_status: Mapped[bool] = mapped_column(Boolean, default=True, comment="发送状态：True-成功，False-失败")
    send_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发送时间")
    expire_time: Mapped[datetime] = mapped_column(DateTime, comment="失效时间")
    ip_address: Mapped[str | None] = mapped_column(String(50), comment="IP地址")
    scene: Mapped[str | None] = mapped_column(String(50), comment="发送场景：login-登录，register-注册，reset_password-重置密码")
    error_message: Mapped[str | None] = mapped_column(String(255), comment="错误信息")
