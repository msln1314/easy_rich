"""测试 GM API 的板块获取功能"""

from gm import api as gm_api

print("测试 GM API 板块获取功能...")

# 测试 get_sector 方法
try:
    print("\n1. 测试 get_sector 方法:")
    # 尝试获取概念板块
    result = gm_api.get_sector(sector_type='concept')
    print(f"概念板块数量: {len(result) if result else 0}")
    if result:
        print(f"第一个板块: {result[0]}")
except Exception as e:
    print(f"get_sector(concept) 失败: {e}")

try:
    print("\n2. 测试 get_sector 方法 (industry):")
    result = gm_api.get_sector(sector_type='industry')
    print(f"行业板块数量: {len(result) if result else 0}")
    if result:
        print(f"第一个板块: {result[0]}")
except Exception as e:
    print(f"get_sector(industry) 失败: {e}")

try:
    print("\n3. 测试 get_sector 方法 (无参数):")
    result = gm_api.get_sector()
    print(f"板块数量: {len(result) if result else 0}")
    if result:
        print(f"第一个板块: {result[0]}")
except Exception as e:
    print(f"get_sector() 失败: {e}")

try:
    print("\n4. 测试 get_constituents 方法:")
    result = gm_api.get_constituents(sector_type='concept')
    print(f"成份股数量: {len(result) if result else 0}")
    if result:
        print(f"第一个成份股: {result[0]}")
except Exception as e:
    print(f"get_constituents 失败: {e}")

print("\n测试完成")
