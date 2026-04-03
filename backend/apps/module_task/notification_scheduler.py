# -*- coding: utf-8 -*-
"""通知定时任务"""
import asyncio
from datetime import date

from core.database import session_factory
from apps.admin.notification.services import NotificationRuleService
from core.logger import logger


async def check_notification_rules():
    """
    检查通知规则并发送提醒

    每日定时执行，检查今天是否有需要发送的通知
    """
    logger.info("开始检查通知规则...")

    async with session_factory() as session:
        async with session.begin():
            db = session

            try:
                service = NotificationRuleService(db)
                result = await service.check_rules_for_date(date.today())

                logger.info(
                    f"通知规则检查完成: "
                    f"检查 {result['rules_checked']} 条规则, "
                    f"发送 {result['notifications_sent']} 条通知"
                )

                if result['errors']:
                    for error in result['errors']:
                        logger.error(f"通知规则错误: {error}")

                return result

            except Exception as e:
                logger.error(f"检查通知规则失败: {e}")
                return {
                    "date": str(date.today()),
                    "rules_checked": 0,
                    "notifications_sent": 0,
                    "errors": [str(e)]
                }


async def main_notification():
    """主函数 - 供定时任务调用"""
    return await check_notification_rules()


if __name__ == "__main__":
    asyncio.run(check_notification_rules())