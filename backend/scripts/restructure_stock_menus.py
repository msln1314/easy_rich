#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
重构股票分析菜单结构，按功能维度分组
运行方式: python scripts/restructure_stock_menus.py
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import db_getter


# 新的菜单分组结构
# 格式: {分组名: {icon, order, children: [{name, path, component, order}]}}
NEW_MENU_STRUCTURE = {
    "行情概览": {
        "icon": "mdi:chart-box-outline",
        "order": 1,
        "children": [
            {"name": "大盘座舱", "path": "marketDashboard", "component": "views/Vadmin/Stock/MarketDashboard/MarketDashboard", "order": 1},
            {"name": "大盘云图", "path": "cloud-map", "component": "views/Vadmin/Stock/MarketCloudMap/MarketCloudMap", "order": 2},
            {"name": "板块轮动", "path": "sector-rotation", "component": "views/Vadmin/Stock/SectorRotation/SectorRotation", "order": 3},
            {"name": "每日排行", "path": "daily-ranking", "component": "views/Vadmin/Stock/DailyRanking/DailyRanking", "order": 4},
        ]
    },
    "选股工具": {
        "icon": "mdi:filter-outline",
        "order": 2,
        "children": [
            {"name": "智能选股", "path": "screener", "component": "views/Vadmin/Stock/Screener/Screener", "order": 1},
            {"name": "选股信号", "path": "selection-signal", "component": "views/Vadmin/Stock/SelectionSignal/SelectionSignal", "order": 2},
            {"name": "形态识别", "path": "pattern", "component": "views/Vadmin/Stock/Pattern/Pattern", "order": 3},
            {"name": "条件选股策略", "path": "condition", "component": "views/Vadmin/Stock/MonitorCondition/MonitorCondition", "order": 4},
        ]
    },
    "个股分析": {
        "icon": "mdi:chart-line-variant",
        "order": 3,
        "children": [
            {"name": "个股分析", "path": "analysis", "component": "views/Vadmin/Stock/Analysis/Analysis", "order": 1},
            {"name": "股票全景", "path": "aggregate", "component": "views/Vadmin/Stock/Aggregate/Aggregate", "order": 2},
            {"name": "个股预测", "path": "prediction", "component": "views/Vadmin/Stock/Prediction/Prediction", "order": 3},
            {"name": "分析报表", "path": "analysis_report", "component": "views/Vadmin/Stock/Analysis/Report", "order": 4},
        ]
    },
    "资金监控": {
        "icon": "mdi:currency-usd",
        "order": 4,
        "children": [
            {"name": "主力分析", "path": "mainforce", "component": "views/Vadmin/Stock/Fund/MainForce", "order": 1},
            {"name": "异动监控", "path": "watchlist", "component": "views/Vadmin/Stock/Watchlist/WatchList", "order": 2},
            {"name": "监听策略", "path": "policy", "component": "views/Vadmin/Stock/Policy/monitor", "order": 3},
            {"name": "策略统计", "path": "policy_report", "component": None, "order": 4},
        ]
    },
    "资讯数据": {
        "icon": "mdi:newspaper-variant-outline",
        "order": 5,
        "children": [
            {"name": "财经新闻", "path": "news", "component": "views/Vadmin/Stock/News/News", "order": 1},
            {"name": "热门新闻", "path": "hot_news", "component": "views/Vadmin/Stock/HotNews/HotNews", "order": 2},
            {"name": "财经日历", "path": "calendar", "component": "views/Vadmin/Stock/InvestCalendar/InvestCalendar", "order": 3},
        ]
    },
    "复盘管理": {
        "icon": "mdi:notebook-outline",
        "order": 6,
        "children": [
            {"name": "复盘工作台", "path": "review", "component": "views/Vadmin/Stock/Review/Review", "order": 1},
            {"name": "心得经验库", "path": "experience", "component": "views/Vadmin/Stock/Review/Experience", "order": 2},
            {"name": "雷区基线", "path": "rules", "component": "views/Vadmin/Stock/Review/Rules", "order": 3},
        ]
    },
    "AI分析": {
        "icon": "mdi:robot-outline",
        "order": 7,
        "children": [
            {"name": "AI对话助手", "path": "ai-chat", "component": "views/Vadmin/Stock/AI/Chat/Chat", "order": 1},
            {"name": "AI分析师工作台", "path": "ai-workbench", "component": "views/Vadmin/Stock/AI/Workbench/Workbench", "order": 2},
            {"name": "大模型配置", "path": "llm-config", "component": "views/Vadmin/Stock/AI/LLMConfig/LLMConfig", "order": 3},
        ]
    },
    "我的股票": {
        "icon": "mdi:star-outline",
        "order": 8,
        "children": [
            {"name": "自选股", "path": "my_stock", "component": "views/Vadmin/Stock/My/Stock", "order": 1},
            {"name": "股票列表", "path": "base_info", "component": "views/Vadmin/Stock/BaseInfo/BaseInfo", "order": 2},
        ]
    },
}

STOCK_PARENT_ID = 100  # 股票分析菜单的ID


async def restructure_menus():
    """重构菜单结构"""
    async_session = db_getter()
    db = await async_session.__anext__()

    try:
        # 1. 获取所有当前股票模块下的直接子菜单（非分组菜单）
        result = await db.execute(
            text("SELECT id, menu_name, path, component, `order` FROM sys_menu WHERE parent_id = :parent_id ORDER BY `order`"),
            {"parent_id": STOCK_PARENT_ID}
        )
        existing_menus = {row[2]: {"id": row[0], "name": row[1], "component": row[3], "order": row[4]} for row in result.fetchall()}
        print(f"找到 {len(existing_menus)} 个现有菜单")

        # 2. 创建新的分组菜单
        for group_name, group_info in NEW_MENU_STRUCTURE.items():
            # 检查分组是否已存在
            result = await db.execute(
                text("SELECT id FROM sys_menu WHERE menu_name = :name AND parent_id = :parent_id"),
                {"name": group_name, "parent_id": STOCK_PARENT_ID}
            )
            existing_group = result.scalar_one_or_none()

            if existing_group:
                group_id = existing_group
                print(f"分组 '{group_name}' 已存在 (ID: {group_id})")
            else:
                # 创建分组菜单
                await db.execute(
                    text("""
                        INSERT INTO sys_menu
                        (menu_name, icon, path, component, status, hidden, `order`, menu_type, parent_id, is_delete, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
                        VALUES
                        (:menu_name, :icon, :path, '#', 1, 0, :order, 'dir', :parent_id, 0, 0, 1, 0, 0, 0, 1, NOW(), NOW())
                    """),
                    {
                        "menu_name": group_name,
                        "icon": group_info["icon"],
                        "path": group_name.lower().replace(" ", "-"),
                        "order": group_info["order"],
                        "parent_id": STOCK_PARENT_ID,
                    }
                )
                # 获取新创建的分组ID
                result = await db.execute(text("SELECT LAST_INSERT_ID()"))
                group_id = result.scalar()
                print(f"创建分组 '{group_name}' (ID: {group_id})")

            # 3. 将子菜单移动到分组下或创建新菜单
            for child in group_info["children"]:
                child_path = child["path"]

                if child_path in existing_menus:
                    # 移动现有菜单到分组下
                    old_menu = existing_menus[child_path]
                    await db.execute(
                        text("UPDATE sys_menu SET parent_id = :new_parent_id, `order` = :order WHERE id = :id"),
                        {"new_parent_id": group_id, "order": child["order"], "id": old_menu["id"]}
                    )
                    print(f"  移动 '{child['name']}' 到 '{group_name}'")
                else:
                    # 创建新菜单
                    if child["component"]:
                        await db.execute(
                            text("""
                                INSERT INTO sys_menu
                                (menu_name, icon, path, component, status, hidden, `order`, menu_type, parent_id, is_delete, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
                                VALUES
                                (:menu_name, NULL, :path, :component, 1, 0, :order, 'page', :parent_id, 0, 0, 1, 0, 0, 0, 1, NOW(), NOW())
                            """),
                            {
                                "menu_name": child["name"],
                                "path": child_path,
                                "component": child["component"],
                                "order": child["order"],
                                "parent_id": group_id,
                            }
                        )
                        print(f"  创建 '{child['name']}' 在 '{group_name}' 下")

        await db.commit()
        print("\n菜单重构完成!")

    except Exception as e:
        await db.rollback()
        print(f"错误: {e}")
        raise
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(restructure_menus())