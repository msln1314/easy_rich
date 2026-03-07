import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """测试根路径接口"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "欢迎使用股票分析服务API"}

def test_get_stock_info():
    """测试获取个股基本信息接口"""
    stock_code = "000001"  # 平安银行
    response = client.get(f"/api/v1/stock/{stock_code}/info")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == stock_code
    assert "name" in data
    assert "industry" in data

def test_get_stock_quote():
    """测试获取个股实时行情接口"""
    stock_code = "000001"  # 平安银行
    response = client.get(f"/api/v1/stock/{stock_code}/quote")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == stock_code
    assert "price" in data
    assert "change_percent" in data

def test_get_stock_history():
    """测试获取个股历史行情数据接口"""
    stock_code = "000001"  # 平安银行
    response = client.get(f"/api/v1/stock/{stock_code}/history?period=daily&start_date=20230101&end_date=20230110")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["stock_code"] == stock_code
    assert "trade_date" in data[0]  # 修改这里，从"date"改为"trade_date"
    assert "open" in data[0]
    assert "close" in data[0]