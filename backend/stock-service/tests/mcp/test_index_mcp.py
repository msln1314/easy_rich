import pytest
from app.mcp.index_mcp import IndexMCP

@pytest.fixture
def index_mcp():
    """创建IndexMCP实例"""
    return IndexMCP()

async def test_get_index_quotes(index_mcp):
    """测试获取指数实时行情列表"""
    result = await index_mcp.get_index_quotes("沪深重要指数")
    assert result is not None
    assert len(result) > 0
    assert "code" in result[0]
    assert "name" in result[0]
    assert "price" in result[0]

async def test_get_index_quote(index_mcp):
    """测试获取单个指数实时行情"""
    index_code = "000001"  # 上证指数
    result = await index_mcp.get_index_quote(index_code)
    assert result is not None
    assert result["code"] == index_code
    assert "name" in result
    assert "price" in result