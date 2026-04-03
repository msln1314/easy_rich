# -*- coding: utf-8 -*-
"""统一通知服务"""
import json
import logging
import random
import string
from datetime import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import NotificationChannel, NotificationLog, NotificationTemplate
from .senders import get_sender

logger = logging.getLogger(__name__)


class NotificationService:
    """统一通知服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def send_notification(
        self,
        user_id: int,
        title: str,
        content: str,
        channels: List[str] = None,
        template_code: str = None,
        extra_data: dict = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送通知

        Args:
            user_id: 用户ID
            title: 通知标题
            content: 通知内容
            channels: 指定渠道列表，为空则使用用户默认渠道
            template_code: 模板编码
            extra_data: 额外数据

        Returns:
            发送结果
        """
        results = {}

        # 获取用户的通知渠道
        user_channels = await self._get_user_channels(user_id, channels)

        if not user_channels:
            logger.warning(f"用户 {user_id} 没有可用的通知渠道")
            return {"success": False, "error": "没有可用的通知渠道", "results": {}}

        for channel in user_channels:
            result = await self._send_to_channel(
                user_id=user_id,
                channel=channel,
                title=title,
                content=content,
                template_code=template_code,
                extra_data=extra_data,
                **kwargs
            )
            results[channel.channel_type] = result

        # 判断整体是否成功
        success = any(r.get("success") for r in results.values())

        return {
            "success": success,
            "results": results,
        }

    async def _send_to_channel(
        self,
        user_id: int,
        channel: NotificationChannel,
        title: str,
        content: str,
        template_code: str = None,
        extra_data: dict = None,
        **kwargs
    ) -> Dict[str, Any]:
        """发送到指定渠道"""
        # 创建日志记录
        log = NotificationLog(
            user_id=user_id,
            channel_type=channel.channel_type,
            template_code=template_code,
            title=title,
            content=content,
            status="pending",
            extra_data=extra_data,
        )
        self.db.add(log)
        await self.db.flush()

        try:
            # 获取发送器
            sender = get_sender(channel.channel_type)
            if not sender:
                raise ValueError(f"不支持的通知渠道: {channel.channel_type}")

            # 解析渠道配置
            config = channel.channel_config or {}
            if isinstance(config, str):
                config = json.loads(config)

            # 发送通知
            result = await sender.send(
                user_id=user_id,
                title=title,
                content=content,
                config=config,
                db=self.db,
                extra_data=extra_data,
                **kwargs
            )

            # 更新日志
            log.status = "sent" if result.get("success") else "failed"
            log.error_msg = result.get("error_msg")
            log.sent_at = datetime.now() if result.get("success") else None

            await self.db.flush()
            return result

        except Exception as e:
            logger.error(f"发送通知失败: {e}")
            log.status = "failed"
            log.error_msg = str(e)
            await self.db.flush()
            return {"success": False, "error_msg": str(e)}

    async def _get_user_channels(
        self,
        user_id: int,
        channel_types: List[str] = None
    ) -> List[NotificationChannel]:
        """获取用户的通知渠道"""
        sql = select(NotificationChannel).where(
            and_(
                NotificationChannel.user_id == user_id,
                NotificationChannel.is_enabled == True,
                NotificationChannel.verified == True,
                NotificationChannel.is_delete == False,
            )
        )

        if channel_types:
            sql = sql.where(NotificationChannel.channel_type.in_(channel_types))

        sql = sql.order_by(NotificationChannel.id)

        result = await self.db.scalars(sql)
        return list(result.all())

    async def create_channel(
        self,
        user_id: int,
        channel_type: str,
        channel_name: str,
        channel_config: dict,
    ) -> NotificationChannel:
        """创建通知渠道"""
        channel = NotificationChannel(
            user_id=user_id,
            channel_type=channel_type,
            channel_name=channel_name,
            channel_config=channel_config,
        )
        self.db.add(channel)
        await self.db.flush()
        return channel

    async def verify_channel(
        self,
        channel: NotificationChannel,
        code: str
    ) -> bool:
        """验证渠道"""
        if channel.verify_code != code:
            return False

        channel.verified = True
        channel.verified_at = datetime.now()
        channel.verify_code = None
        await self.db.flush()
        return True

    async def generate_verify_code(
        self,
        channel: NotificationChannel
    ) -> str:
        """生成验证码"""
        code = "".join(random.choices(string.digits, k=6))
        channel.verify_code = code
        await self.db.flush()
        return code

    async def test_channel(
        self,
        channel: NotificationChannel,
        title: str = "测试通知",
        content: str = "这是一条测试通知消息"
    ) -> Dict[str, Any]:
        """测试发送"""
        config = channel.channel_config or {}
        if isinstance(config, str):
            config = json.loads(config)

        sender = get_sender(channel.channel_type)
        if not sender:
            return {"success": False, "error_msg": f"不支持的渠道: {channel.channel_type}"}

        return await sender.send(
            user_id=channel.user_id,
            title=title,
            content=content,
            config=config,
            db=self.db,
        )

    async def render_template(
        self,
        template_code: str,
        variables: dict
    ) -> Optional[Dict[str, str]]:
        """渲染模板"""
        result = await self.db.execute(
            select(NotificationTemplate).where(
                NotificationTemplate.code == template_code
            )
        )
        template = result.scalar_one_or_none()

        if not template:
            return None

        title = template.title_template
        content = template.content_template

        # 替换变量
        for key, value in variables.items():
            title = title.replace(f"{{{{{key}}}}}", str(value))
            content = content.replace(f"{{{{{key}}}}}", str(value))

        return {"title": title, "content": content}