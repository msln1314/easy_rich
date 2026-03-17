# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : market_extended_service.py
# @IDE            : PyCharm
# @desc           : 市场扩展服务 - 涨停池、跌停池、异动数据等

import akshare as ak
import pandas as pd
import math
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from app.core.logging import get_logger
from app.utils.cache import cache_result
from app.utils.akshare_wrapper import handle_akshare_exception
from app.services.pytdx_source import pytdx_source

logger = get_logger(__name__)


def safe_float(value, default=None):
    if value is None or pd.isna(value):
        return default
    try:
        float_value = float(value)
        if math.isnan(float_value) or math.isinf(float_value):
            return default
        return float_value
    except (ValueError, TypeError):
        return default


# ========== 数据模型 ==========


@dataclass
class ZTPoolItem:
    """涨停池数据"""

    rank: int
    stock_code: str
    stock_name: str
    close_price: Optional[float]
    change_percent: Optional[float]
    turnover_rate: Optional[float]
    final_time: Optional[str]
    first_time: Optional[str]
    open_count: Optional[int]
    continuous_days: Optional[int]
    reason: Optional[str]
    amount: Optional[float]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class DTPoolItem:
    """跌停池数据"""

    rank: int
    stock_code: str
    stock_name: str
    close_price: Optional[float]
    change_percent: Optional[float]
    turnover_rate: Optional[float]
    final_time: Optional[str]
    first_time: Optional[str]
    open_count: Optional[int]
    continuous_days: Optional[int]
    amount: Optional[float]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class StrongPoolItem:
    """强势股池"""

    rank: int
    stock_code: str
    stock_name: str
    close_price: Optional[float]
    change_percent: Optional[float]
    turnover_rate: Optional[float]
    reason: Optional[str]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class SubNewPoolItem:
    """次新股池"""

    rank: int
    stock_code: str
    stock_name: str
    close_price: Optional[float]
    change_percent: Optional[float]
    turnover_rate: Optional[float]
    listing_days: Optional[int]
    continuous_days: Optional[int]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class LimitUpStatistic:
    """涨停统计"""

    trade_date: str
    total_count: int
    new_count: int
    continuous_2_count: int
    continuous_3_count: int
    continuous_4_count: int
    continuous_5_plus_count: int
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class MarketActivity:
    """市场活跃度"""

    trade_date: str
    total_stocks: int
    up_count: int
    down_count: int
    flat_count: int
    limit_up_count: int
    limit_down_count: int
    total_amount: float
    avg_turnover: Optional[float]
    update_time: datetime = field(default_factory=datetime.now)


# ========== 服务类 ==========


class MarketExtendedService:
    """市场扩展数据服务"""

    # ========== 涨停池 ==========

    @cache_result(expire=60)
    @handle_akshare_exception
    async def get_zt_pool(self, trade_date: Optional[str] = None) -> List[ZTPoolItem]:
        """获取涨停池数据"""
        if not trade_date:
            trade_date = datetime.now().strftime("%Y%m%d")

        logger.info(f"获取涨停池: {trade_date}")

        try:
            df = ak.stock_zt_pool_em(date=trade_date)

            if df.empty:
                logger.warning(f"涨停池数据为空: {trade_date}")
                return []

            result = []
            for idx, row in df.iterrows():
                item = ZTPoolItem(
                    rank=idx + 1,
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    close_price=safe_float(row.get("最新价")),
                    change_percent=safe_float(row.get("涨跌幅")),
                    turnover_rate=safe_float(row.get("换手率")),
                    final_time=str(row.get("涨停统计", {}).get("最后涨停时间", ""))
                    if isinstance(row.get("涨停统计"), dict)
                    else str(row.get("最后涨停时间", "")),
                    first_time=str(row.get("首次涨停时间", ""))
                    if pd.notna(row.get("首次涨停时间"))
                    else None,
                    open_count=int(row.get("涨停统计", {}).get("开板次数", 0))
                    if isinstance(row.get("涨停统计"), dict)
                    else safe_float(row.get("开板次数")),
                    continuous_days=int(row.get("涨停统计", {}).get("连板数", 1))
                    if isinstance(row.get("涨停统计"), dict)
                    else safe_float(row.get("连板数")),
                    reason=str(row.get("涨停原因类别", ""))
                    if pd.notna(row.get("涨停原因类别"))
                    else None,
                    amount=safe_float(row.get("成交额")),
                )
                result.append(item)

            logger.info(f"获取涨停池成功: {len(result)}只股票")
            return result

        except Exception as e:
            logger.error(f"获取涨停池失败: {e}")
            raise

    @cache_result(expire=60)
    @handle_akshare_exception
    async def get_zt_pool_strong(
        self, trade_date: Optional[str] = None
    ) -> List[StrongPoolItem]:
        """获取强势股池"""
        if not trade_date:
            trade_date = datetime.now().strftime("%Y%m%d")

        logger.info(f"获取强势股池: {trade_date}")

        try:
            df = ak.stock_zt_pool_strong_em(date=trade_date)

            if df.empty:
                return []

            result = []
            for idx, row in df.iterrows():
                item = StrongPoolItem(
                    rank=idx + 1,
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    close_price=safe_float(row.get("最新价")),
                    change_percent=safe_float(row.get("涨跌幅")),
                    turnover_rate=safe_float(row.get("换手率")),
                    reason=str(row.get("涨停原因类别", ""))
                    if pd.notna(row.get("涨停原因类别"))
                    else None,
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取强势股池失败: {e}")
            return []

    @cache_result(expire=60)
    @handle_akshare_exception
    async def get_zt_pool_zb(
        self, trade_date: Optional[str] = None
    ) -> List[ZTPoolItem]:
        """获取涨停炸板池"""
        if not trade_date:
            trade_date = datetime.now().strftime("%Y%m%d")

        logger.info(f"获取涨停炸板池: {trade_date}")

        try:
            df = ak.stock_zt_pool_zbgc_em(date=trade_date)

            if df.empty:
                return []

            result = []
            for idx, row in df.iterrows():
                item = ZTPoolItem(
                    rank=idx + 1,
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    close_price=safe_float(row.get("最新价")),
                    change_percent=safe_float(row.get("涨跌幅")),
                    turnover_rate=safe_float(row.get("换手率")),
                    final_time=None,
                    first_time=None,
                    open_count=None,
                    continuous_days=None,
                    reason=str(row.get("涨停原因类别", ""))
                    if pd.notna(row.get("涨停原因类别"))
                    else None,
                    amount=safe_float(row.get("成交额")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取涨停炸板池失败: {e}")
            return []

    # ========== 跌停池 ==========

    @cache_result(expire=60)
    @handle_akshare_exception
    async def get_dt_pool(self, trade_date: Optional[str] = None) -> List[DTPoolItem]:
        """获取跌停池数据"""
        if not trade_date:
            trade_date = datetime.now().strftime("%Y%m%d")

        logger.info(f"获取跌停池: {trade_date}")

        try:
            df = ak.stock_zt_pool_dtgc_em(date=trade_date)

            if df.empty:
                return []

            result = []
            for idx, row in df.iterrows():
                item = DTPoolItem(
                    rank=idx + 1,
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    close_price=safe_float(row.get("最新价")),
                    change_percent=safe_float(row.get("涨跌幅")),
                    turnover_rate=safe_float(row.get("换手率")),
                    final_time=str(row.get("最后跌停时间", ""))
                    if pd.notna(row.get("最后跌停时间"))
                    else None,
                    first_time=str(row.get("首次跌停时间", ""))
                    if pd.notna(row.get("首次跌停时间"))
                    else None,
                    open_count=safe_float(row.get("开板次数")),
                    continuous_days=safe_float(row.get("连跌天数")),
                    amount=safe_float(row.get("成交额")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取跌停池失败: {e}")
            return []

    # ========== 次新股池 ==========

    @cache_result(expire=60)
    @handle_akshare_exception
    async def get_sub_new_pool(
        self, trade_date: Optional[str] = None
    ) -> List[SubNewPoolItem]:
        """获取次新股池"""
        if not trade_date:
            trade_date = datetime.now().strftime("%Y%m%d")

        logger.info(f"获取次新股池: {trade_date}")

        try:
            df = ak.stock_zt_pool_sub_new_em(date=trade_date)

            if df.empty:
                return []

            result = []
            for idx, row in df.iterrows():
                item = SubNewPoolItem(
                    rank=idx + 1,
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    close_price=safe_float(row.get("最新价")),
                    change_percent=safe_float(row.get("涨跌幅")),
                    turnover_rate=safe_float(row.get("换手率")),
                    listing_days=safe_float(row.get("上市天数")),
                    continuous_days=safe_float(row.get("连板数")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取次新股池失败: {e}")
            return []

    # ========== 市场统计 ==========

    @cache_result(expire=30)
    @handle_akshare_exception
    async def get_limit_up_statistics(self, days: int = 30) -> List[LimitUpStatistic]:
        """获取涨停统计数据"""
        logger.info(f"获取涨停统计: 近{days}天")

        try:
            df = ak.stock_zt_pool_previous_em(date=datetime.now().strftime("%Y%m%d"))

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = LimitUpStatistic(
                    trade_date=str(row.get("日期", "")),
                    total_count=int(row.get("涨停家数", 0))
                    if pd.notna(row.get("涨停家数"))
                    else 0,
                    new_count=int(row.get("涨停家数", 0))
                    if pd.notna(row.get("涨停家数"))
                    else 0,
                    continuous_2_count=0,
                    continuous_3_count=0,
                    continuous_4_count=0,
                    continuous_5_plus_count=0,
                )
                result.append(item)

            return result[:days]

        except Exception as e:
            logger.warning(f"获取涨停统计失败: {e}")
            return []

    @cache_result(expire=30)
    @handle_akshare_exception
    async def get_market_activity_legu(self) -> Optional[MarketActivity]:
        """获取市场活跃度（乐股网）"""
        logger.info("获取市场活跃度")

        try:
            df = ak.stock_market_activity_legu()

            if df.empty:
                return None

            data = dict(zip(df["item"], df["value"]))

            up_count = int(float(data.get("上涨", 0)))
            down_count = int(float(data.get("下跌", 0)))
            flat_count = int(float(data.get("平盘", 0)))
            limit_up = int(float(data.get("涨停", 0)))
            limit_down = int(float(data.get("跌停", 0)))

            return MarketActivity(
                trade_date=str(date.today()),
                total_stocks=up_count + down_count + flat_count,
                up_count=up_count,
                down_count=down_count,
                flat_count=flat_count,
                limit_up_count=limit_up,
                limit_down_count=limit_down,
                total_amount=0,
                avg_turnover=None,
            )

        except Exception as e:
            logger.warning(f"获取市场活跃度失败: {e}")
            return None

    # ========== 实时异动 ==========

    @cache_result(expire=30)
    @handle_akshare_exception
    async def get_realtime_alert(self) -> List[Dict[str, Any]]:
        """获取实时异动数据"""
        logger.info("获取实时异动")

        try:
            df = ak.stock_change_em()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = {
                    "stock_code": str(row.get("代码", "")),
                    "stock_name": str(row.get("名称", "")),
                    "price": safe_float(row.get("最新价")),
                    "change_percent": safe_float(row.get("涨跌幅")),
                    "volume": safe_float(row.get("成交量")),
                    "amount": safe_float(row.get("成交额")),
                    "turnover_rate": safe_float(row.get("换手率")),
                    "alert_type": str(row.get("异动类型", ""))
                    if pd.notna(row.get("异动类型"))
                    else None,
                    "alert_time": str(row.get("异动时间", ""))
                    if pd.notna(row.get("异动时间"))
                    else None,
                }
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取实时异动失败: {e}")
            return []

    @cache_result(expire=60)
    @handle_akshare_exception
    async def get_fast_up(self) -> List[Dict[str, Any]]:
        """获取快速上涨股票"""
        logger.info("获取快速上涨股票")

        try:
            df = ak.stock_change_em()

            if df.empty:
                return []

            df = df[df["涨跌幅"] > 3]

            result = []
            for _, row in df.iterrows():
                item = {
                    "stock_code": str(row.get("代码", "")),
                    "stock_name": str(row.get("名称", "")),
                    "price": safe_float(row.get("最新价")),
                    "change_percent": safe_float(row.get("涨跌幅")),
                    "volume": safe_float(row.get("成交量")),
                    "amount": safe_float(row.get("成交额")),
                }
                result.append(item)

            return result[:50]

        except Exception as e:
            logger.warning(f"获取快速上涨股票失败: {e}")
            return []

    # ========== 综合排行 ==========

    async def get_all_pools(self, trade_date: Optional[str] = None) -> Dict[str, Any]:
        """获取所有池数据"""
        logger.info("获取所有池数据")

        zt_pool = await self.get_zt_pool(trade_date)
        dt_pool = await self.get_dt_pool(trade_date)
        strong_pool = await self.get_zt_pool_strong(trade_date)
        sub_new_pool = await self.get_sub_new_pool(trade_date)

        return {
            "zt_pool": [asdict(item) for item in zt_pool],
            "dt_pool": [asdict(item) for item in dt_pool],
            "strong_pool": [asdict(item) for item in strong_pool],
            "sub_new_pool": [asdict(item) for item in sub_new_pool],
            "trade_date": trade_date or datetime.now().strftime("%Y%m%d"),
            "update_time": datetime.now().isoformat(),
        }


# 兼容asdict导入
from dataclasses import asdict

market_extended_service = MarketExtendedService()
