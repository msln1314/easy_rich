#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
测试 akshare stock_zh_a_spot_em() 接口
"""

# 导入本地版本的 akshare 代理补丁 (已禁用)
# try:
#     from app.utils.akshare_proxy_patch import test_proxy, install_patch_auto
#     import requests
#
#     POOL_URL = "http://122.51.65.65:5010"
#     MAX_RETRY = 3  # 最大重试次数
#
#     def get_working_proxy(max_attempts: int = 50) -> str:
#         """
#         循环获取代理并测试，直到找到可用的代理
#
#         Args:
#             max_attempts: 最大尝试次数，默认50次（防止无限循环）
#
#         Returns:
#             str: 可用的代理地址，如果都失败则返回None
#         """
#         for attempt in range(1, max_attempts + 1):
#             try:
#                 print(f"\n[步骤1] 从代理池获取代理... (第 {attempt}/{max_attempts} 次)")
#                 resp = requests.get(f"{POOL_URL}/get/", timeout=5)
#
#                 if resp.status_code == 200:
#                     proxy = resp.text.strip()
#                     if proxy and proxy not in ("no proxy", "null", ""):
#                         print(f"[步骤1] ✓ 获取到代理: {proxy}")
#
#                         # 【步骤2】立即测试代理
#                         print(f"[步骤2] 测试代理连通性...")
#                         if test_proxy(proxy=proxy, test_url="http://www.example.com"):
#                             print("[步骤2] ✓ 代理测试通过\n")
#                             return proxy
#                         else:
#                             print("[步骤2] ✗ 代理测试失败，丢弃该代理继续获取...")
#                             # 通知代理池删除失效代理
#                             try:
#                                 requests.get(f"{POOL_URL}/delete/?proxy={proxy.replace('http://', '')}", timeout=3)
#                             except:
#                                 pass
#                     else:
#                         print(f"[步骤1] ✗ 获取到无效代理: {proxy}")
#                 else:
#                     print(f"[步骤1] ✗ 获取代理失败，status={resp.status_code}")
#
#             except Exception as e:
#                 print(f"[步骤1] ✗ 获取代理异常: {e}")
#
#             # 短暂等待后继续下一次获取
#             wait = 0.5 if attempt < 10 else 1.0  # 前10次快试，之后慢点
#             print(f"[步骤1] 等待 {wait}s 后继续获取...")
#             import time
#             time.sleep(wait)
#
#         print(f"\n[步骤1] ✗ 已尝试 {max_attempts} 次仍未获取到可用代理")
#         return None
#
#     # 【步骤1+2】循环获取并测试代理，直到找到可用的
#     proxy = get_working_proxy()
#
#     # 【步骤3】安装补丁
#     print("[步骤3] 安装 akshare 代理补丁...")
#     if proxy:
#         install_patch_auto(proxy=proxy, timeout=60, min_interval=1.5)
#         print(f"✓ akshare 代理补丁已安装（自动Cookie+固定代理模式），代理: {proxy}")
#     else:
#         install_patch_auto(timeout=60, min_interval=1.0)
#         print("✓ akshare 代理补丁已安装（自动Cookie+直连模式）")
#
# except Exception as e:
#     print(f"✗ 错误: {e}")
#     import traceback
#     traceback.print_exc()

import akshare as ak
import pandas as pd
from datetime import datetime


print("=" * 60)
print("开始获取A股实时行情数据...")
print("=" * 60)


""" 创建代理字典 """
# proxies = {
#     "http": "http://xxx.con:xxx",
#     "https": "https://xxx.con:xxx"
# }
# """ 创建代理字典 """
# AkshareConfig.set_proxies(proxies)

try:
    # 获取A股实时行情
    start_time = datetime.now()
    df = ak.stock_zh_a_spot_em()
    end_time = datetime.now()

    elapsed = (end_time - start_time).total_seconds()

    print(f"\n✓ 数据获取成功！")
    print(f"  - 耗时: {elapsed:.2f} 秒")
    print(f"  - 数据行数: {len(df)}")
    print(f"  - 数据列数: {len(df.columns)}")

    print(f"\n前 5 行数据:")
    print(df.head())

    print(f"\n列名:")
    print(df.columns.tolist())

    # 统计信息
    print(f"\n统计信息:")
    print(f"  - 平均涨跌幅: {df['涨跌幅'].mean():.2f}%")
    print(f"  - 上涨家数: {len(df[df['涨跌幅'] > 0])}")
    print(f"  - 下跌家数: {len(df[df['涨跌幅'] < 0])}")
    print(f"  - 平盘家数: {len(df[df['涨跌幅'] == 0])}")

    # 保存到文件
    output_file = "stock_data.xlsx"
    df.to_excel(output_file, index=False)
    print(f"\n✓ 数据已保存到: {output_file}")

except Exception as e:
    print(f"\n✗ 获取数据失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)