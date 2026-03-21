# -*- coding: utf-8 -*-
# @version        : 1.1
# @Create Time    : 2026/3/15
# @File           : market_service.py
# @IDE            : PyCharm
# @desc           : 市场服务 - 市场汇总、股票排行，支持多数据源降级

import akshare as ak
import pandas as pd
import requests
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from app.core.logging import get_logger
from app.utils.cache import cache_result
from app.services.pytdx_source import pytdx_source
from app.services.tencent_source import tencent_source
from app.services.sina_source import sina_source

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
                total_amount = (
                    float(df["成交额"].sum()) if "成交额" in df.columns else 0
                )
                total_volume = (
                    float(df["成交量"].sum()) if "成交量" in df.columns else 0
                )
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
                data_dict = dict(zip(df["item"], df["value"]))

                up_stocks = int(float(data_dict.get("上涨", 0)))
                down_stocks = int(float(data_dict.get("下跌", 0)))
                flat_stocks = int(float(data_dict.get("平盘", 0)))
                limit_up_count = int(float(data_dict.get("涨停", 0)))
                limit_down_count = int(float(data_dict.get("跌停", 0)))
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
                logger.info(
                    f"pytdx 获取市场汇总成功: {pytdx_data.get('total_stocks')}只股票"
                )
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
        # 优先使用涨停池数据（包含换手率）
        try:
            stocks = await self._fetch_ranking_from_zt_pool()
            if stocks and len(stocks) > 0:
                logger.info(f"涨停池获取到 {len(stocks)} 条股票数据")
                return stocks
        except Exception as e:
            logger.warning(f"涨停池获取股票数据失败: {e}")

        # 尝试 AKShare 东方财富
        try:
            df = ak.stock_zh_a_spot_em()
            if df is not None and not df.empty:
                df = df[~df["名称"].str.contains("ST|退", na=False)]
                records = df.to_dict("records")
                logger.info(f"AKShare 东方财富获取到 {len(records)} 条股票数据")
                return records
        except Exception as e:
            logger.warning(f"AKShare 东方财富获取股票数据失败: {e}")

        # 尝试腾讯财经批量获取（注意：不包含换手率）
        try:
            tencent_quotes = await tencent_source.get_all_quotes()
            if tencent_quotes:
                records = []
                for q in tencent_quotes:
                    code = q.stock_code
                    if code.startswith("sh"):
                        code = code[2:]
                    elif code.startswith("sz"):
                        code = code[2:]
                    records.append(
                        {
                            "代码": code,
                            "名称": q.stock_name,
                            "最新价": q.price,
                            "涨跌幅": q.change_percent,
                            "涨跌额": q.change,
                            "成交量": q.volume,
                            "成交额": q.amount,
                            "今开": q.open,
                            "最高": q.high,
                            "最低": q.low,
                            "昨收": q.pre_close,
                            "换手率": None,  # 腾讯接口不提供换手率
                        }
                    )
                logger.info(f"腾讯财经获取到 {len(records)} 条股票数据")
                return records
        except Exception as e:
            logger.warning(f"腾讯财经获取股票数据失败: {e}")

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

            # 涨停池列顺序：序号,代码,名称,涨跌幅,最新价,成交量,流通市值,总市值,换手率,封单金额,...
            # 使用 iloc 按位置获取数据，避免编码问题
            if df_zt is not None and not df_zt.empty:
                for _, row in df_zt.iterrows():
                    try:
                        stocks.append(
                            {
                                "代码": str(row.iloc[1]) if len(row) > 1 else "",
                                "名称": str(row.iloc[2]) if len(row) > 2 else "",
                                "最新价": float(row.iloc[4])
                                if len(row) > 4 and pd.notna(row.iloc[4])
                                else 0,
                                "涨跌幅": float(row.iloc[3])
                                if len(row) > 3 and pd.notna(row.iloc[3])
                                else 9.9,
                                "涨跌额": 0,
                                "成交量": float(row.iloc[5])
                                if len(row) > 5 and pd.notna(row.iloc[5])
                                else 0,
                                "成交额": float(row.iloc[9])
                                if len(row) > 9 and pd.notna(row.iloc[9])
                                else 0,
                                "换手率": float(row.iloc[8])
                                if len(row) > 8 and pd.notna(row.iloc[8])
                                else 0,
                            }
                        )
                    except Exception as e:
                        logger.warning(f"解析涨停数据失败: {e}")
                        continue

            # 跌停池列顺序：序号,代码,名称,涨跌幅,最新价,成交量,流通市值,总市值,动态市盈率,换手率,封单金额,...
            # 换手率在位置 [9]
            if df_dt is not None and not df_dt.empty:
                for _, row in df_dt.iterrows():
                    try:
                        stocks.append(
                            {
                                "代码": str(row.iloc[1]) if len(row) > 1 else "",
                                "名称": str(row.iloc[2]) if len(row) > 2 else "",
                                "最新价": float(row.iloc[4])
                                if len(row) > 4 and pd.notna(row.iloc[4])
                                else 0,
                                "涨跌幅": float(row.iloc[3])
                                if len(row) > 3 and pd.notna(row.iloc[3])
                                else -9.9,
                                "涨跌额": 0,
                                "成交量": float(row.iloc[5])
                                if len(row) > 5 and pd.notna(row.iloc[5])
                                else 0,
                                "成交额": float(row.iloc[10])
                                if len(row) > 10 and pd.notna(row.iloc[10])
                                else 0,
                                "换手率": float(row.iloc[9])
                                if len(row) > 9 and pd.notna(row.iloc[9])
                                else 0,
                            }
                        )
                    except Exception as e:
                        logger.warning(f"解析跌停数据失败: {e}")
                        continue

            return stocks if stocks else None

        except Exception as e:
            logger.warning(f"从涨停池获取数据失败: {e}")
            return None

    async def get_change_percent_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取涨跌幅排行"""
        stocks = await self._get_stock_data()
        sorted_stocks = sorted(
            stocks, key=lambda x: x.get("涨跌幅", 0) or 0, reverse=True
        )
        return self._format_ranking(sorted_stocks[:limit])

    async def get_down_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取跌幅排行"""
        # 优先使用新浪数据源获取全市场数据
        try:
            sina_quotes = await sina_source.get_down_ranking(limit=limit)
            if sina_quotes and len(sina_quotes) >= limit:
                logger.info(f"新浪数据源获取跌幅榜 {len(sina_quotes)} 条")
                return self._format_ranking(sina_quotes[:limit])
        except Exception as e:
            logger.warning(f"新浪数据源获取跌幅榜失败: {e}")

        # 备用：涨停池 + 腾讯数据
        stocks = await self._get_stock_data()
        down_stocks = [s for s in stocks if (s.get("涨跌幅", 0) or 0) < 0]
        sorted_stocks = sorted(down_stocks, key=lambda x: x.get("涨跌幅", 0) or 0)

        if len(sorted_stocks) < limit:
            try:
                tencent_quotes = await tencent_source.get_all_quotes()
                if tencent_quotes:
                    all_stocks = []
                    for q in tencent_quotes:
                        if q.change_percent is not None and q.change_percent < 0:
                            code = q.stock_code
                            if code.startswith("sh"):
                                code = code[2:]
                            elif code.startswith("sz"):
                                code = code[2:]
                            all_stocks.append(
                                {
                                    "代码": code,
                                    "名称": q.stock_name,
                                    "最新价": q.price,
                                    "涨跌幅": q.change_percent,
                                    "涨跌额": q.change,
                                    "成交量": q.volume,
                                    "成交额": q.amount,
                                    "换手率": None,
                                }
                            )
                    all_stocks.sort(key=lambda x: x.get("涨跌幅", 0) or 0)
                    existing_codes = {s.get("代码") for s in sorted_stocks}
                    for s in all_stocks:
                        if s.get("代码") not in existing_codes:
                            sorted_stocks.append(s)
                    sorted_stocks.sort(key=lambda x: x.get("涨跌幅", 0) or 0)
                    logger.info(f"跌幅榜补充腾讯数据，共 {len(sorted_stocks)} 条")
            except Exception as e:
                logger.warning(f"补充跌幅榜数据失败: {e}")

        return self._format_ranking(sorted_stocks[:limit])

    async def get_turnover_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取换手率排行"""
        stocks = await self._get_stock_data()
        sorted_stocks = sorted(
            stocks, key=lambda x: x.get("换手率", 0) or 0, reverse=True
        )
        return self._format_ranking(sorted_stocks[:limit])

    async def get_volume_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取成交量排行"""
        stocks = await self._get_stock_data()
        sorted_stocks = sorted(
            stocks, key=lambda x: x.get("成交量", 0) or 0, reverse=True
        )
        return self._format_ranking(sorted_stocks[:limit])

    async def get_amount_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取成交额排行"""
        stocks = await self._get_stock_data()
        sorted_stocks = sorted(
            stocks, key=lambda x: x.get("成交额", 0) or 0, reverse=True
        )
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

            items.append(
                {
                    "rank": idx + 1,
                    "stock_code": code,
                    "stock_name": s.get("名称", ""),
                    "current_price": float(s["最新价"])
                    if pd.notna(s.get("最新价"))
                    else None,
                    "change_percent": float(s["涨跌幅"])
                    if pd.notna(s.get("涨跌幅"))
                    else None,
                    "change_amount": float(s["涨跌额"])
                    if pd.notna(s.get("涨跌额"))
                    else None,
                    "volume": float(s["成交量"]) / 100
                    if pd.notna(s.get("成交量"))
                    else None,
                    "amount": float(s["成交额"]) if pd.notna(s.get("成交额")) else None,
                    "turnover_rate": float(s["换手率"])
                    if pd.notna(s.get("换手率"))
                    else None,
                    "industry": s.get("所属行业", ""),
                    "market": "SH" if code.startswith(("6", "5")) else "SZ",
                }
            )
        return items

    @cache_result(expire=30)
    async def get_limit_up_pool(self) -> Dict[str, Any]:
        """获取涨停池数据，用于涨停热力图"""
        logger.info("获取涨停池数据")

        result = []
        limit_down_count = 0

        try:
            today = datetime.now().strftime("%Y%m%d")

            # 获取涨停池
            df_zt = ak.stock_zt_pool_em(date=today)

            # 获取跌停池
            try:
                df_dt = ak.stock_zt_pool_dtgc_em(date=today)
                limit_down_count = (
                    len(df_dt) if df_dt is not None and not df_dt.empty else 0
                )
            except:
                limit_down_count = 0

            if df_zt is not None and not df_zt.empty:
                logger.info(f"涨停池列名: {df_zt.columns.tolist()}")

                for _, row in df_zt.iterrows():
                    try:
                        item = {
                            "stock_code": str(
                                row.get("代码", row.iloc[1] if len(row) > 1 else "")
                            ),
                            "stock_name": str(
                                row.get("名称", row.iloc[2] if len(row) > 2 else "")
                            ),
                            "industry": str(row.get("所属行业", "")),
                            "concept": str(row.get("涨停原因类别", "")),
                            "limit_up_time": str(row.get("涨停时间", "")),
                            "seal_amount": float(row.get("封板资金", 0) or 0),
                            "continuous_days": int(row.get("连板数", 1) or 1),
                            "change_percent": float(row.get("涨跌幅", 9.9) or 9.9),
                        }
                        result.append(item)
                    except Exception as e:
                        logger.warning(f"解析涨停数据失败: {e}")
                        continue

            logger.info(
                f"获取涨停池数据成功: {len(result)}条涨停, {limit_down_count}条跌停"
            )
            return {
                "limit_up_list": result,
                "limit_down_count": limit_down_count,
                "update_time": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"获取涨停池数据失败: {e}")
            return {
                "limit_up_list": [],
                "limit_down_count": 0,
                "update_time": datetime.now().isoformat(),
            }

    @cache_result(expire=30)
    async def get_up_down_distribution(self) -> Dict[str, Any]:
        """获取涨跌分布数据"""
        logger.info("获取涨跌分布数据")

        try:
            df = ak.stock_zh_a_spot_em()

            if df is None or df.empty:
                return self._empty_distribution()

            # 按涨幅区间统计
            limit_up = len(df[df["涨跌幅"] >= 9.9])
            high_up = len(df[(df["涨跌幅"] >= 7) & (df["涨跌幅"] < 9.9)])
            medium_up = len(df[(df["涨跌幅"] >= 3) & (df["涨跌幅"] < 7)])
            low_up = len(df[(df["涨跌幅"] > 0) & (df["涨跌幅"] < 3)])
            flat = len(df[df["涨跌幅"] == 0])
            low_down = len(df[(df["涨跌幅"] < 0) & (df["涨跌幅"] > -3)])
            medium_down = len(df[(df["涨跌幅"] <= -3) & (df["涨跌幅"] > -7)])
            high_down = len(df[(df["涨跌幅"] <= -7) & (df["涨跌幅"] > -9.9)])
            limit_down = len(df[df["涨跌幅"] <= -9.9])

            up_total = limit_up + high_up + medium_up + low_up
            down_total = limit_down + high_down + medium_down + low_down

            logger.info(f"涨跌分布: 涨{up_total}, 跌{down_total}, 平{flat}")

            return {
                "limitUp": limit_up,
                "highUp": high_up,
                "mediumUp": medium_up,
                "lowUp": low_up,
                "flat": flat,
                "lowDown": low_down,
                "mediumDown": medium_down,
                "highDown": high_down,
                "limitDown": limit_down,
                "upTotal": up_total,
                "downTotal": down_total,
                "flatTotal": flat,
                "update_time": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"获取涨跌分布数据失败: {e}")
            return self._empty_distribution()

    def _empty_distribution(self) -> Dict[str, Any]:
        """返回空的涨跌分布数据"""
        return {
            "limitUp": 0,
            "highUp": 0,
            "mediumUp": 0,
            "lowUp": 0,
            "flat": 0,
            "lowDown": 0,
            "mediumDown": 0,
            "highDown": 0,
            "limitDown": 0,
            "upTotal": 0,
            "downTotal": 0,
            "flatTotal": 0,
            "update_time": datetime.now().isoformat(),
        }


# 创建服务实例
market_service = MarketService()
