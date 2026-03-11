from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

# API 标签描述
tags_metadata = [
    {
        "name": "stock",
        "description": "股票相关接口，包括股票基本信息、实时行情、历史数据等",
    },
    {
        "name": "index",
        "description": "大盘指数接口，包括上证指数、深证成指、创业板指等",
    },
    {
        "name": "sector",
        "description": "板块相关接口，包括行业板块、概念板块行情数据",
    },
    {
        "name": "sentiment",
        "description": "市场情绪接口，包括涨跌统计、市场热度等",
    },
    {
        "name": "technical",
        "description": "技术分析接口，包括筹码分布、技术指标等",
    },
    {
        "name": "news",
        "description": "新闻资讯接口，包括互动问答、财经新闻等",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
## 股票分析服务 API

基于 AKShare 数据的股票分析服务，提供以下功能：

### 功能模块
- **股票数据**: 获取个股基本信息、实时行情、历史K线数据
- **大盘指数**: 获取上证指数、深证成指、创业板指等主要指数数据
- **板块行情**: 获取行业板块、概念板块的涨跌排行
- **市场情绪**: 市场涨跌统计、热度分析
- **技术分析**: 筹码分布、技术指标计算
- **新闻资讯**: 财经新闻、互动问答等

### 数据来源
- AKShare (主要)
- 掘金量化 GM (备用)
- Tushare Pro (备用)
""",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 尝试包含MCP路由（如果可用）
try:
    from app.mcp.router import mcp_router
    app.include_router(mcp_router)
except ImportError as e:
    print(f"警告: 无法导入 MCP 路由: {e}")


@app.get("/", tags=["root"])
async def root():
    """API 根路径"""
    return {
        "message": "欢迎使用股票分析服务 API",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": f"{settings.API_V1_STR}/openapi.json",
    }


@app.get("/health", tags=["root"])
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": settings.PROJECT_NAME}