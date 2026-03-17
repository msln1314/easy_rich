# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : margin_service.py
# @IDE            : PyCharm
# @desc           : 融资融券服务 - 融资融券数据接口

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


# ========== 数据模型 ==========


@dataclass
class MarginSummary:
    """融资融券汇总"""

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
    """融资融券明细"""

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
    """个股融资融券"""

    stock_code: str
    stock_name: str
    financing_balance: Optional[float]
    financing_balance_change: Optional[float]
    securities_balance: Optional[float]
    securities_balance_change: Optional[float]
    trade_date: str
    update_time: datetime = field(default_factory=datetime.now)


# ========== 服务类 ==========


class MarginService:
    """融资融券数据服务"""

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_margin_summary(
        self, exchange: str = "沪深京A股"
    ) -> Optional[MarginSummary]:
        """
        获取融资融券汇总数据

        Args:
            exchange: 交易所类型
        """
        logger.info(f"获取融资融券汇总: {exchange}")

        try:
            df = ak.stock_margin_underlying_info_szse(
                date=datetime.now().strftime("%Y%m%d")
            )

            if df.empty:
                return None

            total_financing = df["融资余额"].sum() if "融资余额" in df.columns else 0
            total_securities = df["融券余额"].sum() if "融券余额" in df.columns else 0

            return MarginSummary(
                trade_date=datetime.now().strftime("%Y-%m-%d"),
                financing_balance=float(total_financing) if total_financing else None,
                financing_buy_amount=None,
                financing_repay_amount=None,
                securities_balance=float(total_securities)
                if total_securities
                else None,
                securities_sell_volume=None,
                securities_repay_volume=None,
                total_balance=float(total_financing + total_securities)
                if (total_financing and total_securities)
                else None,
            )

        except Exception as e:
            logger.warning(f"获取融资融券汇总失败: {e}")
            return None

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_margin_detail(
        self, trade_date: Optional[str] = None
    ) -> List[MarginDetail]:
        """
        获取融资融券明细

        Args:
            trade_date: 交易日期 YYYYMMDD
        """
        if not trade_date:
            trade_date = datetime.now().strftime("%Y%m%d")

        logger.info(f"获取融资融券明细: {trade_date}")

        try:
            df = ak.stock_margin_detail_szse(date=trade_date)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = MarginDetail(
                    stock_code=str(row.get("证券代码", "")),
                    stock_name=str(row.get("证券简称", "")),
                    financing_balance=safe_float(row.get("融资余额")),
                    financing_buy_amount=safe_float(row.get("融资买入额")),
                    financing_repay_amount=safe_float(row.get("融资偿还额")),
                    securities_balance=safe_float(row.get("融券余额")),
                    securities_sell_volume=safe_float(row.get("融券卖出量")),
                    securities_repay_volume=safe_float(row.get("融券偿还量")),
                    trade_date=trade_date,
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取融资融券明细失败: {e}")
            return []

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_stock_margin(self, stock_code: str) -> List[StockMarginInfo]:
        """获取个股融资融券历史"""
        logger.info(f"获取个股融资融券: {stock_code}")

        try:
            df = ak.stock_margin_detail_szsh(symbol=stock_code)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = StockMarginInfo(
                    stock_code=stock_code,
                    stock_name=str(row.get("证券简称", "")),
                    financing_balance=safe_float(row.get("融资余额")),
                    financing_balance_change=safe_float(row.get("融资余额变动")),
                    securities_balance=safe_float(row.get("融券余额")),
                    securities_balance_change=safe_float(row.get("融券余额变动")),
                    trade_date=str(row.get("交易日期", "")),
                )
                result.append(item)

            return result[:30]

        except Exception as e:
            logger.warning(f"获取个股融资融券失败: {e}")
            return []

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_margin_rank(
        self, indicator: str = "融资余额", top: int = 50
    ) -> List[Dict[str, Any]]:
        """
        获取融资融券排名

        Args:
            indicator: 排名指标（融资余额/融券余额等）
            top: 返回数量
        """
        logger.info(f"获取融资融券排名: {indicator}")

        try:
            df = ak.stock_margin_rank(trade_date=datetime.now().strftime("%Y%m%d"))

            if df.empty:
                return []

            if indicator in df.columns:
                df = df.sort_values(by=indicator, ascending=False)

            result = []
            for idx, row in df.head(top).iterrows():
                item = {
                    "rank": idx + 1,
                    "stock_code": str(row.get("证券代码", "")),
                    "stock_name": str(row.get("证券简称", "")),
                    "financing_balance": safe_float(row.get("融资余额")),
                    "financing_buy_amount": safe_float(row.get("融资买入额")),
                    "securities_balance": safe_float(row.get("融券余额")),
                    "securities_sell_volume": safe_float(row.get("融券卖出量")),
                }
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取融资融券排名失败: {e}")
            return []


margin_service = MarginService()
