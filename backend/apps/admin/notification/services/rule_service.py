# -*- coding: utf-8 -*-
"""通知规则服务 - 处理财经日历的通知规则"""
import json
import logging
from datetime import date, timedelta
from typing import List, Dict, Any, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.notification_rule import NotificationRule
from .notification_service import NotificationService

logger = logging.getLogger(__name__)


class NotificationRuleService:
    """通知规则服务"""

    # 规则类型对应的默认事件类型
    RULE_EVENT_TYPE_MAP = {
        "holiday": ["holiday", "market_closed"],
        "earnings": ["earnings", "earnings_preview"],
        "dividend": ["dividend", "ex_dividend"],
        "unlock": ["unlock", "lift_ban"],
        "custom": [],
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self.notification_service = NotificationService(db)

    async def get_user_rules(
        self,
        user_id: int,
        rule_type: str = None,
        enabled_only: bool = True
    ) -> List[NotificationRule]:
        """获取用户的规则列表"""
        sql = select(NotificationRule).where(
            NotificationRule.user_id == user_id,
            NotificationRule.is_delete == False,
        )

        if enabled_only:
            sql = sql.where(NotificationRule.is_enabled == True)

        if rule_type:
            sql = sql.where(NotificationRule.rule_type == rule_type)

        sql = sql.order_by(NotificationRule.priority.desc(), NotificationRule.id)

        result = await self.db.scalars(sql)
        return list(result.all())

    async def create_rule(
        self,
        user_id: int,
        rule_name: str,
        rule_type: str,
        condition_config: dict,
        action_config: dict,
        event_type_filter: str = None,
        stock_codes: List[str] = None,
        priority: int = 0,
        valid_from: date = None,
        valid_to: date = None,
    ) -> NotificationRule:
        """创建通知规则"""
        rule = NotificationRule(
            user_id=user_id,
            rule_name=rule_name,
            rule_type=rule_type,
            event_type_filter=event_type_filter,
            stock_codes=json.dumps(stock_codes) if stock_codes else None,
            condition_config=condition_config,
            action_config=action_config,
            priority=priority,
            valid_from=valid_from,
            valid_to=valid_to,
        )
        self.db.add(rule)
        await self.db.flush()
        return rule

    async def check_rules_for_date(
        self,
        target_date: date = None
    ) -> Dict[str, Any]:
        """
        检查指定日期的所有规则并发送通知

        Args:
            target_date: 目标日期，默认今天

        Returns:
            检查结果统计
        """
        if target_date is None:
            target_date = date.today()

        stats = {
            "date": str(target_date),
            "rules_checked": 0,
            "notifications_sent": 0,
            "errors": [],
        }

        # 获取所有启用的规则
        sql = select(NotificationRule).where(
            and_(
                NotificationRule.is_enabled == True,
                NotificationRule.is_delete == False,
            )
        )
        result = await self.db.scalars(sql)
        rules = list(result.all())

        for rule in rules:
            try:
                stats["rules_checked"] += 1

                # 检查有效期
                if rule.valid_from and target_date < rule.valid_from:
                    continue
                if rule.valid_to and target_date > rule.valid_to:
                    continue

                # 根据规则类型检查
                should_notify = await self._check_rule(rule, target_date)

                if should_notify:
                    await self._send_rule_notification(rule, should_notify)
                    stats["notifications_sent"] += 1

            except Exception as e:
                error_msg = f"规则 {rule.rule_name} 检查失败: {e}"
                logger.error(error_msg)
                stats["errors"].append(error_msg)

        return stats

    async def _check_rule(
        self,
        rule: NotificationRule,
        target_date: date
    ) -> Optional[Dict[str, Any]]:
        """
        检查单个规则是否触发

        Returns:
            触发信息，None 表示未触发
        """
        condition = rule.condition_config or {}

        if rule.rule_type == "holiday":
            return await self._check_holiday_rule(rule, condition, target_date)
        elif rule.rule_type == "earnings":
            return await self._check_earnings_rule(rule, condition, target_date)
        elif rule.rule_type == "dividend":
            return await self._check_dividend_rule(rule, condition, target_date)
        elif rule.rule_type == "unlock":
            return await self._check_unlock_rule(rule, condition, target_date)
        elif rule.rule_type == "custom":
            return await self._check_custom_rule(rule, condition, target_date)

        return None

    async def _check_holiday_rule(
        self,
        rule: NotificationRule,
        condition: dict,
        target_date: date
    ) -> Optional[Dict[str, Any]]:
        """检查节假日规则"""
        days_before = condition.get("days_before", 2)

        # 查询未来的节假日事件
        from ..models.stock_calendar_event import StockCalendarEvent

        event_date = target_date + timedelta(days=days_before)

        sql = select(StockCalendarEvent).where(
            and_(
                StockCalendarEvent.event_type.in_(["holiday", "market_closed"]),
                StockCalendarEvent.event_date == event_date,
                StockCalendarEvent.is_delete == False,
            )
        )

        result = await self.db.scalars(sql)
        events = list(result.all())

        if not events:
            return None

        return {
            "events": events,
            "message": condition.get("message", f"距离节假日还有{days_before}天，注意仓位管理"),
        }

    async def _check_earnings_rule(
        self,
        rule: NotificationRule,
        condition: dict,
        target_date: date
    ) -> Optional[Dict[str, Any]]:
        """检查财报规则"""
        days_before = condition.get("days_before", 3)
        watchlist_only = condition.get("watchlist_only", True)

        from ..models.stock_calendar_event import StockCalendarEvent

        event_date = target_date + timedelta(days=days_before)

        sql = select(StockCalendarEvent).where(
            and_(
                StockCalendarEvent.event_type == "earnings",
                StockCalendarEvent.event_date == event_date,
                StockCalendarEvent.is_delete == False,
            )
        )

        if watchlist_only:
            sql = sql.where(StockCalendarEvent.is_in_watchlist == 1)

        # 股票代码过滤
        if rule.stock_codes:
            stock_codes = json.loads(rule.stock_codes)
            sql = sql.where(StockCalendarEvent.stock_code.in_(stock_codes))

        result = await self.db.scalars(sql)
        events = list(result.all())

        if not events:
            return None

        return {
            "events": events,
            "message": condition.get("message", f"以下股票将在{days_before}天后发布财报"),
        }

    async def _check_dividend_rule(
        self,
        rule: NotificationRule,
        condition: dict,
        target_date: date
    ) -> Optional[Dict[str, Any]]:
        """检查分红除权规则"""
        days_before = condition.get("days_before", 1)

        from ..models.stock_calendar_event import StockCalendarEvent

        event_date = target_date + timedelta(days=days_before)

        sql = select(StockCalendarEvent).where(
            and_(
                StockCalendarEvent.event_type.in_(["dividend", "ex_dividend"]),
                StockCalendarEvent.event_date == event_date,
                StockCalendarEvent.is_delete == False,
            )
        )

        if rule.stock_codes:
            stock_codes = json.loads(rule.stock_codes)
            sql = sql.where(StockCalendarEvent.stock_code.in_(stock_codes))

        result = await self.db.scalars(sql)
        events = list(result.all())

        if not events:
            return None

        return {
            "events": events,
            "message": condition.get("message", "以下股票即将分红除权"),
        }

    async def _check_unlock_rule(
        self,
        rule: NotificationRule,
        condition: dict,
        target_date: date
    ) -> Optional[Dict[str, Any]]:
        """检查解禁规则"""
        days_before = condition.get("days_before", 5)
        watchlist_only = condition.get("watchlist_only", True)

        from ..models.stock_calendar_event import StockCalendarEvent

        event_date = target_date + timedelta(days=days_before)

        sql = select(StockCalendarEvent).where(
            and_(
                StockCalendarEvent.event_type == "unlock",
                StockCalendarEvent.event_date == event_date,
                StockCalendarEvent.is_delete == False,
            )
        )

        if watchlist_only:
            sql = sql.where(StockCalendarEvent.is_in_watchlist == 1)

        if rule.stock_codes:
            stock_codes = json.loads(rule.stock_codes)
            sql = sql.where(StockCalendarEvent.stock_code.in_(stock_codes))

        result = await self.db.scalars(sql)
        events = list(result.all())

        if not events:
            return None

        return {
            "events": events,
            "message": condition.get("message", "以下股票即将解禁"),
        }

    async def _check_custom_rule(
        self,
        rule: NotificationRule,
        condition: dict,
        target_date: date
    ) -> Optional[Dict[str, Any]]:
        """检查自定义规则"""
        # 自定义规则的检查逻辑
        event_types = rule.event_type_filter.split(",") if rule.event_type_filter else []
        days_before = condition.get("days_before", 1)

        from ..models.stock_calendar_event import StockCalendarEvent

        event_date = target_date + timedelta(days=days_before)

        sql = select(StockCalendarEvent).where(
            and_(
                StockCalendarEvent.event_date == event_date,
                StockCalendarEvent.is_delete == False,
            )
        )

        if event_types:
            sql = sql.where(StockCalendarEvent.event_type.in_(event_types))

        if rule.stock_codes:
            stock_codes = json.loads(rule.stock_codes)
            sql = sql.where(StockCalendarEvent.stock_code.in_(stock_codes))

        result = await self.db.scalars(sql)
        events = list(result.all())

        if not events:
            return None

        return {
            "events": events,
            "message": condition.get("message", "您关注的事件即将发生"),
        }

    async def _send_rule_notification(
        self,
        rule: NotificationRule,
        trigger_info: Dict[str, Any]
    ):
        """发送规则通知"""
        action = rule.action_config or {}
        events = trigger_info.get("events", [])
        message = trigger_info.get("message", "")

        # 构建通知内容
        event_list = []
        for event in events[:5]:  # 最多显示5个
            event_list.append(f"- {event.stock_name} ({event.stock_code}): {event.title}")

        if len(events) > 5:
            event_list.append(f"- ...还有 {len(events) - 5} 个")

        content = f"{message}\n\n" + "\n".join(event_list)

        # 发送通知
        channels = action.get("channels", ["system"])
        template_code = action.get("template_code")

        await self.notification_service.send_notification(
            user_id=rule.user_id,
            title=rule.rule_name,
            content=content,
            channels=channels,
            template_code=template_code,
            extra_data={
                "rule_id": rule.id,
                "rule_type": rule.rule_type,
                "event_count": len(events),
            }
        )

        # 更新规则最后触发时间
        rule.last_triggered_at = date.today().isoformat()
        await self.db.flush()