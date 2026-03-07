import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_index_quotes():
    """测试获取指数实时行情列表接口"""
    response = client.get("/api/v1/index/quotes?symbol=沪深重要指数")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "code" in data[0]
    assert "name" in data[0]
    assert "price" in data[0]

def test_get_index_quote():
    """测试获取单个指数实时行情接口"""
    index_code = "000001"  # 上证指数
    response = client.get(f"/api/v1/index/{index_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == index_code
    assert "name" in data
    assert "price" in data