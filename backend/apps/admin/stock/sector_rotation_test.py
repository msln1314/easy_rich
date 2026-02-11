#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/02/10
# @File           : sector_rotation_test.py
# @IDE            : PyCharm
# @desc           : 板块轮动分析测试数据生成器

import sys
import os
import asyncio
import random
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )
)

from apps.admin.stock.models.stock_board_industry import StockBoardIndustry
from db.db_base import DBSessionBase


async def generate_test_data():
    """生成板块轮动分析的测试数据"""

    # 板块名称列表
    sector_names = [
        "人工智能",
        "新能源汽车",
        "半导体",
        "医药生物",
        "新材料",
        "5G通信",
        "云计算",
        "大数据",
        "物联网",
        "区块链",
        "军工",
        "环保",
        "新能源",
        "光伏",
        "风电",
        "储能",
        "锂电池",
        "芯片",
        "软件",
        "互联网",
    ]

    async with DBSessionBase() as db:
        # 生成最近30天的数据
        for days_ago in range(30, 0, -1):
            date_at = datetime.now() - timedelta(days=days_ago)

            for i, sector_name in enumerate(sector_names):
                # 随机生成数据
                change_percent = round(random.uniform(-8, 8), 2)
                net_inflow = round(random.uniform(-20, 20), 2)
                total_amount = round(random.uniform(50, 500), 2)
                up_count = random.randint(5, 25)
                down_count = random.randint(5, 20)

                # 领涨股信息
                leading_stocks = [
                    "比亚迪",
                    "宁德时代",
                    "茅台",
                    "工商银行",
                    "中国平安",
                    "腾讯",
                    "阿里巴巴",
                    "中国移动",
                    "招商银行",
                    "中国石油",
                ]

                board = StockBoardIndustry(
                    board_name=sector_name,
                    board_code=f"BK{1000 + i}",
                    sequence=i + 1,
                    change_percent=change_percent,
                    average_price=round(random.uniform(10, 100), 2),
                    total_volume=round(random.uniform(100, 1000), 2),
                    total_amount=total_amount,
                    net_inflow=net_inflow,
                    up_count=up_count,
                    down_count=down_count,
                    leading_stock=random.choice(leading_stocks),
                    leading_stock_price=round(random.uniform(20, 200), 2),
                    leading_stock_change=round(random.uniform(-10, 10), 2),
                    leading_stock_code=f"60{1000 + random.randint(1, 9999):04d}",
                    date_at=date_at.date(),
                    data_time=datetime.now(),
                    data_from="test_data",
                )

                db.add(board)

            # 每个日期提交一次
            await db.commit()
            print(f"已生成 {date_at.strftime('%Y-%m-%d')} 的数据")

        print("测试数据生成完成！")


if __name__ == "__main__":
    asyncio.run(generate_test_data())
