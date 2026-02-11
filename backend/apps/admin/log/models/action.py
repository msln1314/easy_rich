#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : login.py
# @IDE            : PyCharm
# @desc           : 登录记录模型
import json


from application.settings import settings

from apps.admin.log.schemas.action import ActionLog
from utils.ip_manage import IPManage
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Text,Integer,ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from fastapi import Request
from starlette.requests import Request as StarletteRequest
from user_agents import parse
# from apps.admin.iot.models.device import IotDevice
from apps.admin.system.models.user import SysUser
class SysActionLog(BaseModel):
    __tablename__ = "iot_action_log"
    __table_args__ = ({'comment': '操作记录表'})
    ip: Mapped[str] = mapped_column(String(255), index=True, nullable=False, comment="ip")
    phone: Mapped[str] = mapped_column(String(255), index=True, nullable=False, comment="手机号")
    status: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否操作成功")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("sys_user.id", ondelete='CASCADE'), comment="操作人")
    # user_id: Mapped[int] = mapped_column(Integer, comment="是否登录成功")
    user: Mapped['SysUser'] = relationship(back_populates="user_logs")
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("iot_client.id", ondelete='CASCADE'), comment="客户端id")
    device_id: Mapped[int] = mapped_column(Integer, ForeignKey("iot_device.id", ondelete='CASCADE'), comment="设备id")
    device: Mapped['IotDevice'] = relationship(back_populates="device_logs")
    message: Mapped[str | None] = mapped_column(Text, comment="信息")

    browser: Mapped[str | None] = mapped_column(String(50), comment="浏览器")
    system: Mapped[str | None] = mapped_column(String(50), comment="操作系统")
    process_time: Mapped[float | None] = mapped_column(Text, comment="响应时间")
    params: Mapped[str | None] = mapped_column(Text, comment="请求参数")
    response: Mapped[str | None] = mapped_column(Text, comment="响应信息")

    @classmethod
    async def create_action_log(
            cls,
            db: AsyncSession,
            data: ActionLog,
            req: Request | StarletteRequest,

    ):
        """
        创建登录记录
        :return:
        """
        if not settings.ACTION_LOG_RECORD:
            return None

        user_agent = parse(req.headers.get("user-agent"))
        system = f"{user_agent.os.family} {user_agent.os.version_string}"
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        ip = IPManage(req.client.host)
        location = await ip.parse()
        print(data)
        data['status'] = True if data['status'] else False

        print(data)
        obj = SysActionLog(

            ip=req.client.host,
            # **data,
            browser=browser,
            system=system,
            status=data['status'],
            device_id=data['device_id'],
            user_id =data['user_id'],
            phone=data['phone'],
            message = data.get('message'),
            client_id = data['client_id']





        )
        print(obj.__dict__)
        db.add(obj)
        await db.flush()
        # await db.commit()
