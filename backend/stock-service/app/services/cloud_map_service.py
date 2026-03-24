# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/22
# @File           : cloud_map_service.py
# @desc           : 大盘云图服务 - 全市场股票 Treemap 数据

import akshare as ak
import pandas as pd
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)

MARKET_FILTERS = {
    "all": None,
    "sh": lambda x: x.startswith("6") or x.startswith("5"),
    "sz": lambda x: x.startswith("0") or x.startswith("3"),
    "bj": lambda x: x.startswith("4") or x.startswith("8"),
    "kc": lambda x: x.startswith("688"),
    "cy": lambda x: x.startswith("300"),
}


class CloudMapService:
    """大盘云图服务"""

    @cache_result(expire=60)
    async def get_cloud_map_data(
        self, market: str = "all", metric: str = "change", period: str = "today"
    ) -> Dict[str, Any]:
        """
        获取云图数据

        Args:
            market: 市场 (all/sh/sz/bj/kc/cy)
            metric: 维度 (change/pe/pb/amount)
            period: 周期 (today/week/month/ytd)

        Returns:
            云图数据，包含行业分组、市场概览、分时快照
        """
        logger.info(f"获取云图数据: market={market}, metric={metric}, period={period}")

        try:
            df = ak.stock_zh_a_spot_em()

            if df is None or df.empty:
                logger.error("获取股票数据为空")
                return self._empty_result()

            # 按市场过滤
            filter_fn = MARKET_FILTERS.get(market)
            if filter_fn:
                df = df[df["代码"].apply(filter_fn)]

            # 解析数据
            stocks = self._parse_stocks(df, metric)

            # 按行业分组
            industries = self._group_by_industry(stocks, metric)

            # 市场概览
            summary = self._calc_summary(df)

            # 分时快照 (简化版，实际需要定时任务存储)
            snapshots = await self._get_snapshots(market, metric)

            return {
                "industries": industries,
                "summary": summary,
                "snapshots": snapshots,
                "update_time": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"获取云图数据失败: {e}")
            return self._empty_result()

    def _parse_stocks(self, df: pd.DataFrame, metric: str) -> List[Dict[str, Any]]:
        """解析股票数据"""
        stocks = []

        for _, row in df.iterrows():
            try:
                code = str(row.get("代码", ""))
                name = str(row.get("名称", ""))

                change = float(row.get("涨跌幅", 0) or 0)
                price = float(row.get("最新价", 0) or 0)
                amount = float(row.get("成交额", 0) or 0)

                # 市值计算 (成交额 / 换手率 * 100，或直接用总市值字段)
                total_mv = float(row.get("总市值", 0) or 0)
                if total_mv == 0:
                    turnover = float(row.get("换手率", 0) or 0)
                    if turnover > 0:
                        total_mv = amount / turnover * 100
                    else:
                        total_mv = amount

                # PE/PB
                pe = float(row.get("市盈率-动态", 0) or 0)
                pb = float(row.get("市净率", 0) or 0)

                # 行业
                industry = str(row.get("所属行业", "其他"))

                # 市场判断
                if code.startswith("6") or code.startswith("5"):
                    market_tag = "SH"
                elif code.startswith("0") or code.startswith("3"):
                    market_tag = "SZ"
                else:
                    market_tag = "BJ"

                stocks.append(
                    {
                        "code": code,
                        "name": name,
                        "market": market_tag,
                        "industry": industry,
                        "value": round(total_mv / 100000000, 2),  # 亿元
                        "change": round(change, 2),
                        "pe": round(pe, 2) if pe else None,
                        "pb": round(pb, 2) if pb else None,
                        "amount": round(amount / 100000000, 2),  # 亿元
                        "price": round(price, 2),
                    }
                )
            except Exception as e:
                continue

        return stocks

    def _group_by_industry(
        self, stocks: List[Dict], metric: str
    ) -> List[Dict[str, Any]]:
        """按行业分组"""
        industry_map: Dict[str, List[Dict]] = {}

        for stock in stocks:
            industry = stock.get("industry", "其他") or "其他"
            if industry not in industry_map:
                industry_map[industry] = []
            industry_map[industry].append(stock)

        result = []
        for industry_name, children in industry_map.items():
            # 计算行业总市值和加权涨跌幅
            total_value = sum(s["value"] for s in children)
            weighted_change = 0
            if total_value > 0:
                weighted_change = (
                    sum(s["change"] * s["value"] for s in children) / total_value
                )

            # 按市值排序
            children_sorted = sorted(children, key=lambda x: x["value"], reverse=True)

            result.append(
                {
                    "name": industry_name,
                    "value": round(total_value, 2),
                    "change": round(weighted_change, 2),
                    "children": children_sorted,
                }
            )

        # 按行业市值排序
        return sorted(result, key=lambda x: x["value"], reverse=True)

    def _calc_summary(self, df: pd.DataFrame) -> Dict[str, int]:
        """计算市场概览"""
        try:
            changes = df["涨跌幅"]
            up = len(changes[changes > 0])
            down = len(changes[changes < 0])
            flat = len(changes[changes == 0])
            limit_up = len(changes[changes >= 9.9])
            limit_down = len(changes[changes <= -9.9])

            return {
                "up": up,
                "down": down,
                "flat": flat,
                "limit_up": limit_up,
                "limit_down": limit_down,
                "total": len(df),
            }
        except Exception:
            return {
                "up": 0,
                "down": 0,
                "flat": 0,
                "limit_up": 0,
                "limit_down": 0,
                "total": 0,
            }

    async def _get_snapshots(self, market: str, metric: str) -> Dict[str, Any]:
        """获取分时快照 (简化版，返回时间点标记)"""
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        # 交易时间点
        time_slots = [
            "09:30",
            "10:00",
            "10:30",
            "11:00",
            "11:30",
            "13:30",
            "14:00",
            "14:30",
            "15:00",
        ]

        snapshots = {}
        for slot in time_slots:
            # 简化：只标记已过去的时间点为可用
            sh, sm = map(int, slot.split(":"))
            slot_time = now.replace(hour=sh, minute=sm, second=0)

            if now > slot_time:
                snapshots[slot] = {"available": True}
            else:
                snapshots[slot] = {"available": False}

        return snapshots

    def _empty_result(self) -> Dict[str, Any]:
        """返回空结果"""
        return {
            "industries": [],
            "summary": {
                "up": 0,
                "down": 0,
                "flat": 0,
                "limit_up": 0,
                "limit_down": 0,
                "total": 0,
            },
            "snapshots": {},
            "update_time": datetime.now().isoformat(),
        }


cloud_map_service = CloudMapService()
