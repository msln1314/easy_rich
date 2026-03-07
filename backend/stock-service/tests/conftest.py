import pytest
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 可以在这里添加全局fixture
@pytest.fixture(scope="session")
def test_stock_code():
    """返回用于测试的股票代码"""
    return "000001"  # 平安银行