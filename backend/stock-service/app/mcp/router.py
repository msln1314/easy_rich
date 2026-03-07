from fastapi import APIRouter
from app.mcp.stock_mcp import StockMCP  # 已修改
from app.mcp.index_mcp import IndexMCP  # 修改导入路径
from app.mcp.sector_mcp import SectorMCP  # 修改导入路径
from app.mcp.sentiment_mcp import SentimentMCP  # 修改导入路径
from app.mcp.technical_mcp import TechnicalMCP  # 修改导入路径
from app.mcp.news_mcp import NewsMCP  # 修改导入路径

mcp_router = APIRouter(prefix="/mcp")

# 实例化MCP类
stock_mcp = StockMCP()
index_mcp = IndexMCP()
sector_mcp = SectorMCP()
sentiment_mcp = SentimentMCP()
technical_mcp = TechnicalMCP()
news_mcp = NewsMCP()

# 股票MCP路由
@mcp_router.get("/stock/info/{stock_code}")
async def get_stock_info(stock_code: str):
    return stock_mcp.get_stock_info(stock_code)

@mcp_router.get("/stock/quote/{stock_code}")
async def get_stock_quote(stock_code: str):
    return stock_mcp.get_stock_quote(stock_code)

# 添加其他MCP接口路由...