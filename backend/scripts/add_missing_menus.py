#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
添加缺失的菜单到数据库
运行方式: python scripts/add_missing_menus.py
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import db_getter


# 要添加的菜单列表
MISSING_MENUS = [
    {
        "menu_name": "每日排行",
        "icon": "mdi:format-list-numbered",
        "path": "daily-ranking",
        "component": "views/Vadmin/Stock/DailyRanking/DailyRanking",
        "order": 107,
    },
    {
        "menu_name": "智能选股",
        "icon": "mdi:filter",
        "path": "screener",
        "component": "views/Vadmin/Stock/Screener/Screener",
        "order": 108,
    },
    {
        "menu_name": "选股信号",
        "icon": "mdi:sine-wave",
        "path": "selection-signal",
        "component": "views/Vadmin/Stock/SelectionSignal/SelectionSignal",
        "order": 109,
    },
    {
        "menu_name": "形态识别",
        "icon": "mdi:chart-areaspline",
        "path": "pattern",
        "component": "views/Vadmin/Stock/Pattern/Pattern",
        "order": 110,
    },
    {
        "menu_name": "股票全景",
        "icon": "mdi:view-dashboard-outline",
        "path": "aggregate",
        "component": "views/Vadmin/Stock/Aggregate/Aggregate",
        "order": 111,
    },
    {
        "menu_name": "AI对话助手",
        "icon": "mdi:robot-outline",
        "path": "ai-chat",
        "component": "views/Vadmin/Stock/AI/Chat/Chat",
        "order": 112,
    },
    {
        "menu_name": "AI分析师工作台",
        "icon": "mdi:brain",
        "path": "ai-workbench",
        "component": "views/Vadmin/Stock/AI/Workbench/Workbench",
        "order": 113,
    },
    {
        "menu_name": "大模型配置",
        "icon": "mdi:cog-outline",
        "path": "llm-config",
        "component": "views/Vadmin/Stock/AI/LLMConfig/LLMConfig",
        "order": 114,
    },
]

PARENT_ID = 100  # 股票分析菜单的ID


async def add_missing_menus():
    """添加缺失的菜单"""
    async_session = db_getter()
    db = await async_session.__anext__()

    try:
        # 检查是否已存在
        for menu in MISSING_MENUS:
            result = await db.execute(
                text("SELECT id FROM sys_menu WHERE path = :path AND parent_id = :parent_id"),
                {"path": menu["path"], "parent_id": PARENT_ID}
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"菜单 '{menu['menu_name']}' 已存在 (ID: {existing})，跳过")
                continue

            # 插入新菜单
            sql = text("""
                INSERT INTO sys_menu
                (menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, is_delete, created_at, updated_at)
                VALUES
                (:menu_name, :icon, NULL, :component, :path, 1, 0, :order, 'page', :parent_id, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW())
            """)
            await db.execute(sql, {
                "menu_name": menu["menu_name"],
                "icon": menu["icon"],
                "component": menu["component"],
                "path": menu["path"],
                "order": menu["order"],
                "parent_id": PARENT_ID,
            })
            print(f"已添加菜单: {menu['menu_name']}")

        await db.commit()
        print("\n所有缺失菜单已添加完成!")

    except Exception as e:
        await db.rollback()
        print(f"错误: {e}")
        raise
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(add_missing_menus())