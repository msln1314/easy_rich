from fastapi.testclient import TestClient
from app.main import app

# 创建测试客户端
client = TestClient(app)

def test_get_global_finance_news():
    """测试获取全球财经快讯数据接口"""
    response = client.get("/api/v1/news/global-finance")
    assert response.status_code == 200
    # 可以添加更多断言来验证响应内容
    data = response.json()
    assert isinstance(data, list)
    if data:  # 如果返回了数据
        assert "title" in data[0]
        assert "summary" in data[0]
        assert "publish_time" in data[0]
    assert "link" in data[0]

def test_get_interactive_questions():
    """测试获取互动易提问数据接口"""
    # 使用一个常见的股票代码
    symbol = "002594"
    response = client.get(f"/api/v1/news/interactive/questions?symbol={symbol}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "stock_code" in data[0]
    assert "stock_name" in data[0]
    assert "question" in data[0]
    assert "questioner" in data[0]
    assert "question_time" in data[0]

def test_get_cls_telegraph():
    """测试获取财联社电报数据接口"""
    # 测试全部类型
    response = client.get("/api/v1/news/cls-telegraph?symbol=全部")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "title" in data[0]
    assert "content" in data[0]
    assert "publish_date" in data[0]
    assert "publish_time" in data[0]
    
    # 测试重点类型
    response = client.get("/api/v1/news/cls-telegraph?symbol=重点")
    assert response.status_code == 200