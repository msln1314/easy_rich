from fastapi import APIRouter

# 修改导入语句，先尝试单独导入每个模块
# 如果某个模块不存在或有错误，可以暂时注释掉
try:
    from app.api.endpoints import stock_routes
except ImportError:
    # 如果导入失败，记录日志或打印警告
    print("警告: 无法导入 stock_routes 模块")
    stock_routes = None

try:
    from app.api.endpoints import index_routes
except ImportError:
    print("警告: 无法导入 index_routes 模块")
    index_routes = None

try:
    from app.api.endpoints import sector_routes
except ImportError:
    print("警告: 无法导入 sector_routes 模块")
    sector_routes = None

try:
    from app.api.endpoints import sentiment_routes
except ImportError:
    print("警告: 无法导入 sentiment_routes 模块")
    sentiment_routes = None

try:
    from app.api.endpoints import technical_routes
except ImportError:
    print("警告: 无法导入 technical_routes 模块")
    technical_routes = None

try:
    from app.api.endpoints import news_routes
except ImportError:
    print("警告: 无法导入 news_routes 模块")
    news_routes = None

api_router = APIRouter()

# 根据模块是否成功导入来添加路由
if stock_routes:
    api_router.include_router(stock_routes.router, prefix="/stock", tags=["stock"])
if index_routes:
    api_router.include_router(index_routes.router, prefix="/index", tags=["index"])
if sector_routes:
    api_router.include_router(sector_routes.router, prefix="/sector", tags=["sector"])
if sentiment_routes:
    api_router.include_router(sentiment_routes.router, prefix="/sentiment", tags=["sentiment"])
if technical_routes:
    api_router.include_router(technical_routes.router, prefix="/technical", tags=["technical"])
if news_routes:
    api_router.include_router(news_routes.router, prefix="/news", tags=["news"])