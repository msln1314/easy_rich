from fastapi import APIRouter

from apps.admin.stock import (
    stock_base,
    news,
    stock_watchlist,
    stock_monitor_condition,
    stock_monitor_strategy,
    stock_analysis,
    stock_prediction,
    stock_group_api,
    my_stock,
    stock_board_industry,
    stock_board_concept,
    stock_ranking,
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

# router.include_router(notice.router, prefix="/system/notice", tags=["system"])
# router.include_router(alarm.router, prefix="/system/alarm", tags=["system"])
