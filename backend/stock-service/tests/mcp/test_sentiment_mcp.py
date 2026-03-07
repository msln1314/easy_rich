import pytest
from app.mcp.sentiment_mcp import SentimentMCP

@pytest.fixture
def sentiment_mcp():
    """创建SentimentMCP实例"""
    return SentimentMCP()

async def test_get_margin_details(sentiment_mcp):
    """测试获取融资融券明细数据"""
    # 使用一个有效的交易日期
    trade_date = "20230922"
    result = await sentiment_mcp.get_margin_details(trade_date)
    assert result is not None
    assert len(result) > 0
    assert "stock_code" in result[0]
    assert "stock_name" in result[0]
    assert "market" in result[0]
    assert "financing_balance" in result[0]
    assert "securities_balance" in result[0]

async def test_get_stock_hot_rank(sentiment_mcp):
    """测试获取股票热度排名数据"""
    result = await sentiment_mcp.get_stock_hot_rank()
    assert result is not None
    assert len(result) > 0
    assert "rank" in result[0]
    assert "stock_code" in result[0]
    assert "stock_name" in result[0]
    assert "price" in result[0]
    assert "change_percent" in result[0]

async def test_get_stock_hot_up_rank(sentiment_mcp):
    """测试获取股票飙升榜数据"""
    result = await sentiment_mcp.get_stock_hot_up_rank()
    assert result is not None
    assert len(result) > 0
    assert "rank_change" in result[0]
    assert "rank" in result[0]
    assert "stock_code" in result[0]
    assert "stock_name" in result[0]
    assert "price" in result[0]
    assert "change_percent" in result[0]

async def test_get_stock_hot_keywords(sentiment_mcp):
    """测试获取股票热门关键词数据"""
    # 使用一个常见的股票代码
    symbol = "SZ000665"
    result = await sentiment_mcp.get_stock_hot_keywords(symbol)
    assert result is not None
    assert len(result) > 0
    assert "time" in result[0]
    assert "stock_code" in result[0]
    assert "concept_name" in result[0]
    assert "concept_code" in result[0]
    assert "heat" in result[0]