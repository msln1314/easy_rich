# -*- coding: utf-8 -*-
"""通知发送器"""
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from application.settings import settings

logger = logging.getLogger(__name__)


class BaseSender(ABC):
    """通知发送器基类"""

    @abstractmethod
    async def send(
        self,
        user_id: int,
        title: str,
        content: str,
        config: dict,
        db: AsyncSession = None,
        **kwargs
    ) -> dict:
        """
        发送通知

        Returns:
            dict: {"success": bool, "error_msg": str|None}
        """
        pass

    def get_name(self) -> str:
        """获取发送器名称"""
        return self.__class__.__name__


class EmailSender(BaseSender):
    """邮件发送器 - 使用 SMTP"""

    async def send(
        self,
        user_id: int,
        title: str,
        content: str,
        config: dict,
        db: AsyncSession = None,
        **kwargs
    ) -> dict:
        """
        发送邮件

        Args:
            config: {"address": "user@example.com"}
        """
        try:
            import aiosmtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            to_email = config.get("address")
            if not to_email:
                return {"success": False, "error_msg": "未配置邮箱地址"}

            # 创建邮件
            message = MIMEMultipart()
            message["From"] = settings.SMTP_FROM or settings.SMTP_USER
            message["To"] = to_email
            message["Subject"] = title

            # 添加正文
            message.attach(MIMEText(content, "plain", "utf-8"))

            # 发送邮件
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                use_tls=True,
            )

            logger.info(f"邮件发送成功: 用户{user_id} -> {to_email}")
            return {"success": True, "error_msg": None}

        except ImportError:
            logger.warning("aiosmtplib 未安装，无法发送邮件")
            return {"success": False, "error_msg": "邮件服务未配置(aiosmtplib未安装)"}
        except Exception as e:
            logger.error(f"邮件发送失败: {e}")
            return {"success": False, "error_msg": str(e)}


class WechatSender(BaseSender):
    """微信推送发送器 - 使用第三方服务(Server酱/WxPusher)"""

    async def send(
        self,
        user_id: int,
        title: str,
        content: str,
        config: dict,
        db: AsyncSession = None,
        **kwargs
    ) -> dict:
        """
        发送微信推送

        Args:
            config: {
                "push_type": "serverchan" | "wxpusher" | "custom",
                "sendkey": "xxx",  # Server酱
                "token": "xxx",    # WxPusher
                "uid": "xxx",      # WxPusher 用户ID
                "url": "xxx"       # 自定义推送URL
            }
        """
        push_type = config.get("push_type", "serverchan")

        try:
            if push_type == "serverchan":
                return await self._send_serverchan(title, content, config)
            elif push_type == "wxpusher":
                return await self._send_wxpusher(title, content, config)
            elif push_type == "custom":
                return await self._send_custom(title, content, config)
            else:
                return {"success": False, "error_msg": f"不支持的推送类型: {push_type}"}

        except Exception as e:
            logger.error(f"微信推送发送失败: {e}")
            return {"success": False, "error_msg": str(e)}

    async def _send_serverchan(self, title: str, content: str, config: dict) -> dict:
        """Server酱推送"""
        sendkey = config.get("sendkey")
        if not sendkey:
            return {"success": False, "error_msg": "未配置Server酱SendKey"}

        url = f"https://sctapi.ftqq.com/{sendkey}.send"

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                data={"title": title, "desp": content},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                result = await resp.json()
                if result.get("code") == 0:
                    logger.info(f"Server酱推送成功: {title}")
                    return {"success": True, "error_msg": None}
                else:
                    error_msg = result.get("message", "未知错误")
                    logger.error(f"Server酱推送失败: {error_msg}")
                    return {"success": False, "error_msg": error_msg}

    async def _send_wxpusher(self, title: str, content: str, config: dict) -> dict:
        """WxPusher推送"""
        token = config.get("token")
        uid = config.get("uid")
        if not token or not uid:
            return {"success": False, "error_msg": "未配置WxPusher Token或UID"}

        url = "https://wxpusher.zjiecode.com/api/send/message/simple-push"

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json={
                    "appToken": token,
                    "content": f"{title}\n\n{content}",
                    "summary": title,
                    "contentType": 1,  # 文本
                    "uids": [uid],
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                result = await resp.json()
                if result.get("code") == 1000:
                    logger.info(f"WxPusher推送成功: {title}")
                    return {"success": True, "error_msg": None}
                else:
                    error_msg = result.get("msg", "未知错误")
                    logger.error(f"WxPusher推送失败: {error_msg}")
                    return {"success": False, "error_msg": error_msg}

    async def _send_custom(self, title: str, content: str, config: dict) -> dict:
        """自定义推送URL"""
        url = config.get("url")
        if not url:
            return {"success": False, "error_msg": "未配置自定义推送URL"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json={"title": title, "content": content},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status == 200:
                    logger.info(f"自定义推送成功: {title}")
                    return {"success": True, "error_msg": None}
                else:
                    error_msg = f"HTTP {resp.status}"
                    logger.error(f"自定义推送失败: {error_msg}")
                    return {"success": False, "error_msg": error_msg}


class SystemSender(BaseSender):
    """系统内通知发送器"""

    async def send(
        self,
        user_id: int,
        title: str,
        content: str,
        config: dict,
        db: AsyncSession = None,
        **kwargs
    ) -> dict:
        """
        发送系统内通知

        Args:
            config: {
                "notification_type": "info" | "warning" | "success" | "error",
                "link": "可选的跳转链接"
            }
        """
        if db is None:
            return {"success": False, "error_msg": "数据库会话未提供"}

        try:
            from ..models import SystemNotification

            notification = SystemNotification(
                user_id=user_id,
                title=title,
                content=content,
                notification_type=config.get("notification_type", "info"),
                link=config.get("link"),
                extra_data=kwargs.get("extra_data"),
            )
            db.add(notification)
            await db.flush()

            logger.info(f"系统通知创建成功: 用户{user_id} - {title}")
            return {"success": True, "error_msg": None}

        except Exception as e:
            logger.error(f"系统通知创建失败: {e}")
            return {"success": False, "error_msg": str(e)}


# 发送器注册表
SENDERS = {
    "email": EmailSender(),
    "wechat": WechatSender(),
    "system": SystemSender(),
}


def get_sender(channel_type: str) -> Optional[BaseSender]:
    """获取发送器"""
    return SENDERS.get(channel_type)