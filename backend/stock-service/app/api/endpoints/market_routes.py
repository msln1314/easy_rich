from fastapi import APIRouter, Query
from app.services.market_service import market_service
from app.services.index_service import index_service
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/summary")
async def get_market_summary():
    """
    获取市场汇总数据

    返回:
    - total_stocks: 总股票数
    - up_stocks: 上涨家数
    - down_stocks: 下跌家数
    - flat_stocks: 平盘家数
    - total_amount: 总成交额
    - total_volume: 总成交量
    - limit_up_count: 涨停数
    - limit_down_count: 跌停数
    """
    try:
        data = await market_service.get_market_summary()
        return {"data": data}
    except Exception as e:
        logger.error(f"获取市场汇总失败: {e}")
        return {"data": None, "error": str(e)}


@router.get("/indices")
async def get_main_indices():
    """
    获取主要指数行情

    返回上证指数、深证成指、创业板指、科创50的实时行情
    """
    try:
        quotes, source = await index_service.get_index_quotes()
        items = []
        for q in quotes:
            if isinstance(q, dict):
                items.append(
                    {
                        "index_code": q.get("code"),
                        "index_name": q.get("name"),
                        "close_price": q.get("price"),
                        "change_percent": q.get("change_percent"),
                        "change_amount": q.get("change"),
                        "volume": q.get("volume"),
                        "amount": q.get("amount"),
                    }
                )
            else:
                items.append(
                    {
                        "index_code": q.code,
                        "index_name": q.name,
                        "close_price": q.price,
                        "change_percent": q.change_percent,
                        "change_amount": q.change,
                        "volume": q.volume,
                        "amount": q.amount,
                    }
                )
        return {
            "data": {
                "items": items,
                "source": source,
                "update_time": quotes[0].update_time.isoformat()
                if quotes and hasattr(quotes[0], "update_time")
                else None,
            }
        }
    except Exception as e:
        logger.error(f"获取主要指数失败: {e}")
        return {"data": None, "error": str(e)}


@router.get("/rankings")
async def get_realtime_rankings(
    limit: int = Query(20, ge=1, le=100, description="每类排行数量"),
):
    """
    获取实时排行数据

    返回:
    - change_percent_ranking: 涨幅榜
    - down_ranking: 跌幅榜
    - turnover_ranking: 换手率榜
    - amount_ranking: 成交额榜
    """
    try:
        data = await market_service.get_realtime_rankings(limit)
        return {"data": data}
    except Exception as e:
        logger.error(f"获取实时排行失败: {e}")
        return {"data": None, "error": str(e)}


@router.get("/rankings/change")
async def get_change_ranking(limit: int = Query(20, ge=1, le=100)):
    """获取涨幅排行"""
    try:
        data = await market_service.get_change_percent_ranking(limit)
        return {"data": data, "total": len(data)}
    except Exception as e:
        logger.error(f"获取涨幅排行失败: {e}")
        return {"data": [], "error": str(e)}


@router.get("/rankings/down")
async def get_down_ranking(limit: int = Query(20, ge=1, le=100)):
    """获取跌幅排行"""
    try:
        data = await market_service.get_down_ranking(limit)
        return {"data": data, "total": len(data)}
    except Exception as e:
        logger.error(f"获取跌幅排行失败: {e}")
        return {"data": [], "error": str(e)}


@router.get("/rankings/turnover")
async def get_turnover_ranking(limit: int = Query(20, ge=1, le=100)):
    """获取换手率排行"""
    try:
        data = await market_service.get_turnover_ranking(limit)
        return {"data": data, "total": len(data)}
    except Exception as e:
        logger.error(f"获取换手率排行失败: {e}")
        return {"data": [], "error": str(e)}


@router.get("/rankings/amount")
async def get_amount_ranking(limit: int = Query(20, ge=1, le=100)):
    """获取成交额排行"""
    try:
        data = await market_service.get_amount_ranking(limit)
        return {"data": data, "total": len(data)}
    except Exception as e:
        logger.error(f"获取成交额排行失败: {e}")
        return {"data": [], "error": str(e)}


@router.get("/limit-up-pool")
async def get_limit_up_pool():
    """获取涨停池数据，用于涨停热力图"""
    try:
        data = await market_service.get_limit_up_pool()
        return {"data": data}
    except Exception as e:
        logger.error(f"获取涨停池数据失败: {e}")
        return {"data": None, "error": str(e)}


@router.get("/up-down-distribution")
async def get_up_down_distribution():
    """获取涨跌分布数据"""
    try:
        data = await market_service.get_up_down_distribution()
        return {"data": data}
    except Exception as e:
        logger.error(f"获取涨跌分布数据失败: {e}")
        return {"data": None, "error": str(e)}
