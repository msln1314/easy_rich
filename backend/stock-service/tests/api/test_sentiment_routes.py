from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_margin_details():
    """测试获取融资融券明细数据接口"""
    # 使用一个有效的交易日期
    trade_date = "20230922"
    response = client.get(f"/api/v1/sentiment/margin/details?trade_date={trade_date}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "stock_code" in data[0]
    assert "stock_name" in data[0]
    assert "market" in data[0]
    assert "financing_balance" in data[0]
    assert "securities_balance" in data[0]
    
    # 测试无效日期格式
    invalid_date = "2023-09-22"
    response = client.get(f"/api/v1/sentiment/margin/details?trade_date={invalid_date}")
    assert response.status_code == 400


def test_get_stock_hot_rank():
    """测试获取股票热度排名数据接口"""
    response = client.get("/api/v1/sentiment/stock/hot-rank")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "rank" in data[0]
    assert "stock_code" in data[0]
    assert "stock_name" in data[0]
    assert "price" in data[0]
    assert "change_percent" in data[0]


def test_get_stock_hot_up_rank():
    """测试获取股票飙升榜数据接口"""
    response = client.get("/api/v1/sentiment/stock/hot-up-rank")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "rank_change" in data[0]
    assert "rank" in data[0]
    assert "stock_code" in data[0]
    assert "stock_name" in data[0]
    assert "price" in data[0]
    assert "change_percent" in data[0]


def test_get_stock_hot_keywords():
    """测试获取股票热门关键词数据接口"""
    # 使用一个常见的股票代码
    symbol = "SZ000665"
    response = client.get(f"/api/v1/sentiment/stock/hot-keywords?symbol={symbol}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "time" in data[0]
    assert "stock_code" in data[0]
    assert "concept_name" in data[0]
    assert "concept_code" in data[0]
    assert "heat" in data[0]