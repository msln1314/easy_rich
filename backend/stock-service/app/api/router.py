from fastapi import APIRouter

try:
    from app.api.endpoints import stock_routes
except ImportError:
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

try:
    from app.api.endpoints import hot_news_routes
except ImportError:
    print("警告: 无法导入 hot_news_routes 模块")
    hot_news_routes = None

try:
    from app.api.endpoints import fund_flow_routes
except ImportError:
    print("警告: 无法导入 fund_flow_routes 模块")
    fund_flow_routes = None

try:
    from app.api.endpoints import market_routes
except ImportError:
    print("警告: 无法导入 market_routes 模块")
    market_routes = None

try:
    from app.api.endpoints import stock_extended_routes
except ImportError:
    print("警告: 无法导入 stock_extended_routes 模块")
    stock_extended_routes = None

try:
    from app.api.endpoints import market_extended_routes
except ImportError:
    print("警告: 无法导入 market_extended_routes 模块")
    market_extended_routes = None

try:
    from app.api.endpoints import margin_routes
except ImportError:
    print("警告: 无法导入 margin_routes 模块")
    margin_routes = None

try:
    from app.api.endpoints import institution_routes
except ImportError:
    print("警告: 无法导入 institution_routes 模块")
    institution_routes = None

try:
    from app.api.endpoints import macro_routes
except ImportError:
    print("警告: 无法导入 macro_routes 模块")
    macro_routes = None

try:
    from app.api.endpoints import screener_routes
except ImportError:
    print("警告: 无法导入 screener_routes 模块")
    screener_routes = None

try:
    from app.api.endpoints import export_routes
except ImportError:
    print("警告: 无法导入 export_routes 模块")
    export_routes = None

try:
    from app.api.endpoints import watchlist_routes
except ImportError:
    print("警告: 无法导入 watchlist_routes 模块")
    watchlist_routes = None

try:
    from app.api.endpoints import pattern_routes
except ImportError:
    print("警告: 无法导入 pattern_routes 模块")
    pattern_routes = None

try:
    from app.api.endpoints import etf_routes
except ImportError:
    print("警告: 无法导入 etf_routes 模块")
    etf_routes = None

try:
    from app.api.endpoints import cloud_map_routes
except ImportError:
    print("警告: 无法导入 cloud_map_routes 模块")
    cloud_map_routes = None

try:
    from app.api.endpoints import stock_aggregate_routes
except ImportError:
    print("警告: 无法导入 stock_aggregate_routes 模块")
    stock_aggregate_routes = None

try:
    from app.api.endpoints import baostock_routes
except ImportError:
    print("警告: 无法导入 baostock_routes 模块")
    baostock_routes = None

api_router = APIRouter()

if stock_routes:
    api_router.include_router(stock_routes.router, prefix="/stock", tags=["stock"])
if index_routes:
    api_router.include_router(index_routes.router, prefix="/index", tags=["index"])
if sector_routes:
    api_router.include_router(sector_routes.router, prefix="/sector", tags=["sector"])
if sentiment_routes:
    api_router.include_router(
        sentiment_routes.router, prefix="/sentiment", tags=["sentiment"]
    )
if technical_routes:
    api_router.include_router(
        technical_routes.router, prefix="/technical", tags=["technical"]
    )
if news_routes:
    api_router.include_router(news_routes.router, prefix="/news", tags=["news"])
if hot_news_routes:
    api_router.include_router(
        hot_news_routes.router, prefix="/hot-news", tags=["hot-news"]
    )
if fund_flow_routes:
    api_router.include_router(
        fund_flow_routes.router, prefix="/fund-flow", tags=["fund-flow"]
    )
if market_routes:
    api_router.include_router(market_routes.router, prefix="/market", tags=["market"])
if stock_extended_routes:
    api_router.include_router(
        stock_extended_routes.router, prefix="/stock-ext", tags=["stock-ext"]
    )
if market_extended_routes:
    api_router.include_router(
        market_extended_routes.router, prefix="/market-ext", tags=["market-ext"]
    )
if margin_routes:
    api_router.include_router(margin_routes.router, prefix="/margin", tags=["margin"])
if institution_routes:
    api_router.include_router(
        institution_routes.router, prefix="/institution", tags=["institution"]
    )
if macro_routes:
    api_router.include_router(macro_routes.router, prefix="/macro", tags=["macro"])
if screener_routes:
    api_router.include_router(
        screener_routes.router, prefix="/screener", tags=["screener"]
    )
if export_routes:
    api_router.include_router(export_routes.router, prefix="/export", tags=["export"])
if watchlist_routes:
    api_router.include_router(
        watchlist_routes.router, prefix="/watchlist", tags=["watchlist"]
    )
if pattern_routes:
    api_router.include_router(
        pattern_routes.router, prefix="/pattern", tags=["pattern"]
    )
if etf_routes:
    api_router.include_router(etf_routes.router, prefix="/etf", tags=["etf"])
if cloud_map_routes:
    api_router.include_router(
        cloud_map_routes.router, prefix="/cloud-map", tags=["cloud-map"]
    )
if stock_aggregate_routes:
    api_router.include_router(
        stock_aggregate_routes.router, prefix="/aggregate", tags=["aggregate"]
    )
if baostock_routes:
    api_router.include_router(
        baostock_routes.router, prefix="/baostock", tags=["baostock"]
    )
