import logging
from datetime import datetime, date, timedelta
from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.stock_calendar_event import StockCalendarEvent
from ..models.stock_event_reminder import StockEventReminder

logger = logging.getLogger(__name__)


class ReminderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_active_reminders(self) -> List[StockEventReminder]:
        result = await self.db.execute(
            select(StockEventReminder).where(
                and_(
                    StockEventReminder.is_active == 1,
                    StockEventReminder.is_delete == False,
                )
            )
        )
        return result.scalars().all()

    async def check_and_send_reminders(self) -> dict:
        today = date.today()
        reminders_sent = 0
        errors = []

        reminders = await self.get_active_reminders()

        for reminder in reminders:
            try:
                event = await self._get_event(reminder.event_id)
                if not event:
                    continue

                remind_date = event.event_date - timedelta(days=reminder.remind_days)

                if remind_date == today:
                    await self._send_reminder(reminder, event)
                    reminder.last_remind_at = datetime.now()
                    reminders_sent += 1

            except Exception as e:
                logger.error(f"处理提醒失败: {e}")
                errors.append(str(e))

        await self.db.commit()

        return {
            "reminders_sent": reminders_sent,
            "total_checked": len(reminders),
            "errors": errors,
        }

    async def _get_event(self, event_id: int) -> StockCalendarEvent:
        result = await self.db.execute(
            select(StockCalendarEvent).where(
                and_(
                    StockCalendarEvent.id == event_id,
                    StockCalendarEvent.is_delete == False,
                )
            )
        )
        return result.scalar_one_or_none()

    async def _send_reminder(
        self, reminder: StockEventReminder, event: StockCalendarEvent
    ):
        message = self._build_reminder_message(event, reminder)

        if reminder.remind_type == "system":
            await self._send_system_notification(reminder.user_id, message)
        elif reminder.remind_type == "email":
            await self._send_email_notification(reminder.user_id, message)

        logger.info(f"已发送提醒: 用户{reminder.user_id} - {event.title}")

    def _build_reminder_message(
        self, event: StockCalendarEvent, reminder: StockEventReminder
    ) -> str:
        lines = [
            "【投资日历提醒】",
            f"股票: {event.stock_name} ({event.stock_code})",
            f"事件: {event.title}",
            f"日期: {event.event_date}",
        ]

        if event.ai_suggestion:
            lines.append(f"AI建议: {event.ai_suggestion}")

        lines.append("\n请及时关注!")

        return "\n".join(lines)

    async def _send_system_notification(self, user_id: int, message: str):
        logger.info(f"[系统通知] 用户 {user_id}: {message}")

    async def _send_email_notification(self, user_id: int, message: str):
        logger.info(f"[邮件通知] 用户 {user_id}: {message}")
