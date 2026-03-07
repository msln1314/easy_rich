#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
测试直接请求东方财富网页
"""

import requests

url = "https://quote.eastmoney.com/center/gridlist.html#hs_a_board"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://quote.eastmoney.com/",
    "Upgrade-Insecure-Requests": "1",
}

print("=" * 60)
print(f"测试请求: {url}")
print("=" * 60)

try:
    response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)

    print(f"\n状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"内容长度: {len(response.content)} 字节")
    print(f"是否成功: {response.ok}")

    # 保存响应内容
    with open("test_response.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"\n✓ 响应已保存到: test_response.html")

    # 打印前500字符
    print(f"\n响应内容预览（前500字符）:")
    print(response.text[:500])

except Exception as e:
    print(f"\n✗ 请求失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
