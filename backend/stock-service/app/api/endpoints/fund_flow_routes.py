from fastapi import APIRouter, Query
from app.services.fund_flow_service import fund_flow_service
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/north-money/flow")
async def get_north_money_flow(
    days: int = Query(30, ge=1, le=365, description="获取最近N天的数据"),
):
    """
    获取北向资金历史流向数据

    返回:
    - date: 日期
    - time: 时间
    - sh_hk_flow: 沪港通资金流向
    - sz_hk_flow: 深港通资金流向
    - total_flow: 北向资金合计
    """
    try:
        data = await fund_flow_service.get_north_money_flow(days)
        return {"data": data, "total": len(data)}
    except Exception as e:
        logger.error(f"获取北向资金流向失败: {e}")
        return {"data": [], "total": 0, "error": str(e)}


@router.get("/north-money/realtime")
async def get_realtime_north_money():
    """
    获取实时北向资金

    返回:
    - sh_hk_flow: 沪港通资金流向
    - sz_hk_flow: 深港通资金流向
    - total_flow: 北向资金合计
    - update_time: 更新时间
    """
    try:
        data = await fund_flow_service.get_realtime_north_money()
        return {"data": data}
    except Exception as e:
        logger.error(f"获取实时北向资金失败: {e}")
        return {"data": None, "error": str(e)}


@router.get("/north-money/summary")
async def get_north_money_summary():
    """
    获取北向资金汇总

    返回各渠道的北向资金买卖汇总数据
    """
    try:
        data = await fund_flow_service.get_north_money_summary()
        return {"data": data}
    except Exception as e:
        logger.error(f"获取北向资金汇总失败: {e}")
        return {"data": {}, "error": str(e)}


@router.get("/market/flow")
async def get_market_fund_flow(
    days: int = Query(30, ge=1, le=365, description="获取最近N天的数据"),
):
    """
    获取市场资金流向数据

    返回:
    - date: 日期
    - sh_close: 上证收盘
    - sh_change: 上证涨跌幅
    - sz_close: 深证收盘
    - sz_change: 深证涨跌幅
    - main_net_inflow: 主力净流入
    - main_net_inflow_pct: 主力净流入占比
    - super_large_net_inflow: 超大单净流入
    - large_net_inflow: 大单净流入
    - medium_net_inflow: 中单净流入
    - small_net_inflow: 小单净流入
    """
    try:
        data = await fund_flow_service.get_market_fund_flow(days)
        return {"data": data, "total": len(data)}
    except Exception as e:
        logger.error(f"获取市场资金流向失败: {e}")
        return {"data": [], "total": 0, "error": str(e)}


@router.get("/market/flow/today")
async def get_today_market_fund_flow():
    """获取今日市场资金流向"""
    try:
        data = await fund_flow_service.get_today_market_fund_flow()
        return {"data": data}
    except Exception as e:
        logger.error(f"获取今日市场资金流向失败: {e}")
        return {"data": None, "error": str(e)}


@router.get("/south-money/realtime")
async def get_realtime_south_money():
    """获取实时南向资金（港股通）"""
    try:
        data = await fund_flow_service.get_south_money_realtime()
        return {"data": data}
    except Exception as e:
        logger.error(f"获取南向资金失败: {e}")
        return {"data": None, "error": str(e)}
