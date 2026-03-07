import pytest
from app.mcp.news_mcp import NewsMCP

@pytest.fixture
def news_mcp():
    """创建NewsMCP实例"""
    return NewsMCP()

async def test_get_global_finance_news(news_mcp):
    """测试获取全球财经快讯数据"""
    result = await news_mcp.get_global_finance_news()
    assert result is not None
    assert len(result) > 0
    assert "title" in result[0]
    assert "summary" in result[0]
    assert "publish_time" in result[0]
    assert "link" in result[0]

async def test_get_cls_telegraph(news_mcp):
    """测试获取财联社电报数据"""
    # 测试全部类型
    result = await news_mcp.get_cls_telegraph(symbol="全部")
    assert result is not None
    assert len(result) > 0
    assert "title" in result[0]
    assert "content" in result[0]
    assert "publish_date" in result[0]
    assert "publish_time" in result[0]
    
    # 测试重点类型
    result = await news_mcp.get_cls_telegraph(symbol="重点")  # 添加await关键字
    assert result is not None
    assert len(result) > 0

async def test_get_interactive_questions(news_mcp):
    """测试获取互动易提问数据"""
    # 使用一个常见的股票代码
    symbol = "002594"
    result = await news_mcp.get_interactive_questions(symbol)
    assert result is not None
    assert len(result) > 0
    assert "stock_code" in result[0]
    assert "stock_name" in result[0]
    assert "question" in result[0]
    assert "questioner" in result[0]
    assert "question_time" in result[0]