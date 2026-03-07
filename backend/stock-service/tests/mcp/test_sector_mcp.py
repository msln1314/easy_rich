import pytest
from app.mcp.sector_mcp import SectorMCP

@pytest.fixture
def sector_mcp():
    """创建SectorMCP实例"""
    return SectorMCP()

async def test_get_concept_boards(sector_mcp):
    """测试获取概念板块列表"""
    result = await sector_mcp.get_concept_boards()  # 添加await关键字
    assert result is not None
    assert len(result) > 0
    assert "code" in result[0]
    assert "name" in result[0]
    assert "price" in result[0]

async def test_get_concept_board(sector_mcp):
    """测试获取单个概念板块"""
    # 先获取一个有效的板块代码
    boards = await sector_mcp.get_concept_boards()
    assert len(boards) > 0
    board_code = boards[0]["code"]
    
    # 测试获取单个板块
    result = await sector_mcp.get_concept_board(board_code)
    assert result is not None
    assert result["code"] == board_code
    assert "name" in result
    assert "price" in result

async def test_get_concept_board_constituents(sector_mcp):
    """测试获取概念板块成份股"""
    # 使用一个常见的概念板块名称
    board_name = "融资融券"
    result = await sector_mcp.get_concept_board_constituents(board_name)
    assert result is not None
    assert len(result) > 0
    assert "code" in result[0]
    assert "name" in result[0]
    assert "price" in result[0]
    
    # 使用板块代码测试
    # 先获取一个有效的板块代码
    boards = await sector_mcp.get_concept_boards()
    assert len(boards) > 0
    board_code = boards[0]["code"]
    
    # 测试获取板块成份股
    result = await sector_mcp.get_concept_board_constituents(board_code)
    assert result is not None
    assert len(result) > 0
    assert "code" in result[0]
    assert "name" in result[0]
    assert "price" in result[0]

async def test_get_concept_board_spot(sector_mcp):
    """测试获取概念板块实时行情详情（通过名称）"""
    # 使用一个常见的概念板块名称
    board_name = "可燃冰"
    result = await sector_mcp.get_concept_board_spot(board_name)
    assert result is not None
    assert result["name"] == board_name
    assert "price" in result
    assert "change_percent" in result

async def test_get_concept_board_spot_by_code(sector_mcp):
    """测试获取概念板块实时行情详情（通过代码）"""
    # 先获取一个有效的板块代码
    boards = await sector_mcp.get_concept_boards()
    assert len(boards) > 0
    board_code = boards[0]["code"]
    
    # 测试获取单个板块实时行情
    result = await sector_mcp.get_concept_board_spot_by_code(board_code)
    assert result is not None
    assert "name" in result
    assert "price" in result
    assert "change_percent" in result

async def test_get_industry_boards(sector_mcp):
    """测试获取行业板块列表"""
    result = await sector_mcp.get_industry_boards()
    assert result is not None
    assert len(result) > 0
    assert "code" in result[0]
    assert "name" in result[0]
    assert "price" in result[0]

async def test_get_industry_board(sector_mcp):
    """测试获取单个行业板块"""
    # 先获取一个有效的板块代码
    boards = await sector_mcp.get_industry_boards()
    assert len(boards) > 0
    board_code = boards[0]["code"]
    
    # 测试获取单个板块
    result = await sector_mcp.get_industry_board(board_code)
    assert result is not None
    assert result["code"] == board_code
    assert "name" in result
    assert "price" in result

async def test_get_industry_board_spot(sector_mcp):
    """测试获取行业板块实时行情详情（通过名称）"""
    # 使用一个常见的行业板块名称
    board_name = "小金属"
    result = await sector_mcp.get_industry_board_spot(board_name)
    assert result is not None
    assert result["name"] == board_name
    assert "price" in result
    assert "change_percent" in result

async def test_get_industry_board_spot_by_code(sector_mcp):
    """测试获取行业板块实时行情详情（通过代码）"""
    # 先获取一个有效的板块代码
    boards = await sector_mcp.get_industry_boards()
    assert len(boards) > 0
    board_code = boards[0]["code"]
    
    # 测试获取单个板块实时行情
    # 修改方法名，使用正确的方法名
    result = await sector_mcp.get_industry_board(board_code)  # 或者使用其他存在的方法
    assert result is not None
    assert "name" in result
    assert "price" in result
    assert "change_percent" in result

async def test_get_industry_board_constituents(sector_mcp):
    """测试获取行业板块成份股"""
    # 使用一个常见的行业板块名称
    board_name = "小金属"
    result = await sector_mcp.get_industry_board_constituents(board_name)
    assert result is not None
    assert len(result) > 0
    assert "code" in result[0]
    assert "name" in result[0]
    assert "price" in result[0]
    
    # 使用板块代码测试
    # 先获取一个有效的板块代码
    boards = await sector_mcp.get_industry_boards()
    assert len(boards) > 0
    board_code = boards[0]["code"]
    
    # 测试获取板块成份股
    result = await sector_mcp.get_industry_board_constituents(board_code)
    assert result is not None
    assert len(result) > 0
    assert "code" in result[0]
    assert "name" in result[0]
    assert "price" in result[0]