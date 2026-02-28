"""测试 Tushare 导入和基本功能"""

import sys
sys.path.insert(0, 'd:/project/other/easy_rich/backend/stock-service')

print("测试 Tushare 导入...")
try:
    import tushare as ts
    print(f"Tushare 导入成功: {ts.__version__}")
except ImportError as e:
    print(f"Tushare 导入失败: {e}")
except Exception as e:
    print(f"其他错误: {e}")

print("\n测试 Tushare 服务初始化...")
try:
    from app.services.tushare_service import tushare_service
    print(f"Tushare 服务初始化成功")
    print(f"服务可用: {tushare_service.is_available()}")
except Exception as e:
    print(f"Tushare 服务初始化失败: {e}")

print("\n测试完成")
