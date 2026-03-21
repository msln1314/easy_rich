# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/21
# @File           : etf_service.py
# @IDE            : PyCharm
# @desc           : ETF资金流向服务

import akshare as ak
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)


@dataclass
class ETFFundFlow:
    etf_code: str
    etf_name: str
    subscribe_amount: Optional[float]
    redeem_amount: Optional[float]
    net_flow: Optional[float]
    trade_date: str


class ETFService:
    """ETF资金流向服务"""

    @cache_result(expire=300)
    async def get_etf_fund_flow_rank(self, top: int = 20) -> List[Dict[str, Any]]:
        """
        获取ETF资金流向排行

        Args:
            top: 返回数量

        Returns:
            ETF资金流向排行数据
        """
        logger.info(f"获取ETF资金流向排行: top {top}")

        try:
            df = ak.fund_etf_fund_info_em(fund="资金净流入")

            if df is None or df.empty:
                logger.warning("ETF资金流向数据为空")
                return []

            result = []
            for idx, (_, row) in enumerate(df.head(top).iterrows()):
                try:
                    cols = list(df.columns)
                    item = {
                        "rank": idx + 1,
                        "etf_code": str(row.iloc[1]) if len(cols) > 1 else "",
                        "etf_name": str(row.iloc[0]) if len(cols) > 0 else "",
                        "net_flow": self._safe_float(row.iloc[2])
                        if len(cols) > 2
                        else None,
                        "subscribe_amount": self._safe_float(row.iloc[3])
                        if len(cols) > 3
                        else None,
                        "redeem_amount": self._safe_float(row.iloc[4])
                        if len(cols) > 4
                        else None,
                        "trade_date": datetime.now().strftime("%Y-%m-%d"),
                    }
                    result.append(item)
                except Exception as e:
                    logger.warning(f"解析ETF资金流向数据失败: {e}")
                    continue

            logger.info(f"获取到 {len(result)} 条ETF资金流向数据")
            return result

        except Exception as e:
            logger.error(f"获取ETF资金流向失败: {e}")
            return []

    @cache_result(expire=300)
    async def get_etf_subscribe_rank(self, top: int = 10) -> List[Dict[str, Any]]:
        """
        获取ETF申购排行

        Args:
            top: 返回数量

        Returns:
            ETF申购排行数据
        """
        logger.info(f"获取ETF申购排行: top {top}")

        try:
            df = ak.fund_etf_fund_info_em(fund="申购")

            if df is None or df.empty:
                return []

            result = []
            for idx, (_, row) in enumerate(df.head(top).iterrows()):
                try:
                    cols = list(df.columns)
                    item = {
                        "rank": idx + 1,
                        "etf_code": str(row.iloc[1]) if len(cols) > 1 else "",
                        "etf_name": str(row.iloc[0]) if len(cols) > 0 else "",
                        "subscribe_amount": self._safe_float(row.iloc[2])
                        if len(cols) > 2
                        else None,
                        "trade_date": datetime.now().strftime("%Y-%m-%d"),
                    }
                    result.append(item)
                except Exception as e:
                    logger.warning(f"解析ETF申购数据失败: {e}")
                    continue

            return result

        except Exception as e:
            logger.error(f"获取ETF申购排行失败: {e}")
            return []

    @cache_result(expire=300)
    async def get_etf_redeem_rank(self, top: int = 10) -> List[Dict[str, Any]]:
        """
        获取ETF赎回排行

        Args:
            top: 返回数量

        Returns:
            ETF赎回排行数据
        """
        logger.info(f"获取ETF赎回排行: top {top}")

        try:
            df = ak.fund_etf_fund_info_em(fund="赎回")

            if df is None or df.empty:
                return []

            result = []
            for idx, (_, row) in enumerate(df.head(top).iterrows()):
                try:
                    cols = list(df.columns)
                    item = {
                        "rank": idx + 1,
                        "etf_code": str(row.iloc[1]) if len(cols) > 1 else "",
                        "etf_name": str(row.iloc[0]) if len(cols) > 0 else "",
                        "redeem_amount": self._safe_float(row.iloc[2])
                        if len(cols) > 2
                        else None,
                        "trade_date": datetime.now().strftime("%Y-%m-%d"),
                    }
                    result.append(item)
                except Exception as e:
                    logger.warning(f"解析ETF赎回数据失败: {e}")
                    continue

            return result

        except Exception as e:
            logger.error(f"获取ETF赎回排行失败: {e}")
            return []

    async def get_etf_overview(self, top: int = 10) -> Dict[str, Any]:
        """
        获取ETF资金流向概览（包含申购和赎回两个维度）

        Args:
            top: 返回数量

        Returns:
            ETF资金流向概览数据
        """
        logger.info("获取ETF资金流向概览")

        net_flow_rank = await self.get_etf_fund_flow_rank(top)
        subscribe_rank = await self.get_etf_subscribe_rank(top)
        redeem_rank = await self.get_etf_redeem_rank(top)

        return {
            "net_flow_rank": net_flow_rank,
            "subscribe_rank": subscribe_rank,
            "redeem_rank": redeem_rank,
            "update_time": datetime.now().isoformat(),
        }

    def _safe_float(self, value) -> Optional[float]:
        if value is None or pd.isna(value):
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None


etf_service = ETFService()
