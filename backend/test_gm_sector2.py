"""测试 GM API 的板块获取功能 - 第二轮"""

from gm import api as gm_api

print("测试 GM API 板块获取功能（第二轮）...")

# 测试 get_sector 方法
try:
    print("\n1. 测试 get_sector 方法 (需要 code 参数):")
    # 尝试获取某个板块
    result = gm_api.get_sector(code='BK0001')
    print(f"结果: {result}")
except Exception as e:
    print(f"get_sector 失败: {e}")

try:
    print("\n2. 测试 get_constituents 方法:")
    # 尝试获取成份股
    result = gm_api.get_constituents(code='BK0001')
    print(f"成份股数量: {len(result) if result else 0}")
    if result:
        print(f"第一个成份股: {result[0]}")
except Exception as e:
    print(f"get_constituents 失败: {e}")

try:
    print("\n3. 测试 get_instruments 方法:")
    # 尝试获取所有股票
    result = gm_api.get_instruments(sec_type='stock')
    print(f"股票数量: {len(result) if result else 0}")
    if result:
        print(f"第一个股票: {result[0]}")
except Exception as e:
    print(f"get_instruments 失败: {e}")

print("\n测试完成")
