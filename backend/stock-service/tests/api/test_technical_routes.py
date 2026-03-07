from fastapi.testclient import TestClient
from app.main import app

# 创建测试客户端
client = TestClient(app)

def test_get_chip_distribution():
    """测试获取股票筹码分布数据接口"""
    # 使用一个常见的股票代码
    symbol = "000001"
    response = client.get(f"/api/v1/technical/chip-distribution?symbol={symbol}")
    assert response.status_code == 200
    # 可以添加更多断言来验证响应内容
    data = response.json()
    assert isinstance(data, list)
    if data:  # 如果返回了数据
        assert "stock_code" in data[0]
        assert "profit_ratio" in data[0]
        assert "avg_cost" in data[0]
    assert "concentration_90" in data[0]
    
    # 测试前复权
    response = client.get(f"/api/v1/technical/chip-distribution?symbol={symbol}&adjust=qfq")
    assert response.status_code == 200
    
    # 测试后复权
    response = client.get(f"/api/v1/technical/chip-distribution?symbol={symbol}&adjust=hfq")
    assert response.status_code == 200