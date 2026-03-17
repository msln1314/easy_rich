import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

# 加载 AKShare 代理补丁
try:
    from app.utils.akshare_proxy_patch import install_patch_default

    auth_token = os.getenv("AKSHARE_AUTH_TOKEN", "")
    version = os.getenv("AKSHARE_VERSION", "0.2.13")

    install_patch_default(auth_token=auth_token, version=version, timeout=60, min_interval=0.5)
    print("[Stock Service] AKShare 代理补丁已加载（云端模式）")
except Exception as e:
    print(f"[Stock Service] AKShare 代理补丁加载失败: {e}")

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
        "description": "技术分析接口，包括筹码分布、MACD、KDJ、RSI、BOLL等技术指标",
    },
    {
        "name": "news",
        "description": "新闻资讯接口，包括互动问答、财经新闻等",
    },
    {
        "name": "stock-ext",
        "description": "股票扩展接口，包括龙虎榜、资金流向、财务数据、大宗交易等",
    },
    {
        "name": "market-ext",
        "description": "市场扩展接口，包括涨停池、跌停池、次新股池、异动数据等",
    },
    {
        "name": "margin",
        "description": "融资融券接口，包括融资融券汇总、明细、排名等",
    },
    {
        "name": "institution",
        "description": "机构数据接口，包括机构调研、基金持股、北向资金等",
    },
    {
        "name": "macro",
        "description": "宏观经济接口，包括GDP、CPI、PPI、PMI、利率、汇率等",
    },
    {
        "name": "screener",
        "description": "股票筛选器接口，包括条件选股、涨停/跌停筛选、高换手率筛选等",
    },
    {
        "name": "export",
        "description": "数据导出接口，支持导出Excel、CSV、JSON格式",
    },
    {
        "name": "watchlist",
        "description": "自选股管理接口，包括添加/删除自选股、分组管理、标签管理",
    },
    {
        "name": "pattern",
        "description": "K线形态识别接口，包括W底、M头、头肩顶、突破形态识别",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
## 股票分析服务 API v2.3

基于 AKShare 数据的股票分析服务，提供以下功能：

### 基础功能模块
- **股票数据**: 获取个股基本信息、实时行情、历史K线数据
- **大盘指数**: 获取上证指数、深证成指、创业板指等主要指数数据
- **板块行情**: 获取行业板块、概念板块的涨跌排行
- **市场情绪**: 市场涨跌统计、热度分析
- **技术分析**: 筹码分布、MACD、KDJ、RSI、BOLL、MA等技术指标
- **新闻资讯**: 财经新闻、互动问答等

### 扩展功能模块
- **股票扩展**: 龙虎榜、资金流向、财务指标、分红历史、大宗交易
- **市场扩展**: 涨停池、跌停池、强势股池、次新股池、实时异动
- **融资融券**: 融资融券汇总、明细、排名
- **机构数据**: 机构调研、基金持股、北向资金
- **宏观经济**: GDP、CPI、PPI、PMI、利率、汇率、外汇储备
- **股票筛选**: 条件选股、涨停/跌停筛选、高换手率、低估值筛选
- **数据导出**: 支持导出Excel、CSV、JSON格式
- **自选股管理**: 添加/删除自选股、分组管理、标签管理
- **形态识别**: W底、M头、头肩顶、突破形态等K线形态识别

### 数据来源（兼容层支持多数据源降级）
- AKShare (主要) → pytdx → 新浪财经 → GM → Tushare Pro
""",
    version="2.3.0",
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
