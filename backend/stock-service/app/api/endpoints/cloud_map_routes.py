from fastapi import APIRouter, Query
from app.services.cloud_map_service import cloud_map_service
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/data")
async def get_cloud_map_data(
    market: str = Query("all", description="市场: all/sh/sz/bj/kc/cy"),
    metric: str = Query("change", description="维度: change/pe/pb/amount"),
    period: str = Query("today", description="周期: today/week/month/ytd"),
):
    """
    获取大盘云图数据

    返回:
    - industries: 按行业分组的股票数据
    - summary: 市场概览 (涨跌数量等)
    - snapshots: 分时快照时间点
    - update_time: 更新时间
    """
    try:
        data = await cloud_map_service.get_cloud_map_data(market, metric, period)
        return {"data": data}
    except Exception as e:
        logger.error(f"获取云图数据失败: {e}")
        return {"data": None, "error": str(e)}
