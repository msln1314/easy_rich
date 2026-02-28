print("测试 gm 导入...")
try:
    from gm import api as gm_api
    print(f"导入成功: {type(gm_api)}")
    print(f"可用函数: history, current, get_instruments, get_constituents, get_sector")
except ImportError as e:
    print(f"导入失败: {e}")
except Exception as e:
    print(f"其他错误: {e}")
