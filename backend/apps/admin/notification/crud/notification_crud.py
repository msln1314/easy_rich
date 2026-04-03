# -*- coding: utf-8 -*-
"""通知模块 CRUD"""
from typing import List, Tuple, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from ..models import NotificationChannel, NotificationTemplate, NotificationLog, SystemNotification


class NotificationChannelDal(DalBase):
    """通知渠道 CRUD"""

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = NotificationChannel

    async def get_user_channels(
        self,
        user_id: int,
        channel_type: str = None,
        enabled_only: bool = False,
        verified_only: bool = False
    ) -> List[NotificationChannel]:
        """获取用户的通知渠道"""
        sql = select(NotificationChannel).where(
            and_(
                NotificationChannel.user_id == user_id,
                NotificationChannel.is_delete == False,
            )
        )

        if channel_type:
            sql = sql.where(NotificationChannel.channel_type == channel_type)

        if enabled_only:
            sql = sql.where(NotificationChannel.is_enabled == True)

        if verified_only:
            sql = sql.where(NotificationChannel.verified == True)

        sql = sql.order_by(NotificationChannel.id)

        result = await self.db.scalars(sql)
        return list(result.all())


class NotificationTemplateDal(DalBase):
    """通知模板 CRUD"""

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = NotificationTemplate

    async def get_by_code(self, code: str) -> Optional[NotificationTemplate]:
        """根据编码获取模板"""
        result = await self.db.execute(
            select(NotificationTemplate).where(NotificationTemplate.code == code)
        )
        return result.scalar_one_or_none()

    async def get_system_templates(self) -> List[NotificationTemplate]:
        """获取系统内置模板"""
        result = await self.db.scalars(
            select(NotificationTemplate).where(NotificationTemplate.is_system == True)
        )
        return list(result.all())


class NotificationLogDal(DalBase):
    """通知日志 CRUD"""

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = NotificationLog

    async def get_user_logs(
        self,
        user_id: int,
        status: str = None,
        channel_type: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[NotificationLog]]:
        """获取用户的通知日志"""
        sql = select(NotificationLog).where(
            NotificationLog.user_id == user_id
        )

        if status:
            sql = sql.where(NotificationLog.status == status)

        if channel_type:
            sql = sql.where(NotificationLog.channel_type == channel_type)

        # 计数
        count_sql = select(NotificationLog.id).where(
            NotificationLog.user_id == user_id
        )
        if status:
            count_sql = count_sql.where(NotificationLog.status == status)
        if channel_type:
            count_sql = count_sql.where(NotificationLog.channel_type == channel_type)

        count_result = await self.db.execute(count_sql)
        total = len(count_result.all())

        # 分页
        sql = sql.order_by(NotificationLog.created_at.desc())
        sql = sql.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.scalars(sql)
        items = list(result.all())

        return total, items


class SystemNotificationDal(DalBase):
    """系统通知 CRUD"""

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = SystemNotification

    async def get_user_notifications(
        self,
        user_id: int,
        is_read: bool = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[SystemNotification]]:
        """获取用户的系统通知"""
        sql = select(SystemNotification).where(
            and_(
                SystemNotification.user_id == user_id,
                SystemNotification.is_delete == False,
            )
        )

        if is_read is not None:
            sql = sql.where(SystemNotification.is_read == is_read)

        # 计数
        count_sql = select(SystemNotification.id).where(
            and_(
                SystemNotification.user_id == user_id,
                SystemNotification.is_delete == False,
            )
        )
        if is_read is not None:
            count_sql = count_sql.where(SystemNotification.is_read == is_read)

        count_result = await self.db.execute(count_sql)
        total = len(count_result.all())

        # 分页
        sql = sql.order_by(SystemNotification.created_at.desc())
        sql = sql.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.scalars(sql)
        items = list(result.all())

        return total, items

    async def get_unread_count(self, user_id: int) -> int:
        """获取未读数量"""
        result = await self.db.execute(
            select(SystemNotification.id).where(
                and_(
                    SystemNotification.user_id == user_id,
                    SystemNotification.is_read == False,
                    SystemNotification.is_delete == False,
                )
            )
        )
        return len(result.all())

    async def mark_as_read(self, notification_id: int, user_id: int) -> bool:
        """标记为已读"""
        from datetime import datetime

        result = await self.db.execute(
            select(SystemNotification).where(
                and_(
                    SystemNotification.id == notification_id,
                    SystemNotification.user_id == user_id,
                )
            )
        )
        notification = result.scalar_one_or_none()

        if notification:
            notification.is_read = True
            notification.read_at = datetime.now()
            await self.db.flush()
            return True

        return False

    async def mark_all_as_read(self, user_id: int) -> int:
        """标记全部已读"""
        from datetime import datetime

        result = await self.db.execute(
            select(SystemNotification).where(
                and_(
                    SystemNotification.user_id == user_id,
                    SystemNotification.is_read == False,
                    SystemNotification.is_delete == False,
                )
            )
        )
        notifications = list(result.all())

        now = datetime.now()
        for notification in notifications:
            notification.is_read = True
            notification.read_at = now

        await self.db.flush()
        return len(notifications)