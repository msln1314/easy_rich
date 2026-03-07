import pytest
from app.mcp.stock_mcp import StockMCP

@pytest.fixture
def stock_mcp():
    """创建StockMCP实例"""
    return StockMCP()

async def test_get_stock_info(stock_mcp, test_stock_code):
    """测试获取个股基本信息"""
    result = await stock_mcp.get_stock_info(test_stock_code)
    assert result is not None
    assert "股票代码" in result or "code" in result
    assert "股票简称" in result or "name" in result

async def test_get_stock_quote(stock_mcp, test_stock_code):
    """测试获取个股实时行情"""
    result = await stock_mcp.get_stock_quote(test_stock_code)
    assert result is not None
    assert "代码" in result or "code" in result
    assert "最新价" in result or "price" in result

async def test_get_stock_history(stock_mcp, test_stock_code):
    """测试获取个股历史行情"""
    result = await stock_mcp.get_stock_history(
        test_stock_code,
        period="daily",
        start_date="20230101",
        end_date="20230110"
    )
    assert result is not None
    assert len(result) > 0
    assert "trade_date" in result[0]  # 修改这里，使用正确的字段名称
    assert "open" in result[0]
    assert "close" in result[0]