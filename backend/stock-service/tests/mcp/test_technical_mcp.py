import pytest
from app.mcp.technical_mcp import TechnicalMCP

@pytest.fixture
def technical_mcp():
    """创建TechnicalMCP实例"""
    return TechnicalMCP()

@pytest.mark.asyncio
async def test_get_chip_distribution(technical_mcp):
    """测试获取股票筹码分布数据"""
    # 使用一个常见的股票代码
    symbol = "000001"
    result = await technical_mcp.get_chip_distribution(symbol)
    assert result is not None
    assert len(result) > 0
    assert "stock_code" in result[0]
    assert "profit_ratio" in result[0]
    assert "avg_cost" in result[0]
    assert "concentration_90" in result[0]
    
    # 测试前复权
    result = await technical_mcp.get_chip_distribution(symbol, "qfq")
    assert result is not None
    assert len(result) > 0
    
    # 测试后复权
    result = await technical_mcp.get_chip_distribution(symbol, "hfq")
    assert result is not None
    assert len(result) > 0