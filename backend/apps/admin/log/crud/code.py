#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/1/28
# @File           : code.py
# @IDE            : PyCharm
# @desc           : 验证码发送记录 CRUD

from core.crud import DalBase
from apps.admin.log import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, and_,select
from datetime import datetime


class CodeSendLogDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(CodeSendLogDal, self).__init__()
        self.db = db
        self.model = models.SysCodeSendLog
        self.schema = schemas.CodeSendLogSimpleOut

    async def create_code_log(
        self,
        user_id: int | None,
        contact: str,
        code: str,
        code_type: str,
        send_status: bool,
        expire_time,
        ip_address: str = None,
        scene: str = "login",
        error_message: str = None
    ) -> schemas.CodeSendLogOut:
        """
        创建验证码发送记录

        :param user_id: 用户ID
        :param contact: 联系方式
        :param code: 验证码
        :param code_type: 验证码类型
        :param send_status: 发送状态
        :param expire_time: 失效时间
        :param ip_address: IP地址
        :param scene: 发送场景
        :param error_message: 错误信息
        :return: 验证码发送记录
        """
        from datetime import datetime

        data = {
            "user_id": user_id,
            "contact": contact,
            "code": code,
            "code_type": code_type,
            "send_status": send_status,
            "send_time": datetime.now(),
            "expire_time": expire_time,
            "ip_address": ip_address,
            "scene": scene,
            "error_message": error_message
        }

        return await self.create_data(data, v_schema=schemas.CodeSendLogOut)

    async def verify_code(self, contact: str, code: str, scene: str = None) -> bool:
        """
        验证验证码是否正确

        :param contact: 联系方式
        :param code: 验证码
        :param scene: 发送场景（可选）
        :return: 是否验证成功
        """
     
        
        # 构建查询条件
        stmt = select(self.model).where(
            self.model.contact == contact,
            self.model.code == code,
            self.model.send_status == True,
            self.model.is_delete == False,
            self.model.expire_time > datetime.now()
        )

        if scene:
            stmt = stmt.where(self.model.scene == scene)

        # 获取最近的一条验证码记录
        stmt = stmt.order_by(desc(self.model.send_time))
        result = await self.db.execute(stmt)
        code_log = result.scalar_one_or_none()

        if code_log:
            # 验证成功后软删除该验证码记录（设置 is_delete = True）
            code_log.is_delete = True
            code_log.delete_datetime = datetime.now()
            await self.db.flush()
            return True

        return False

    async def check_send_interval(self, contact: str, interval_seconds: int = 60, scene: str = None) -> bool:
        """
        检查是否满足发送间隔

        :param contact: 联系方式
        :param interval_seconds: 间隔秒数
        :param scene: 发送场景（可选）
        :return: 是否可以发送（True-可以，False-不行）
        """
        from datetime import timedelta

        from sqlalchemy import select, desc
        
        # 构建查询条件
        stmt = select(self.model).where(
            self.model.contact == contact,
            self.model.is_delete == False,
            self.model.send_time > datetime.now() - timedelta(seconds=interval_seconds)
        )

        if scene:
            stmt = stmt.where(self.model.scene == scene)

        # 获取最近的一条记录
        stmt = stmt.order_by(desc(self.model.send_time))
        result = await self.db.execute(stmt)
        recent_log = result.scalar_one_or_none()

        return recent_log is None
