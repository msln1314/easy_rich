# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : margin_service.py
# @IDE            : PyCharm
# @desc           : 融资融券服务

import akshare as ak
import pandas as pd
import math
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from app.core.logging import get_logger
from app.utils.cache import cache_result
from app.utils.akshare_wrapper import handle_akshare_exception

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


@dataclass
class MarginSummary:
    trade_date: str
    financing_balance: Optional[float]
    financing_buy_amount: Optional[float]
    financing_repay_amount: Optional[float]
    securities_balance: Optional[float]
    securities_sell_volume: Optional[float]
    securities_repay_volume: Optional[float]
    total_balance: Optional[float]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class MarginDetail:
    stock_code: str
    stock_name: str
    financing_balance: Optional[float]
    financing_buy_amount: Optional[float]
    financing_repay_amount: Optional[float]
    securities_balance: Optional[float]
    securities_sell_volume: Optional[float]
    securities_repay_volume: Optional[float]
    trade_date: str
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class StockMarginInfo:
    stock_code: str
    stock_name: str
    financing_balance: Optional[float]
    financing_balance_change: Optional[float]
    securities_balance: Optional[float]
    securities_balance_change: Optional[float]
    trade_date: str
    update_time: datetime = field(default_factory=datetime.now)


class MarginService:
    """融资融券数据服务"""

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_margin_summary(
        self, exchange: str = "沪深京A股"
    ) -> Optional[Dict[str, Any]]:
        logger.info(f"获取融资融券汇总: {exchange}")

        try:
            sh_df = ak.stock_margin_sse()

            if sh_df is None or sh_df.empty:
                logger.warning("沪市融资融券数据为空")
                return None

            latest = sh_df.iloc[0]
            cols = list(sh_df.columns)

            trade_date = str(latest[cols[0]]) if len(cols) > 0 else None
            rzye = safe_float(latest[cols[1]]) if len(cols) > 1 else None
            rzmre = safe_float(latest[cols[2]]) if len(cols) > 2 else None
            rqye = safe_float(latest[cols[3]]) if len(cols) > 3 else None
            rqmcl = safe_float(latest[cols[4]]) if len(cols) > 4 else None
            rzche = safe_float(latest[cols[5]]) if len(cols) > 5 else None
            total = safe_float(latest[cols[6]]) if len(cols) > 6 else None

            return {
                "trade_date": trade_date,
                "rzye": rzye,
                "rzmre": rzmre,
                "rqye": rqye,
                "rqmcl": rqmcl,
                "rzche": rzche,
                "total": total,
                "update_time": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.warning(f"获取融资融券汇总失败: {e}")
            return None

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_margin_detail(
        self, trade_date: Optional[str] = None
    ) -> List[MarginDetail]:
        if not trade_date:
            trade_date = datetime.now().strftime("%Y%m%d")

        logger.info(f"获取融资融券明细: {trade_date}")

        try:
            df = ak.stock_margin_detail_sse()

            if df is None or df.empty:
                return []

            cols = list(df.columns)
            result = []
            for _, row in df.head(50).iterrows():
                item = MarginDetail(
                    stock_code=str(row[cols[1]]) if len(cols) > 1 else "",
                    stock_name=str(row[cols[2]]) if len(cols) > 2 else "",
                    financing_balance=safe_float(row[cols[3]])
                    if len(cols) > 3
                    else None,
                    financing_buy_amount=safe_float(row[cols[4]])
                    if len(cols) > 4
                    else None,
                    financing_repay_amount=safe_float(row[cols[5]])
                    if len(cols) > 5
                    else None,
                    securities_balance=safe_float(row[cols[6]])
                    if len(cols) > 6
                    else None,
                    securities_sell_volume=safe_float(row[cols[7]])
                    if len(cols) > 7
                    else None,
                    securities_repay_volume=safe_float(row[cols[8]])
                    if len(cols) > 8
                    else None,
                    trade_date=str(row[cols[0]]) if len(cols) > 0 else trade_date,
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取融资融券明细失败: {e}")
            return []

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_margin_rank(
        self, indicator: str = "融资余额", top: int = 50
    ) -> List[Dict[str, Any]]:
        """
        获取融资融券排名，按融资余额或融券余额排序

        使用 stock_margin_detail_sse 接口获取个股融资融券明细数据，
        然后按融资余额排序返回排名
        """
        logger.info(f"获取融资融券排名: {indicator}")

        try:
            df = ak.stock_margin_detail_sse()

            if df is None or df.empty:
                return []

            cols = list(df.columns)

            # 按融资余额排序 (cols[3] 是融资余额)
            if len(cols) > 3:
                df = df.sort_values(by=cols[3], ascending=False)

            result = []
            for idx, (_, row) in enumerate(df.head(top).iterrows()):
                item = {
                    "rank": idx + 1,
                    "stock_code": str(row[cols[1]]) if len(cols) > 1 else "",
                    "stock_name": str(row[cols[2]]) if len(cols) > 2 else "",
                    "rzye": safe_float(row[cols[3]])
                    if len(cols) > 3
                    else None,  # 融资余额
                    "rzmre": safe_float(row[cols[4]])
                    if len(cols) > 4
                    else None,  # 融资买入额
                    "rqye": safe_float(row[cols[6]])
                    if len(cols) > 6
                    else None,  # 融券余额
                    "data_from": "akshare",
                }
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取融资融券排名失败: {e}")
            return []

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_stock_margin(self, stock_code: str) -> List[StockMarginInfo]:
        """
        获取个股融资融券历史数据

        注意：stock_margin_account_info 返回的是账户历史数据，不是个股数据
        如需获取个股历史融资融券数据，可能需要其他数据源
        """
        logger.info(f"获取个股融资融券: {stock_code}")

        try:
            # stock_margin_account_info 返回的是融资融券账户统计，不是个股数据
            # 暂时返回空列表，后续可以考虑使用其他数据源
            df = ak.stock_margin_account_info()

            if df is None or df.empty:
                return []

            result = []
            for _, row in df.head(30).iterrows():
                item = StockMarginInfo(
                    stock_code=stock_code,
                    stock_name="",
                    financing_balance=safe_float(row.get("融资余额")),
                    financing_balance_change=None,
                    securities_balance=safe_float(row.get("融券余额")),
                    securities_balance_change=None,
                    trade_date=str(row.get("日期", "")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取个股融资融券失败: {e}")
            return []


margin_service = MarginService()
