#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2025/02/15
# @File : stock_monitor_service.py
# @IDE : PyCharm
# @desc : 股票监听策略服务

from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from apps.admin.stock import models, crud


class StockMonitorService:
    """股票监听策略服务"""

    STRATEGY_TYPE_MAP = {
        "limit_up": "涨停",
        "limit_down": "跌停",
        "open_board": "开板",
        "turnover": "换手",
        "breakout": "突破",
        "rebound": "反弹",
    }

    @staticmethod
    async def get_matched_strategies(
        db: AsyncSession, stock_code: str, stock_data: dict
    ) -> list:
        """
        获取匹配股票数据的策略
        :param db: 数据库会话
        :param stock_code: 股票代码
        :param stock_data: 股票实时数据
        :return: 匹配的策略列表
        """
        strategies = await crud.StockMonitorStrategyDal(db).get_by_stock_code(
            stock_code
        )
        matched = []

        for strategy in strategies:
            if await StockMonitorService._check_strategy_match(strategy, stock_data):
                matched.append(strategy)

        return matched

    @staticmethod
    async def _check_strategy_match(strategy: dict, stock_data: dict) -> bool:
        """检查策略是否匹配"""
        strategy_type = strategy.get("strategy_type")

        if strategy_type == "limit_up":
            return await StockMonitorService._check_limit_up(strategy, stock_data)
        elif strategy_type == "limit_down":
            return await StockMonitorService._check_limit_down(strategy, stock_data)
        elif strategy_type == "open_board":
            return await StockMonitorService._check_open_board(strategy, stock_data)
        elif strategy_type == "turnover":
            return await StockMonitorService._check_turnover(strategy, stock_data)
        elif strategy_type == "breakout":
            return await StockMonitorService._check_breakout(strategy, stock_data)
        elif strategy_type == "rebound":
            return await StockMonitorService._check_rebound(strategy, stock_data)

        return False

    @staticmethod
    async def _check_limit_up(strategy: dict, stock_data: dict) -> bool:
        """检查涨停策略"""
        change_percent = stock_data.get("change_percent", 0)
        is_limit_up = stock_data.get("is_limit_up", False)

        if is_limit_up or change_percent >= 9.9:
            trigger_percent_min = strategy.get("trigger_percent_min")
            trigger_percent_max = strategy.get("trigger_percent_max")

            if trigger_percent_min and change_percent < trigger_percent_min:
                return False
            if trigger_percent_max and change_percent > trigger_percent_max:
                return False

            return True

        return False

    @staticmethod
    async def _check_limit_down(strategy: dict, stock_data: dict) -> bool:
        """检查跌停策略"""
        change_percent = stock_data.get("change_percent", 0)
        is_limit_down = stock_data.get("is_limit_down", False)

        if is_limit_down or change_percent <= -9.9:
            trigger_percent_min = strategy.get("trigger_percent_min")
            trigger_percent_max = strategy.get("trigger_percent_max")

            if trigger_percent_min and change_percent < trigger_percent_min:
                return False
            if trigger_percent_max and change_percent > trigger_percent_max:
                return False

            return True

        return False

    @staticmethod
    async def _check_open_board(strategy: dict, stock_data: dict) -> bool:
        """检查开板策略"""
        is_limit_up = stock_data.get("is_limit_up", False)
        was_limit_up = stock_data.get("was_limit_up", False)

        if was_limit_up and not is_limit_up:
            return True

        return False

    @staticmethod
    async def _check_turnover(strategy: dict, stock_data: dict) -> bool:
        """检查换手率策略"""
        turnover_rate = stock_data.get("turnover_rate", 0)

        trigger_value_min = strategy.get("trigger_value_min")
        trigger_value_max = strategy.get("trigger_value_max")

        if trigger_value_min and turnover_rate < trigger_value_min:
            return False
        if trigger_value_max and turnover_rate > trigger_value_max:
            return False

        return True

    @staticmethod
    async def _check_breakout(strategy: dict, stock_data: dict) -> bool:
        """检查突破策略"""
        price = stock_data.get("price", 0)
        breakthrough_price = strategy.get("trigger_value_min")

        if breakthrough_price and price >= breakthrough_price:
            return True

        return False

    @staticmethod
    async def _check_rebound(strategy: dict, stock_data: dict) -> bool:
        """检查反弹策略"""
        change_percent = stock_data.get("change_percent", 0)
        price = stock_data.get("price", 0)
        prev_price = stock_data.get("prev_price", 0)

        if prev_price > 0:
            direction = strategy.get("strategy_config", "{}")
            direction_dict = eval(direction) if direction else {}

            if direction_dict.get("direction") == "up" and change_percent > 0:
                trigger_percent_min = strategy.get("trigger_percent_min")
                if trigger_percent_min and change_percent < trigger_percent_min:
                    return False
                return True
            elif direction_dict.get("direction") == "down" and change_percent < 0:
                trigger_percent_max = strategy.get("trigger_percent_max")
                if trigger_percent_max and change_percent > trigger_percent_max:
                    return False
                return True

        return False

    @staticmethod
    async def check_cooldown(strategy: dict) -> tuple[bool, Optional[datetime]]:
        """
        检查策略是否在冷却期内
        :param strategy: 策略数据
        :return: (是否在冷却期内, 下次可触发时间)
        """
        last_trigger_time = strategy.get("last_trigger_time")
        cooldown_minutes = strategy.get("cooldown_minutes", 60)
        cooldown_type = strategy.get("cooldown_type", "same_day")

        if not last_trigger_time:
            return False, None

        last_trigger = datetime.fromisoformat(last_trigger_time.replace("Z", "+00:00"))
        now = datetime.now()

        if cooldown_type == "same_day":
            if last_trigger.date() == now.date():
                next_time = datetime(now.year, now.month, now.day, 23, 59, 59)
                return True, next_time
        else:
            next_time = last_trigger + timedelta(minutes=cooldown_minutes)
            if now < next_time:
                return True, next_time

        return False, None

    @staticmethod
    def format_trigger_condition(strategy: dict, stock_data: dict) -> str:
        """格式化触发条件描述"""
        strategy_type = strategy.get("strategy_type")
        type_name = StockMonitorService.STRATEGY_TYPE_MAP.get(
            strategy_type, strategy_type
        )

        conditions = []

        if strategy_type in ["limit_up", "limit_down", "rebound"]:
            change_percent = stock_data.get("change_percent", 0)
            conditions.append(f"涨跌幅: {change_percent:.2f}%")

        if strategy_type == "turnover":
            turnover_rate = stock_data.get("turnover_rate", 0)
            conditions.append(f"换手率: {turnover_rate:.2f}%")

        if strategy_type == "breakout":
            price = stock_data.get("price", 0)
            conditions.append(f"价格: {price:.2f}")

        return f"{type_name} {' '.join(conditions)}"

    @staticmethod
    async def should_notify(strategy: dict, trigger_count: int) -> bool:
        """
        检查是否应该发送通知
        :param strategy: 策略数据
        :param trigger_count: 当前触发次数
        :return: 是否应该发送通知
        """
        notify_enabled = strategy.get("notify_enabled", 1)
        if not notify_enabled:
            return False

        notify_trigger_count = strategy.get("notify_trigger_count", 1)
        notify_type = strategy.get("notify_type", "once")

        if notify_type == "once":
            return trigger_count <= notify_trigger_count
        elif notify_type == "always":
            return True
        elif notify_type == "interval":
            interval = strategy.get("cooldown_minutes", 60)
            return (
                trigger_count <= notify_trigger_count or trigger_count % interval == 0
            )

        return trigger_count <= notify_trigger_count


async def create_trigger_log(
    db: AsyncSession, strategy: dict, stock_data: dict, trigger_count: int
) -> models.StockMonitorLog:
    """创建触发日志"""
    log = models.StockMonitorLog(
        strategy_id=strategy["id"],
        strategy_name=strategy["name"],
        user_id=strategy["user_id"],
        stock_code=stock_data.get("stock_code", ""),
        stock_name=stock_data.get("stock_name", ""),
        strategy_type=strategy["strategy_type"],
        trigger_time=datetime.now(),
        trigger_count=trigger_count,
        trigger_condition=StockMonitorService.format_trigger_condition(
            strategy, stock_data
        ),
        trigger_value=stock_data.get("price"),
        trigger_percent=stock_data.get("change_percent"),
        price=stock_data.get("price"),
        change_percent=stock_data.get("change_percent"),
        volume=stock_data.get("volume"),
        turnover_rate=stock_data.get("turnover_rate"),
        notify_status=0,
        notify_method=strategy.get("notify_method", "system"),
        strategy_config_snapshot=strategy.get("strategy_config"),
    )

    db.add(log)
    await db.flush()

    return log
