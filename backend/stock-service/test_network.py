#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
直接测试 akshare 接口（不使用补丁）
"""
# python 文件顶部添加2行代码 (已禁用)
# import akshare_proxy_patch
# akshare_proxy_patch.install_patch("101.201.173.125", "", 30)
import akshare as ak
import pandas as pd
from datetime import datetime

print("=" * 60)
print("直接测试 akshare 接口（无补丁）")
print("=" * 60)

try:
    # 获取A股实时行情
    start_time = datetime.now()
    df = ak.stock_zh_a_spot_em()
    end_time = datetime.now()

    elapsed = (end_time - start_time).total_seconds()

    print(f"\n✓ 数据获取成功！")
    print(f"  - 耗时: {elapsed:.2f} 秒")
    print(f"  - 数据行数: {len(df)}")

    print(f"\n前 5 行数据:")
    print(df.head())

except Exception as e:
    print(f"\n✗ 获取数据失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
