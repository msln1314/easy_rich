from fastapi import APIRouter

from apps.admin.stock import (
    stock_base,
    news,
    stock_watchlist,
    stock_monitor_condition,
    stock_monitor_strategy,
    stock_monitor_log,
    stock_analysis,
    stock_prediction,
    stock_group_api,
    my_stock,
    stock_board_industry,
    stock_board_concept,
    stock_ranking,
    stock_index,
    stock_daily_ranking,
    stock_quote,
    hot_news,
    fund_flow,
    stock_selection,
    stock_longhubang,
    stock_market_dashboard,
)


# #
#
router = APIRouter()
router.include_router(stock_base.router, prefix="/stock_base", tags=["stock"])
router.include_router(news.router, prefix="/news", tags=["stock"])
router.include_router(stock_watchlist.router, prefix="/stock_watchlist", tags=["stock"])
router.include_router(
    stock_monitor_condition.router, prefix="/stock_monitor_condition", tags=["stock"]
)
router.include_router(
    stock_monitor_strategy.router, prefix="/stock_monitor_strategy", tags=["stock"]
)
router.include_router(
    stock_monitor_log.router, prefix="/stock_monitor_log", tags=["stock"]
)
router.include_router(stock_analysis.router, prefix="/stock_analysis", tags=["stock"])
router.include_router(
    stock_prediction.router, prefix="/stock_prediction", tags=["stock"]
)
router.include_router(stock_group_api.router, prefix="/stock_group", tags=["stock"])
router.include_router(my_stock.router, prefix="/my_stock", tags=["stock"])
router.include_router(
    stock_board_industry.router, prefix="/board_industry", tags=["industry"]
)
router.include_router(
    stock_board_concept.router, prefix="/board_concept", tags=["concept"]
)
router.include_router(stock_ranking.router, tags=["ranking"])
router.include_router(stock_index.router, tags=["大盘指数"])
router.include_router(stock_daily_ranking.router, tags=["每日排行"])
router.include_router(stock_quote.router, tags=["股票行情"])
router.include_router(hot_news.router, tags=["热门头条"])
router.include_router(fund_flow.router, tags=["资金流向"])
router.include_router(stock_selection.router, tags=["选股信号"])
router.include_router(stock_longhubang.router, tags=["龙虎榜"])
router.include_router(stock_market_dashboard.router, tags=["大盘座舱"])

# router.include_router(notice.router, prefix="/system/notice", tags=["system"])
# router.include_router(alarm.router, prefix="/system/alarm", tags=["system"])
