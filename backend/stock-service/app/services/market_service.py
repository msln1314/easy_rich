# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/15
# @File           : market_service.py
# @IDE            : PyCharm
# @desc           : 市场服务 - 市场汇总、股票排行

import akshare as ak
import pandas as pd
import requests
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from app.core.logging import get_logger
from app.utils.cache import cache_result
from app.services.pytdx_source import pytdx_source

logger = get_logger(__name__)


@dataclass
class MarketSummary:
    """市场汇总数据"""
    total_stocks: int
    up_stocks: int
    down_stocks: int
    flat_stocks: int
    total_amount: float
    total_volume: float
    limit_up_count: int
    limit_down_count: int
    trade_date: str
    update_time: str


@dataclass
class StockRankingItem:
    """股票排行项"""
    rank: int
    stock_code: str
    stock_name: str
    current_price: Optional[float]
    change_percent: Optional[float]
    volume: Optional[float]
    amount: Optional[float]
    turnover_rate: Optional[float]
    industry: Optional[str]
    market: str


# 新浪股票接口配置
SINA_STOCK_URL = "http://hq.sinajs.cn/list="


class MarketService:
    """市场服务"""

    _stock_cache: List[Dict[str, Any]] = []
    _cache_time: Optional[datetime] = None

    @cache_result(expire=30)  # 缓存30秒
    async def get_market_summary(self) -> Dict[str, Any]:
        """
        获取市场汇总数据

        Returns:
            市场汇总数据
        """
        logger.info("获取市场汇总数据")

        # 尝试 AKShare 东方财富接口
        try:
            df = ak.stock_zh_a_spot_em()

            if df is not None and not df.empty:
                total_stocks = len(df)
                up_stocks = len(df[df["涨跌幅"] > 0])
                down_stocks = len(df[df["涨跌幅"] < 0])
                flat_stocks = len(df[df["涨跌幅"] == 0])
                total_amount = float(df["成交额"].sum()) if "成交额" in df.columns else 0
                total_volume = float(df["成交量"].sum()) if "成交量" in df.columns else 0
                limit_up_count = len(df[df["涨跌幅"] >= 9.9])
                limit_down_count = len(df[df["涨跌幅"] <= -9.9])

                logger.info(f"AKShare 东方财富获取市场汇总成功: {total_stocks}只股票")
                return {
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
            logger.warning(f"AKShare 东方财富获取市场汇总失败: {e}")

        # 尝试使用大盘氛围接口（乐股网）
        try:
            df = ak.stock_market_activity_legu()
            if df is not None and not df.empty:
                # 解析数据
                data_dict = dict(zip(df['item'], df['value']))

                up_stocks = int(float(data_dict.get('上涨', 0)))
                down_stocks = int(float(data_dict.get('下跌', 0)))
                flat_stocks = int(float(data_dict.get('平盘', 0)))
                limit_up_count = int(float(data_dict.get('涨停', 0)))
                limit_down_count = int(float(data_dict.get('跌停', 0)))
                total_stocks = up_stocks + down_stocks + flat_stocks

                logger.info(f"乐股网获取市场汇总成功: {total_stocks}只股票")
                return {
                    "total_stocks": total_stocks,
                    "up_stocks": up_stocks,
                    "down_stocks": down_stocks,
                    "flat_stocks": flat_stocks,
                    "total_amount": 0,  # 该接口不提供成交额
                    "total_volume": 0,
                    "limit_up_count": limit_up_count,
                    "limit_down_count": limit_down_count,
                    "trade_date": str(date.today()),
                    "update_time": datetime.now().isoformat(),
                }

        except Exception as e:
            logger.warning(f"乐股网获取市场汇总失败: {e}")

        # 尝试使用 pytdx 数据源
        try:
            pytdx_data = await pytdx_source.get_market_summary()
            if pytdx_data and pytdx_data.get("total_stocks", 0) > 0:
                logger.info(f"pytdx 获取市场汇总成功: {pytdx_data.get('total_stocks')}只股票")
                return pytdx_data
        except Exception as e:
            logger.warning(f"pytdx 获取市场汇总失败: {e}")

        # 返回空数据
        logger.error("所有数据源均无法获取市场汇总")
        return self._empty_summary()

    def _empty_summary(self) -> Dict[str, Any]:
        """返回空的汇总数据"""
        return {
            "total_stocks": 0,
            "up_stocks": 0,
            "down_stocks": 0,
            "flat_stocks": 0,
            "total_amount": 0,
            "total_volume": 0,
            "limit_up_count": 0,
            "limit_down_count": 0,
            "trade_date": str(date.today()),
            "update_time": datetime.now().isoformat(),
        }

    async def _get_stock_data(self) -> List[Dict[str, Any]]:
        """获取股票数据（带缓存）"""
        now = datetime.now()
        # 缓存 30 秒
        if self._stock_cache and self._cache_time:
            if (now - self._cache_time).seconds < 30:
                return self._stock_cache

        # 获取新数据
        stocks = await self._fetch_stock_data()
        if stocks:
            self._stock_cache = stocks
            self._cache_time = now
            return stocks

        return self._stock_cache or []

    @cache_result(expire=30)
    async def _fetch_stock_data(self) -> Optional[List[Dict[str, Any]]]:
        """获取股票数据"""
        # 尝试 AKShare 东方财富
        try:
            df = ak.stock_zh_a_spot_em()
            if df is not None and not df.empty:
                # 过滤 ST 股票和退市股票
                df = df[~df["名称"].str.contains("ST|退", na=False)]
                records = df.to_dict("records")
                logger.info(f"AKShare 东方财富获取到 {len(records)} 条股票数据")
                return records
        except Exception as e:
            logger.warning(f"AKShare 东方财富获取股票数据失败: {e}")

        # 尝试使用涨停池+跌停池构建排行数据
        try:
            stocks = await self._fetch_ranking_from_zt_pool()
            if stocks:
                logger.info(f"涨停池获取到 {len(stocks)} 条股票数据")
                return stocks
        except Exception as e:
            logger.warning(f"涨停池获取股票数据失败: {e}")

        # 尝试使用 pytdx 数据源
        try:
            pytdx_stocks = await pytdx_source.get_stock_list(limit=2000)
            if pytdx_stocks:
                logger.info(f"pytdx 获取到 {len(pytdx_stocks)} 条股票数据")
                return pytdx_stocks
        except Exception as e:
            logger.warning(f"pytdx 获取股票数据失败: {e}")

        return None

    async def _fetch_ranking_from_zt_pool(self) -> Optional[List[Dict[str, Any]]]:
        """从涨停池获取排行数据"""
        try:
            today = datetime.now().strftime("%Y%m%d")

            # 获取涨停池
            df_zt = ak.stock_zt_pool_em(date=today)

            # 获取跌停池
            try:
                df_dt = ak.stock_zt_pool_dtgc_em(date=today)
            except:
                df_dt = pd.DataFrame()

            stocks = []

            # 处理涨停股票
            if df_zt is not None and not df_zt.empty:
                for _, row in df_zt.iterrows():
                    stocks.append({
                        "代码": row.get("代码", ""),
                        "名称": row.get("名称", ""),
                        "最新价": row.get("最新价", 0),
                        "涨跌幅": row.get("涨跌幅", 9.9),
                        "涨跌额": row.get("涨跌额", 0),
                        "成交量": row.get("成交量", 0),
                        "成交额": row.get("成交额", 0),
                        "换手率": row.get("换手率", 0),
                    })

            # 处理跌停股票
            if df_dt is not None and not df_dt.empty:
                for _, row in df_dt.iterrows():
                    stocks.append({
                        "代码": row.get("代码", ""),
                        "名称": row.get("名称", ""),
                        "最新价": row.get("最新价", 0),
                        "涨跌幅": row.get("涨跌幅", -9.9),
                        "涨跌额": row.get("涨跌额", 0),
                        "成交量": row.get("成交量", 0),
                        "成交额": row.get("成交额", 0),
                        "换手率": row.get("换手率", 0),
                    })

            return stocks if stocks else None

        except Exception as e:
            logger.warning(f"从涨停池获取数据失败: {e}")
            return None

    async def get_change_percent_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取涨跌幅排行"""
        stocks = await self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("涨跌幅", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    async def get_down_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取跌幅排行"""
        stocks = await self._get_stock_data()
        # 筛选跌幅为负的股票
        down_stocks = [s for s in stocks if (s.get("涨跌幅", 0) or 0) < 0]
        sorted_stocks = sorted(down_stocks, key=lambda x: x.get("涨跌幅", 0) or 0)
        return self._format_ranking(sorted_stocks[:limit])

    async def get_turnover_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取换手率排行"""
        stocks = await self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("换手率", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    async def get_volume_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取成交量排行"""
        stocks = await self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("成交量", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    async def get_amount_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取成交额排行"""
        stocks = await self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("成交额", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    async def get_realtime_rankings(self, limit: int = 20) -> Dict[str, Any]:
        """
        获取所有实时排行

        Returns:
            包含涨幅榜、跌幅榜、换手率榜、成交额榜的字典
        """
        logger.info("获取实时排行数据")

        change_ranking = await self.get_change_percent_ranking(limit)
        down_ranking = await self.get_down_ranking(limit)
        turnover_ranking = await self.get_turnover_ranking(limit)
        amount_ranking = await self.get_amount_ranking(limit)

        return {
            "change_percent_ranking": change_ranking,
            "down_ranking": down_ranking,
            "turnover_ranking": turnover_ranking,
            "amount_ranking": amount_ranking,
            "update_time": datetime.now().isoformat(),
        }

    def _format_ranking(self, stocks: List[Dict]) -> List[Dict[str, Any]]:
        """格式化排行数据"""
        items = []
        for idx, s in enumerate(stocks):
            code = str(s.get("代码", ""))
            if not code:
                continue

            items.append({
                "rank": idx + 1,
                "stock_code": code,
                "stock_name": s.get("名称", ""),
                "current_price": float(s["最新价"]) if pd.notna(s.get("最新价")) else None,
                "change_percent": float(s["涨跌幅"]) if pd.notna(s.get("涨跌幅")) else None,
                "change_amount": float(s["涨跌额"]) if pd.notna(s.get("涨跌额")) else None,
                "volume": float(s["成交量"]) / 100 if pd.notna(s.get("成交量")) else None,
                "amount": float(s["成交额"]) if pd.notna(s.get("成交额")) else None,
                "turnover_rate": float(s["换手率"]) if pd.notna(s.get("换手率")) else None,
                "industry": s.get("所属行业", ""),
                "market": "SH" if code.startswith(("6", "5")) else "SZ",
            })
        return items


# 创建服务实例
market_service = MarketService()