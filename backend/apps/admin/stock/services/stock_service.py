#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/10
# @File           : stock_service.py
# @IDE            : PyCharm
# @desc           : 股票服务层 - 封装数据获取逻辑，兼容多种数据源

from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
import akshare as ak
import pandas as pd
from core.logger import logger


# 主要指数代码映射
INDEX_CODES = {
    "sh000001": {"name": "上证指数", "code": "000001.SH"},
    "sz399001": {"name": "深证成指", "code": "399001.SZ"},
    "sz399006": {"name": "创业板指", "code": "399006.SZ"},
    "sh000688": {"name": "科创50", "code": "000688.SH"},
}


class StockIndexService:
    """大盘指数服务类 - 封装指数数据获取逻辑"""

    @staticmethod
    def get_index_quote() -> List[Dict[str, Any]]:
        """
        获取主要指数实时行情

        Returns:
            指数行情列表
        """
        try:
            df = ak.stock_zh_index_spot()
            if df is None or df.empty:
                return []

            main_indices = [v["code"] for v in INDEX_CODES.values()]
            df_main = df[df["代码"].isin(main_indices)]

            items = []
            for _, row in df_main.iterrows():
                items.append({
                    "index_code": row["代码"],
                    "index_name": row["名称"],
                    "current_price": float(row["最新价"]) if pd.notna(row["最新价"]) else None,
                    "change_percent": float(row["涨跌幅"]) if pd.notna(row["涨跌幅"]) else None,
                    "change_amount": float(row["涨跌额"]) if pd.notna(row["涨跌额"]) else None,
                    "volume": float(row["成交量"]) / 100 if pd.notna(row["成交量"]) else None,
                    "amount": float(row["成交额"]) if pd.notna(row["成交额"]) else None,
                })

            return items

        except Exception as e:
            logger.error(f"获取指数行情失败: {str(e)}")
            return []

    @staticmethod
    def get_index_history(
        index_code: str,
        period: str = "daily",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        获取指数历史K线数据

        Args:
            index_code: 指数代码
            period: 周期
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            K线数据列表
        """
        try:
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            if not start_date:
                start_date = (datetime.now() - timedelta(days=300)).strftime("%Y%m%d")

            df = ak.stock_zh_index_daily(symbol=index_code)
            if df is None or df.empty:
                return []

            df["date"] = pd.to_datetime(df["date"])
            start_dt = datetime.strptime(start_date, "%Y%m%d")
            end_dt = datetime.strptime(end_date, "%Y%m%d")
            df = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]

            items = []
            for _, row in df.iterrows():
                items.append({
                    "date": row["date"].strftime("%Y-%m-%d"),
                    "open": float(row["open"]) if pd.notna(row["open"]) else None,
                    "high": float(row["high"]) if pd.notna(row["high"]) else None,
                    "low": float(row["low"]) if pd.notna(row["low"]) else None,
                    "close": float(row["close"]) if pd.notna(row["close"]) else None,
                    "volume": float(row["volume"]) / 100 if pd.notna(row["volume"]) else None,
                    "amount": float(row.get("amount", 0)) if pd.notna(row.get("amount", 0)) else None,
                })

            return items

        except Exception as e:
            logger.error(f"获取指数历史失败: {str(e)}")
            return []


class MarketSummaryService:
    """市场汇总服务类 - 封装市场数据获取逻辑"""

    @staticmethod
    def get_market_summary() -> Dict[str, Any]:
        """
        获取市场汇总数据

        Returns:
            市场汇总数据
        """
        try:
            # 1. 获取主要指数
            index_items = StockIndexService.get_index_quote()

            # 2. 获取市场涨跌统计
            df_stock = ak.stock_zh_a_spot_em()
            if df_stock is not None and not df_stock.empty:
                total_stocks = len(df_stock)
                up_stocks = len(df_stock[df_stock["涨跌幅"] > 0])
                down_stocks = len(df_stock[df_stock["涨跌幅"] < 0])
                flat_stocks = len(df_stock[df_stock["涨跌幅"] == 0])
                total_amount = float(df_stock["成交额"].sum()) if "成交额" in df_stock.columns else 0
                total_volume = float(df_stock["成交量"].sum()) if "成交量" in df_stock.columns else 0
                limit_up_count = len(df_stock[df_stock["涨跌幅"] >= 9.9])
                limit_down_count = len(df_stock[df_stock["涨跌幅"] <= -9.9])
            else:
                total_stocks = up_stocks = down_stocks = flat_stocks = 0
                total_amount = total_volume = 0
                limit_up_count = limit_down_count = 0

            return {
                "indices": index_items,
                "total_stocks": total_stocks,
                "up_stocks": up_stocks,
                "down_stocks": down_stocks,
                "flat_stocks": flat_stocks,
                "total_amount": total_amount,
                "total_volume": total_volume,
                "limit_up_count": limit_up_count,
                "limit_down_count": limit_down_count,
                "trade_date": str(date.today()),
                "update_time": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"获取市场汇总失败: {str(e)}")
            return {}


class StockRankingService:
    """股票排行服务类 - 封装排行数据获取逻辑"""

    def __init__(self):
        """初始化，缓存股票数据"""
        self._stock_cache: Optional[List[Dict[str, Any]]] = None
        self._cache_time: Optional[datetime] = None

    def _get_stock_data(self) -> List[Dict[str, Any]]:
        """获取股票数据（带缓存）"""
        now = datetime.now()
        # 缓存 30 秒
        if self._stock_cache and self._cache_time:
            if (now - self._cache_time).seconds < 30:
                return self._stock_cache

        try:
            df = ak.stock_zh_a_spot_em()
            if df is None or df.empty:
                return []

            # 过滤 ST 股票和退市股票
            df = df[~df["名称"].str.contains("ST|退", na=False)]
            df = df[df["代码"].str.startswith(("sh", "sz"))]

            self._stock_cache = df.to_dict("records")
            self._cache_time = now
            return self._stock_cache

        except Exception as e:
            logger.error(f"获取股票数据失败: {str(e)}")
            return self._stock_cache or []

    def get_change_percent_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取涨跌幅排行"""
        stocks = self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("涨跌幅", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    def get_turnover_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取换手率排行"""
        stocks = self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("换手率", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    def get_volume_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取成交量排行"""
        stocks = self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("成交量", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    def get_amount_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取成交额排行"""
        stocks = self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("成交额", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    def _format_ranking(self, stocks: List[Dict]) -> List[Dict[str, Any]]:
        """格式化排行数据"""
        items = []
        for idx, s in enumerate(stocks):
            items.append({
                "rank": idx + 1,
                "stock_code": s.get("代码", ""),
                "stock_name": s.get("名称", ""),
                "current_price": float(s["最新价"]) if pd.notna(s.get("最新价")) else None,
                "change_percent": float(s["涨跌幅"]) if pd.notna(s.get("涨跌幅")) else None,
                "volume": float(s["成交量"]) / 100 if pd.notna(s.get("成交量")) else None,
                "amount": float(s["成交额"]) if pd.notna(s.get("成交额")) else None,
                "turnover_rate": float(s["换手率"]) if pd.notna(s.get("换手率")) else None,
                "industry": s.get("所属行业", ""),
                "market": "SH" if str(s.get("代码", "")).startswith("sh") else "SZ",
            })
        return items


# 全局服务实例
stock_index_service = StockIndexService()
market_summary_service = MarketSummaryService()
stock_ranking_service = StockRankingService()