#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import db_getter


async def add_cloud_map_menu():
    async_session = db_getter()
    db = await async_session.__anext__()

    try:
        parent_id = 100
        print(f"Using parent menu ID: {parent_id}")

        result = await db.execute(
            text("SELECT MAX(`order`) FROM sys_menu WHERE parent_id = :parent_id"),
            {"parent_id": parent_id},
        )
        row = result.fetchone()
        max_order = row[0] or 0
        print(f"Current max order: {max_order}")

        result = await db.execute(
            text(
                "SELECT menu_name FROM sys_menu WHERE parent_id = :parent_id AND path = 'cloud-map'"
            ),
            {"parent_id": parent_id},
        )
        existing = result.fetchone()

        if existing:
            print("Menu 'cloud-map' already exists, skipping")
            return

        await db.execute(
            text("""
                INSERT INTO sys_menu 
                (menu_name, icon, path, component, menu_type, parent_id, `order`, status, hidden, 
                 noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, is_delete, created_at, updated_at)
                VALUES 
                (:menu_name, :icon, :path, :component, 'page', :parent_id, :order, 1, 0, 
                 0, 1, 0, 0, 1, 0, 0, NOW(), NOW())
            """),
            {
                "menu_name": "\u5927\u76d8\u4e91\u56fe",
                "icon": "ep:grid",
                "path": "cloud-map",
                "component": "Vadmin/Stock/MarketCloudMap/MarketCloudMap",
                "parent_id": parent_id,
                "order": max_order + 1,
            },
        )
        print("Added menu: cloud-map")

        await db.commit()
        print("\nMenu added successfully")

    except Exception as e:
        await db.rollback()
        print(f"Failed to add menu: {e}")
        raise
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(add_cloud_map_menu())
