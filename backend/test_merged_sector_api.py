#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
板块轮动分析接口测试脚本（合并后版本）
"""

import asyncio
import aiohttp
import json
from datetime import datetime


async def test_sector_apis():
    """测试板块轮动分析相关接口"""

    base_url = "http://localhost:9000/api/v1/stock/board_industry/sector/rotation"

    async with aiohttp.ClientSession() as session:
        print("=" * 50)
        print("开始测试板块轮动分析接口（合并后版本）")
        print("=" * 50)

        # 测试1: 板块排行榜
        print("\n1. 测试板块排行榜接口")
        try:
            async with session.get(f"{base_url}/ranking") as response:
                data = await response.json()
                print(f"状态码: {response.status}")
                if data.get("code") == 200:
                    print(f"数据条数: {data.get('count', 0)}")
                    if data.get("data"):
                        print(
                            f"第一名: {data['data'][0]['sector_name']} - 涨跌幅: {data['data'][0]['change_rate']}%"
                        )
                else:
                    print(f"错误: {data}")
        except Exception as e:
            print(f"请求失败: {e}")

        # 测试2: 资金流向趋势
        print("\n2. 测试资金流向趋势接口")
        try:
            async with session.get(f"{base_url}/trend") as response:
                data = await response.json()
                print(f"状态码: {response.status}")
                if data.get("code") == 200:
                    print(f"趋势数据条数: {len(data.get('data', []))}")
                    if data.get("data"):
                        latest_date = data["data"][0]["date"]
                        sectors_count = len(data["data"][0]["sectors"])
                        print(f"最新日期: {latest_date}, 板块数量: {sectors_count}")
                else:
                    print(f"错误: {data}")
        except Exception as e:
            print(f"请求失败: {e}")

        # 测试3: 热力图数据
        print("\n3. 测试热力图数据接口")
        try:
            async with session.get(f"{base_url}/heatmap") as response:
                data = await response.json()
                print(f"状态码: {response.status}")
                if data.get("code") == 200:
                    print(f"热力图数据条数: {len(data.get('data', []))}")
                    if data.get("data"):
                        print(
                            f"第一个板块: {data['data'][0]['sector_name']} - 涨跌幅: {data['data'][0]['change_rate']}%"
                        )
                else:
                    print(f"错误: {data}")
        except Exception as e:
            print(f"请求失败: {e}")

        # 测试4: 板块列表
        print("\n4. 测试板块列表接口")
        try:
            async with session.get(f"{base_url}/list") as response:
                data = await response.json()
                print(f"状态码: {response.status}")
                if data.get("code") == 200:
                    print(f"板块数量: {len(data.get('data', []))}")
                    if data.get("data"):
                        print(
                            f"第一个板块: {data['data'][0]['sector_name']} ({data['data'][0]['sector_code']})"
                        )
                else:
                    print(f"错误: {data}")
        except Exception as e:
            print(f"请求失败: {e}")

        # 测试5: 板块详情
        print("\n5. 测试板块详情接口")
        try:
            async with session.get(f"{base_url}/detail/人工智能") as response:
                data = await response.json()
                print(f"状态码: {response.status}")
                if data.get("code") == 200:
                    detail = data.get("data", {})
                    if isinstance(detail, dict):
                        print(f"板块名称: {detail.get('sector_name')}")
                        print(f"涨跌幅: {detail.get('change_rate')}%")
                        print(f"净流入: {detail.get('net_inflow')}亿元")
                    else:
                        print(f"返回数据: {detail}")
                else:
                    print(f"错误: {data}")
        except Exception as e:
            print(f"请求失败: {e}")

        # 测试6: 分析概览
        print("\n6. 测试分析概览接口")
        try:
            async with session.get(f"{base_url}/analysis/summary") as response:
                data = await response.json()
                print(f"状态码: {response.status}")
                if data.get("code") == 200:
                    summary = data.get("data", {})
                    if isinstance(summary, dict):
                        print(f"总板块数: {summary.get('total_sectors')}")
                        print(f"上涨板块: {summary.get('rising_sectors')}")
                        print(f"下跌板块: {summary.get('falling_sectors')}")
                        best_sector = summary.get("best_sector", {})
                        worst_sector = summary.get("worst_sector", {})
                        if isinstance(best_sector, dict):
                            print(f"最佳板块: {best_sector.get('sector_name')}")
                        if isinstance(worst_sector, dict):
                            print(f"最差板块: {worst_sector.get('sector_name')}")
                    else:
                        print(f"返回数据: {summary}")
                else:
                    print(f"错误: {data}")
        except Exception as e:
            print(f"请求失败: {e}")

        print("\n" + "=" * 50)
        print("接口测试完成！")
        print("=" * 50)


async def main():
    """主函数"""
    print("请确保后端服务运行在 http://localhost:9000")
    print("如果服务未运行，请先启动后端服务：")
    print("cd backend && python main.py run")
    print()

    try:
        await test_sector_apis()
    except Exception as e:
        print(f"测试过程中出现错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())
