#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : factor_engine.py
# @IDE            : PyCharm
# @desc           : 多因子计算引擎

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
from utils.akshare_enhanced import get_ak_enhanced
from core.logger import logger


class FactorEngine:
    """多因子计算引擎"""

    def __init__(self):
        self.ak = get_ak_enhanced()

    async def calculate_all_factors(self, stock: str) -> Dict[str, Any]:
        """计算单只股票的所有因子"""
        result = {
            "stock_code": stock,
            "trade_date": datetime.now(),
            "value_score": 0,
            "growth_score": 0,
            "quality_score": 0,
            "momentum_score": 0,
            "composite_score": 0,
        }

        try:
            value_factors = await self.calculate_value_factors(stock)
            growth_factors = await self.calculate_growth_factors(stock)
            quality_factors = await self.calculate_quality_factors(stock)
            momentum_factors = await self.calculate_momentum_factors(stock)

            result.update(value_factors)
            result.update(growth_factors)
            result.update(quality_factors)
            result.update(momentum_factors)

            result["value_score"] = self._calculate_value_score(value_factors)
            result["growth_score"] = self._calculate_growth_score(growth_factors)
            result["quality_score"] = self._calculate_quality_score(quality_factors)
            result["momentum_score"] = self._calculate_momentum_score(momentum_factors)

            result["composite_score"] = (
                result["value_score"] * 0.25
                + result["growth_score"] * 0.25
                + result["quality_score"] * 0.25
                + result["momentum_score"] * 0.25
            )

        except Exception as e:
            logger.error(f"计算因子失败: {stock}, 错误: {e}")

        return result

    async def calculate_value_factors(self, stock: str) -> Dict[str, Any]:
        """计算价值因子"""
        factors = {
            "pe": None,
            "pb": None,
            "ps": None,
            "pcf": None,
            "pe_percentile": None,
            "pb_percentile": None,
        }

        try:
            df = await self.ak.get_financial_abstract(stock)
            if df is not None and not df.empty:
                if "市盈率" in df.columns:
                    factors["pe"] = (
                        float(df["市盈率"].iloc[-1])
                        if pd.notna(df["市盈率"].iloc[-1])
                        else None
                    )
                if "市净率" in df.columns:
                    factors["pb"] = (
                        float(df["市净率"].iloc[-1])
                        if pd.notna(df["市净率"].iloc[-1])
                        else None
                    )
                if "市销率" in df.columns:
                    factors["ps"] = (
                        float(df["市销率"].iloc[-1])
                        if pd.notna(df["市销率"].iloc[-1])
                        else None
                    )
                if "市现率" in df.columns:
                    factors["pcf"] = (
                        float(df["市现率"].iloc[-1])
                        if pd.notna(df["市现率"].iloc[-1])
                        else None
                    )

        except Exception as e:
            logger.error(f"获取价值因子失败: {stock}, {e}")

        return factors

    async def calculate_growth_factors(self, stock: str) -> Dict[str, Any]:
        """计算成长因子"""
        factors = {
            "revenue_growth": None,
            "profit_growth": None,
        }

        try:
            df = await self.ak.get_financial_indicators(stock)
            if df is not None and not df.empty:
                if "营业收入增长率" in df.columns:
                    factors["revenue_growth"] = (
                        float(df["营业收入增长率"].iloc[-1])
                        if pd.notna(df["营业收入增长率"].iloc[-1])
                        else None
                    )
                if "净利润增长率" in df.columns:
                    factors["profit_growth"] = (
                        float(df["净利润增长率"].iloc[-1])
                        if pd.notna(df["净利润增长率"].iloc[-1])
                        else None
                    )

        except Exception as e:
            logger.error(f"获取成长因子失败: {stock}, {e}")

        return factors

    async def calculate_quality_factors(self, stock: str) -> Dict[str, Any]:
        """计算质量因子"""
        factors = {
            "roe": None,
            "roa": None,
            "gross_margin": None,
            "net_margin": None,
            "debt_ratio": None,
        }

        try:
            df = await self.ak.get_financial_indicators(stock)
            if df is not None and not df.empty:
                if "净资产收益率" in df.columns:
                    factors["roe"] = (
                        float(df["净资产收益率"].iloc[-1])
                        if pd.notna(df["净资产收益率"].iloc[-1])
                        else None
                    )
                if "总资产收益率" in df.columns:
                    factors["roa"] = (
                        float(df["总资产收益率"].iloc[-1])
                        if pd.notna(df["总资产收益率"].iloc[-1])
                        else None
                    )
                if "毛利率" in df.columns:
                    factors["gross_margin"] = (
                        float(df["毛利率"].iloc[-1])
                        if pd.notna(df["毛利率"].iloc[-1])
                        else None
                    )
                if "净利率" in df.columns:
                    factors["net_margin"] = (
                        float(df["净利率"].iloc[-1])
                        if pd.notna(df["净利率"].iloc[-1])
                        else None
                    )
                if "资产负债率" in df.columns:
                    factors["debt_ratio"] = (
                        float(df["资产负债率"].iloc[-1])
                        if pd.notna(df["资产负债率"].iloc[-1])
                        else None
                    )

        except Exception as e:
            logger.error(f"获取质量因子失败: {stock}, {e}")

        return factors

    async def calculate_momentum_factors(self, stock: str) -> Dict[str, Any]:
        """计算动量因子"""
        factors = {
            "change_5d": None,
            "change_20d": None,
            "change_60d": None,
            "change_120d": None,
            "relative_strength": None,
        }

        try:
            df = await self.ak.get_stock_price_change(stock)
            if df is not None and not df.empty:
                if "5日" in df.columns:
                    factors["change_5d"] = (
                        float(df["5日"].iloc[0])
                        if pd.notna(df["5日"].iloc[0])
                        else None
                    )
                if "20日" in df.columns:
                    factors["change_20d"] = (
                        float(df["20日"].iloc[0])
                        if pd.notna(df["20日"].iloc[0])
                        else None
                    )
                if "60日" in df.columns:
                    factors["change_60d"] = (
                        float(df["60日"].iloc[0])
                        if pd.notna(df["60日"].iloc[0])
                        else None
                    )
                if "年初至今" in df.columns:
                    factors["change_120d"] = (
                        float(df["年初至今"].iloc[0])
                        if pd.notna(df["年初至今"].iloc[0])
                        else None
                    )

        except Exception as e:
            logger.error(f"获取动量因子失败: {stock}, {e}")

        return factors

    def _calculate_value_score(self, factors: Dict[str, Any]) -> float:
        """计算价值因子得分 (0-100)"""
        score = 50

        if factors.get("pe"):
            pe = factors["pe"]
            if 0 < pe < 10:
                score += 30
            elif 10 <= pe < 20:
                score += 15
            elif 20 <= pe < 30:
                score += 0
            else:
                score -= 20

        if factors.get("pb"):
            pb = factors["pb"]
            if 0 < pb < 1:
                score += 20
            elif 1 <= pb < 2:
                score += 10
            elif 2 <= pb < 3:
                score += 0
            else:
                score -= 10

        return max(0, min(100, score))

    def _calculate_growth_score(self, factors: Dict[str, Any]) -> float:
        """计算成长因子得分 (0-100)"""
        score = 50

        if factors.get("revenue_growth"):
            growth = factors["revenue_growth"]
            if growth > 30:
                score += 30
            elif growth > 15:
                score += 15
            elif growth > 0:
                score += 0
            else:
                score -= 20

        if factors.get("profit_growth"):
            profit = factors["profit_growth"]
            if profit > 30:
                score += 20
            elif profit > 15:
                score += 10
            elif profit > 0:
                score += 0
            else:
                score -= 10

        return max(0, min(100, score))

    def _calculate_quality_score(self, factors: Dict[str, Any]) -> float:
        """计算质量因子得分 (0-100)"""
        score = 50

        if factors.get("roe"):
            roe = factors["roe"]
            if roe > 20:
                score += 30
            elif roe > 10:
                score += 15
            elif roe > 5:
                score += 0
            else:
                score -= 20

        if factors.get("gross_margin"):
            margin = factors["gross_margin"]
            if margin > 40:
                score += 20
            elif margin > 20:
                score += 10
            else:
                score -= 5

        if factors.get("debt_ratio"):
            debt = factors["debt_ratio"]
            if debt < 30:
                score += 10
            elif debt < 50:
                score += 0
            else:
                score -= 15

        return max(0, min(100, score))

    def _calculate_momentum_score(self, factors: Dict[str, Any]) -> float:
        """计算动量因子得分 (0-100)"""
        score = 50

        if factors.get("change_20d"):
            change = factors["change_20d"]
            if change > 20:
                score += 30
            elif change > 10:
                score += 15
            elif change > 0:
                score += 5
            elif change > -10:
                score -= 10
            else:
                score -= 20

        if factors.get("change_60d"):
            change = factors["change_60d"]
            if change > 30:
                score += 20
            elif change > 15:
                score += 10
            elif change > 0:
                score += 0
            else:
                score -= 10

        return max(0, min(100, score))

    async def batch_calculate(self, stocks: List[str]) -> List[Dict[str, Any]]:
        """批量计算多只股票的因子"""
        tasks = [self.calculate_all_factors(stock) for stock in stocks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if isinstance(r, dict)]


_factor_engine_instance: Optional[FactorEngine] = None


def get_factor_engine() -> FactorEngine:
    """获取因子计算引擎单例"""
    global _factor_engine_instance
    if _factor_engine_instance is None:
        _factor_engine_instance = FactorEngine()
    return _factor_engine_instance
