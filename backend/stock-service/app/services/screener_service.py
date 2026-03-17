# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : screener_service.py
# @IDE            : PyCharm
# @desc           : 股票筛选器服务 - 条件选股、形态选股、财务筛选

import akshare as ak
import pandas as pd
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)


@dataclass
class ScreenerResult:
    stock_code: str
    stock_name: str
    price: Optional[float]
    change_percent: Optional[float]
    match_score: float
    match_reasons: List[str] = field(default_factory=list)


class ScreenerService:
    @cache_result(expire=60)
    async def _get_all_stocks(self) -> pd.DataFrame:
        try:
            return ak.stock_zh_a_spot_em()
        except Exception as e:
            logger.error(f"获取股票数据失败: {e}")
            return pd.DataFrame()

    async def screen_by_condition(
        self, conditions: List[Dict[str, Any]], limit: int = 50
    ) -> List[ScreenerResult]:
        logger.info(f"条件选股: {len(conditions)}个条件")

        df = await self._get_all_stocks()
        if df.empty:
            return []

        field_map = {
            "price": "最新价",
            "change_percent": "涨跌幅",
            "volume": "成交量",
            "amount": "成交额",
            "turnover_rate": "换手率",
            "pe_ratio": "市盈率-动态",
            "pb_ratio": "市净率",
            "market_cap": "总市值",
            "amplitude": "振幅",
        }

        for cond in conditions:
            col = field_map.get(cond.get("field"), cond.get("field"))
            if col not in df.columns:
                continue
            series = pd.to_numeric(df[col], errors="coerce")
            op, val = cond.get("operator"), cond.get("value")
            if op == "gt":
                df = df[series > val]
            elif op == "lt":
                df = df[series < val]
            elif op == "gte":
                df = df[series >= val]
            elif op == "lte":
                df = df[series <= val]
            elif op == "between":
                df = df[(series >= val) & (series <= cond.get("value2"))]

        results = []
        for _, row in df.head(limit).iterrows():
            results.append(
                ScreenerResult(
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    price=float(row.get("最新价", 0))
                    if pd.notna(row.get("最新价"))
                    else None,
                    change_percent=float(row.get("涨跌幅", 0))
                    if pd.notna(row.get("涨跌幅"))
                    else None,
                    match_score=100.0,
                    match_reasons=[f"满足{len(conditions)}个条件"],
                )
            )
        return results

    async def screen_limit_up(self, limit: int = 50) -> List[ScreenerResult]:
        df = await self._get_all_stocks()
        if df.empty:
            return []
        df = df[df["涨跌幅"] >= 9.5]
        return [
            ScreenerResult(
                stock_code=str(r.get("代码", "")),
                stock_name=str(r.get("名称", "")),
                price=float(r.get("最新价", 0)) if pd.notna(r.get("最新价")) else None,
                change_percent=float(r.get("涨跌幅", 0))
                if pd.notna(r.get("涨跌幅"))
                else None,
                match_score=100.0,
                match_reasons=["涨停"],
            )
            for _, r in df.head(limit).iterrows()
        ]

    async def screen_limit_down(self, limit: int = 50) -> List[ScreenerResult]:
        df = await self._get_all_stocks()
        if df.empty:
            return []
        df = df[df["涨跌幅"] <= -9.5]
        return [
            ScreenerResult(
                stock_code=str(r.get("代码", "")),
                stock_name=str(r.get("名称", "")),
                price=float(r.get("最新价", 0)) if pd.notna(r.get("最新价")) else None,
                change_percent=float(r.get("涨跌幅", 0))
                if pd.notna(r.get("涨跌幅"))
                else None,
                match_score=100.0,
                match_reasons=["跌停"],
            )
            for _, r in df.head(limit).iterrows()
        ]

    async def screen_high_turnover(self, limit: int = 50) -> List[ScreenerResult]:
        df = await self._get_all_stocks()
        if df.empty:
            return []
        df = df[df["换手率"] > 10].sort_values("换手率", ascending=False)
        return [
            ScreenerResult(
                stock_code=str(r.get("代码", "")),
                stock_name=str(r.get("名称", "")),
                price=float(r.get("最新价", 0)) if pd.notna(r.get("最新价")) else None,
                change_percent=float(r.get("涨跌幅", 0))
                if pd.notna(r.get("涨跌幅"))
                else None,
                match_score=float(r.get("换手率", 0))
                if pd.notna(r.get("换手率"))
                else 0,
                match_reasons=[f"换手率: {r.get('换手率', 0):.2f}%"],
            )
            for _, r in df.head(limit).iterrows()
        ]

    async def screen_low_pe(self, limit: int = 50) -> List[ScreenerResult]:
        df = await self._get_all_stocks()
        if df.empty:
            return []
        df = df[(df["市盈率-动态"] > 0) & (df["市盈率-动态"] < 20)].sort_values(
            "市盈率-动态"
        )
        return [
            ScreenerResult(
                stock_code=str(r.get("代码", "")),
                stock_name=str(r.get("名称", "")),
                price=float(r.get("最新价", 0)) if pd.notna(r.get("最新价")) else None,
                change_percent=float(r.get("涨跌幅", 0))
                if pd.notna(r.get("涨跌幅"))
                else None,
                match_score=100 - float(r.get("市盈率-动态", 0))
                if pd.notna(r.get("市盈率-动态"))
                else 0,
                match_reasons=[f"市盈率: {r.get('市盈率-动态', 0):.2f}"],
            )
            for _, r in df.head(limit).iterrows()
        ]

    async def screen_volume_surge(self, limit: int = 50) -> List[ScreenerResult]:
        df = await self._get_all_stocks()
        if df.empty:
            return []
        df["amount_rank"] = df["成交额"].rank(pct=True)
        df = df[df["amount_rank"] > 0.9]
        return [
            ScreenerResult(
                stock_code=str(r.get("代码", "")),
                stock_name=str(r.get("名称", "")),
                price=float(r.get("最新价", 0)) if pd.notna(r.get("最新价")) else None,
                change_percent=float(r.get("涨跌幅", 0))
                if pd.notna(r.get("涨跌幅"))
                else None,
                match_score=float(r.get("成交额", 0))
                if pd.notna(r.get("成交额"))
                else 0,
                match_reasons=[f"成交额: {r.get('成交额', 0) / 1e8:.2f}亿"],
            )
            for _, r in df.head(limit).iterrows()
        ]

    async def screen_small_cap(self, limit: int = 50) -> List[ScreenerResult]:
        df = await self._get_all_stocks()
        if df.empty:
            return []
        df = df[df["总市值"] < 5e9].sort_values("总市值")
        return [
            ScreenerResult(
                stock_code=str(r.get("代码", "")),
                stock_name=str(r.get("名称", "")),
                price=float(r.get("最新价", 0)) if pd.notna(r.get("最新价")) else None,
                change_percent=float(r.get("涨跌幅", 0))
                if pd.notna(r.get("涨跌幅"))
                else None,
                match_score=100 - float(r.get("总市值", 0)) / 5e9 * 100
                if pd.notna(r.get("总市值"))
                else 0,
                match_reasons=[f"市值: {r.get('总市值', 0) / 1e8:.2f}亿"],
            )
            for _, r in df.head(limit).iterrows()
        ]


screener_service = ScreenerService()
