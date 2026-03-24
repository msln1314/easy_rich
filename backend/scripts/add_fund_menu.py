#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
使用原生SQL添加基金分析功能菜单到数据库
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import db_getter


async def add_fund_menus():
    async_session = db_getter()
    db = await async_session.__anext__()

    try:
        result = await db.execute(
            text("SELECT id FROM sys_menu WHERE menu_name = '股票分析' LIMIT 1")
        )
        row = result.fetchone()

        if not row:
            print("未找到'股票分析'菜单")
            return

        parent_id = row[0]
        print(f"找到'股票分析'菜单，ID: {parent_id}")

        result = await db.execute(
            text("SELECT MAX(`order`) FROM sys_menu WHERE parent_id = :parent_id"),
            {"parent_id": parent_id},
        )
        row = result.fetchone()
        max_order = row[0] or 0
        print(f"当前最大排序值: {max_order}")

        result = await db.execute(
            text(
                "SELECT menu_name FROM sys_menu WHERE parent_id = :parent_id AND menu_name = '主力分析'"
            ),
            {"parent_id": parent_id},
        )
        existing = [r[0] for r in result.fetchall()]

        menus = [
            (
                "主力分析",
                "ep:data-analysis",
                "mainforce",
                "Vadmin/Stock/Fund/MainForce",
                max_order + 1,
            ),
        ]

        added = 0
        for name, icon, path, component, order in menus:
            if name in existing:
                print(f"菜单 '{name}' 已存在，跳过")
                continue

            await db.execute(
                text("""
                    INSERT INTO sys_menu 
                    (menu_name, icon, path, component, menu_type, parent_id, `order`, status, hidden, 
                     noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
                    VALUES 
                    (:menu_name, :icon, :path, :component, 'page', :parent_id, :order, 1, 0, 
                     0, 1, 0, 0, 1, 0, NOW(), NOW())
                """),
                {
                    "menu_name": name,
                    "icon": icon,
                    "path": path,
                    "component": component,
                    "parent_id": parent_id,
                    "order": order,
                },
            )
            print(f"添加菜单: {name}")
            added += 1

        await db.commit()
        print(f"\n成功添加 {added} 个菜单")

    except Exception as e:
        await db.rollback()
        print(f"添加菜单失败: {e}")
        raise
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(add_fund_menus())
