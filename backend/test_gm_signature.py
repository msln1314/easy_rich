"""检查 GM API 的方法签名"""

from gm import api as gm_api
import inspect

print("检查 GM API 的方法签名...")

print("\n1. get_sector 方法:")
print(f"签名: {inspect.signature(gm_api.get_sector)}")
print(f"文档: {gm_api.get_sector.__doc__}")

print("\n2. get_constituents 方法:")
print(f"签名: {inspect.signature(gm_api.get_constituents)}")
print(f"文档: {gm_api.get_constituents.__doc__}")

print("\n3. get_instruments 方法:")
print(f"签名: {inspect.signature(gm_api.get_instruments)}")
print(f"文档: {gm_api.get_instruments.__doc__}")

print("\n4. current 方法:")
print(f"签名: {inspect.signature(gm_api.current)}")
print(f"文档: {gm_api.current.__doc__}")

print("\n5. history 方法:")
print(f"签名: {inspect.signature(gm_api.history)}")
print(f"文档: {gm_api.history.__doc__}")

print("\n检查完成")
