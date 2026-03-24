# 导入本地版本的 akshare 代理补丁 (已禁用)
# try:
#     from app.utils.akshare_proxy_patch import install_patch
#     install_patch("127.0.0.1", "", 60)  # auth_token 为空时不使用代理
# except ImportError as e:
#     print(f"警告：无法导入 akshare 代理补丁: {e}")
#     pass

import akshare as ak
import pandas as pd  # 添加pandas导入
from datetime import datetime, timedelta  # 添加timedelta导入
from typing import List, Optional, Any, Dict

# 更新导入语句
from app.models.stock_models import (
    StockInfo,
    StockQuote,
    StockFinancial,
    StockFundFlow,
    StockHistory,
)
from app.core.logging import get_logger
from app.utils.cache import cache_result
from app.services.gm_service import gm_service
from app.services.tencent_source import tencent_source  # 腾讯财经 - 成功率高
from app.services.baostock_source import baostock_source  # 证券宝 - 免费稳定

logger = get_logger(__name__)


class StockService:
    @cache_result()
    async def get_stock_info(self, stock_code: str) -> StockInfo:
        """
        获取个股基本信息
        优先使用 AKShare，失败时自动降级到 GM
        """
        logger.info(f"获取个股基本信息: {stock_code}")

        try:
            # 首先尝试使用 AKShare
            stock_info = ak.stock_individual_info_em(symbol=stock_code)

            # 处理数据并返回
            if stock_info.empty:
                logger.warning(f"未找到股票代码 {stock_code} 的基本信息")
                raise ValueError(f"未找到股票代码 {stock_code} 的基本信息")

            # 创建字典用于存储信息
            info_dict = {}
            for _, row in stock_info.iterrows():
                # 使用iloc进行位置索引，而不是直接使用[]
                info_dict[row.iloc[0]] = row.iloc[1]

            # 处理上市时间，确保是字符串类型
            listing_date = info_dict.get("上市时间")
            if listing_date is not None:
                # 将上市时间转换为字符串类型
                listing_date = str(listing_date)

            # 处理数据并返回
            return StockInfo(
                code=stock_code,
                name=info_dict.get("股票简称", ""),
                industry=info_dict.get("行业", None),
                listing_date=listing_date,  # 使用转换后的字符串
                total_market_value=float(info_dict.get("总市值", 0))
                if info_dict.get("总市值")
                else None,
                circulating_market_value=float(info_dict.get("流通市值", 0))
                if info_dict.get("流通市值")
                else None,
                total_share=float(info_dict.get("总股本", 0))
                if info_dict.get("总股本")
                else None,
                circulating_share=float(info_dict.get("流通股", 0))
                if info_dict.get("流通股")
                else None,
            )

        except Exception as e:
            logger.warning(f"AKShare 获取个股基本信息失败: {str(e)}，尝试使用 GM 服务")

            if not gm_service.is_available():
                logger.error("GM 服务不可用")
                raise ValueError(
                    f"无法获取股票 {stock_code} 的基本信息，AKShare 和 GM 均失败"
                )

            try:
                return await self._get_stock_info_from_gm(stock_code)
            except Exception as gm_error:
                logger.error(f"GM 获取个股基本信息失败: {str(gm_error)}")
                raise ValueError(
                    f"无法获取股票 {stock_code} 的基本信息，AKShare 失败: {str(e)}，GM 失败: {str(gm_error)}"
                )

    async def _get_stock_info_from_gm(self, stock_code: str) -> StockInfo:
        """
        从 GM 服务获取个股基本信息
        """
        logger.info(f"使用 GM 获取个股基本信息: {stock_code}")

        try:
            # 使用 GM 的 get_instruments 方法获取标的列表
            # 注意：GM 需要使用完整的 symbol 格式，如 SHSE.600000
            gm_symbol = self._convert_to_gm_symbol(stock_code)
            logger.info(f"GM 代码转换: {stock_code} -> {gm_symbol}")

            instruments = gm_service.gm.get_instruments(symbols=[gm_symbol])

            if not instruments or len(instruments) == 0:
                logger.warning(f"GM 未找到股票 {stock_code} 的基本信息")
                raise ValueError(f"未找到股票 {stock_code} 的基本信息")

            inst = instruments[0]

            return StockInfo(
                code=stock_code,
                name=inst.get("name", ""),
                industry=inst.get("sec_name", ""),  # GM 可能没有行业信息
                listing_date=inst.get("list_date", ""),
                total_market_value=None,  # 需要通过其他方式获取
                circulating_market_value=None,
                total_share=None,
                circulating_share=None,
            )
        except Exception as e:
            logger.error(f"GM 获取个股基本信息失败: {str(e)}")
            raise

    async def get_stock_quote(self, stock_code: str) -> StockQuote:
        """
        获取个股实时行情
        优先级: AKShare → 腾讯财经 → GM
        """
        logger.info(f"获取个股实时行情: {stock_code}")

        try:
            # 首先尝试使用 AKShare
            stock_quote = ak.stock_zh_a_spot_em()

            # 筛选指定股票并处理数据
            stock_data = stock_quote[stock_quote["代码"] == stock_code]
            if stock_data.empty:
                logger.warning(f"未找到股票代码 {stock_code} 的行情数据")
                raise ValueError(f"未找到股票代码 {stock_code} 的行情数据")

            # 获取第一行数据
            row = stock_data.iloc[0]

            # 创建并返回StockQuote对象，确保包含所有必需字段
            return StockQuote(
                code=stock_code,
                name=row["名称"],
                price=float(row["最新价"]),
                change=float(row["涨跌额"]),
                change_percent=float(row["涨跌幅"]),
                open=float(row["今开"]),
                high=float(row["最高"]),
                low=float(row["最低"]),
                volume=int(row["成交量"]),
                amount=float(row["成交额"]),
                turnover_rate=float(row["换手率"]),
                pe_ratio=float(row["市盈率-动态"])
                if "市盈率-动态" in row and not pd.isna(row["市盈率-动态"])
                else None,
                pb_ratio=float(row["市净率"])
                if "市净率" in row and not pd.isna(row["市净率"])
                else None,
                market_cap=float(row["总市值"])
                if "总市值" in row and not pd.isna(row["总市值"])
                else None,
                update_time=datetime.now(),
            )

        except Exception as e:
            logger.warning(f"AKShare 获取个股实时行情失败: {str(e)}，尝试使用腾讯财经")

            # 优先尝试腾讯财经（成功率高）
            try:
                tencent_quote = await tencent_source.get_quote(stock_code)
                if tencent_quote:
                    return StockQuote(
                        code=stock_code,
                        name=tencent_quote.stock_name,
                        price=tencent_quote.price,
                        change=tencent_quote.change,
                        change_percent=tencent_quote.change_percent,
                        open=tencent_quote.open,
                        high=tencent_quote.high,
                        low=tencent_quote.low,
                        volume=int(tencent_quote.volume)
                        if tencent_quote.volume
                        else None,
                        amount=tencent_quote.amount,
                        turnover_rate=None,  # 腾讯不提供
                        pe_ratio=None,
                        pb_ratio=None,
                        market_cap=None,
                        update_time=datetime.now(),
                    )
            except Exception as tencent_error:
                logger.warning(f"腾讯财经获取行情失败: {str(tencent_error)}")

            # 最后尝试 GM
            if not gm_service.is_available():
                logger.error("GM 服务不可用")
                raise ValueError(
                    f"无法获取股票 {stock_code} 的实时行情，所有数据源均失败"
                )

            try:
                return await self._get_stock_quote_from_gm(stock_code)
            except Exception as gm_error:
                logger.error(f"GM 获取个股实时行情失败: {str(gm_error)}")
                raise ValueError(
                    f"无法获取股票 {stock_code} 的实时行情，所有数据源均失败"
                )

    async def _get_stock_quote_from_gm(self, stock_code: str) -> StockQuote:
        """
        从 GM 服务获取个股实时行情
        """
        logger.info(f"使用 GM 获取个股实时行情: {stock_code}")

        try:
            # 使用 GM 的 current 方法获取当前行情快照
            # 注意：GM 需要使用完整的 symbol 格式，如 SHSE.600000
            gm_symbol = self._convert_to_gm_symbol(stock_code)
            logger.info(f"GM 代码转换: {stock_code} -> {gm_symbol}")

            quotes = gm_service.gm.current(symbols=[gm_symbol])

            if not quotes or len(quotes) == 0:
                logger.warning(f"GM 未找到股票 {stock_code} 的行情数据")
                raise ValueError(f"未找到股票 {stock_code} 的行情数据")

            quote = quotes[0]

            return StockQuote(
                code=stock_code,
                name=quote.get("name", ""),
                price=float(quote.get("last", 0)),
                change=float(quote.get("last", 0) - quote.get("pre_close", 0)),
                change_percent=self._calc_change_percent(
                    float(quote.get("last", 0)), float(quote.get("pre_close", 0))
                ),
                open=float(quote.get("open", 0)),
                high=float(quote.get("high", 0)),
                low=float(quote.get("low", 0)),
                volume=int(quote.get("volume", 0)),
                amount=float(quote.get("amount", 0)),
                turnover_rate=float(quote.get("turnover", 0))
                if quote.get("turnover")
                else 0.0,
                pe_ratio=None,
                pb_ratio=None,
                market_cap=float(quote.get("market_cap", 0))
                if quote.get("market_cap")
                else None,
                update_time=datetime.now(),
            )
        except Exception as e:
            logger.error(f"GM 获取个股实时行情失败: {str(e)}")
            raise

    def _calc_change_percent(self, current: float, pre_close: float) -> float:
        """
        计算涨跌幅

        Args:
            current: 当前价格
            pre_close: 昨收价

        Returns:
            float: 涨跌幅（百分比）
        """
        if pre_close and pre_close != 0:
            return round((current - pre_close) / pre_close * 100, 2)
        return 0.0

    async def get_stock_financial(self, stock_code: str) -> Dict[str, Any]:
        """获取个股财务信息"""
        logger.info(f"获取个股财务信息: {stock_code}")

        try:
            df = ak.stock_financial_analysis_indicator(symbol=stock_code)

            if df.empty:
                return {"stock_code": stock_code, "data": []}

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "report_date": str(row.get("日期", "")),
                        "roe": self._safe_float(row.get("净资产收益率")),
                        "roa": self._safe_float(row.get("总资产净利率")),
                        "gross_margin": self._safe_float(row.get("销售毛利率")),
                        "net_margin": self._safe_float(row.get("销售净利率")),
                        "debt_ratio": self._safe_float(row.get("资产负债率")),
                        "current_ratio": self._safe_float(row.get("流动比率")),
                        "quick_ratio": self._safe_float(row.get("速动比率")),
                        "eps": self._safe_float(row.get("每股收益")),
                        "bvps": self._safe_float(row.get("每股净资产")),
                    }
                )

            return {"stock_code": stock_code, "data": result[:10]}

        except Exception as e:
            logger.warning(f"获取财务信息失败: {e}")
            return {"stock_code": stock_code, "data": [], "error": str(e)}

    async def get_stock_fund_flow(self, stock_code: str) -> Dict[str, Any]:
        """获取个股资金流向"""
        logger.info(f"获取个股资金流向: {stock_code}")

        try:
            market = "sh" if stock_code.startswith("6") else "sz"
            df = ak.stock_individual_fund_flow(stock=stock_code, market=market)

            if df.empty:
                return {"stock_code": stock_code, "data": None}

            row = df.iloc[0]
            return {
                "stock_code": stock_code,
                "stock_name": str(row.get("名称", "")),
                "close_price": self._safe_float(row.get("收盘价")),
                "change_percent": self._safe_float(row.get("涨跌幅")),
                "main_net_inflow": self._safe_float(row.get("主力净流入")),
                "main_net_inflow_ratio": self._safe_float(row.get("主力净占比")),
                "super_net_inflow": self._safe_float(row.get("超大单净流入")),
                "big_net_inflow": self._safe_float(row.get("大单净流入")),
                "medium_net_inflow": self._safe_float(row.get("中单净流入")),
                "small_net_inflow": self._safe_float(row.get("小单净流入")),
            }

        except Exception as e:
            logger.warning(f"获取资金流向失败: {e}")
            return {"stock_code": stock_code, "data": None, "error": str(e)}

    async def get_stock_margin(self, stock_code: str) -> Dict[str, Any]:
        """获取个股融资融券信息"""
        logger.info(f"获取个股融资融券信息: {stock_code}")

        try:
            df = ak.stock_margin_detail_szsh(symbol=stock_code)

            if df.empty:
                return {"stock_code": stock_code, "data": []}

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "trade_date": str(row.get("交易日期", "")),
                        "financing_balance": self._safe_float(row.get("融资余额")),
                        "financing_buy": self._safe_float(row.get("融资买入额")),
                        "financing_repay": self._safe_float(row.get("融资偿还额")),
                        "securities_balance": self._safe_float(row.get("融券余额")),
                        "securities_sell": self._safe_float(row.get("融券卖出量")),
                    }
                )

            return {"stock_code": stock_code, "data": result[:30]}

        except Exception as e:
            logger.warning(f"获取融资融券失败: {e}")
            return {"stock_code": stock_code, "data": [], "error": str(e)}

    def _safe_float(self, value) -> Optional[float]:
        if value is None or pd.isna(value):
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @cache_result()
    async def get_stock_history(
        self,
        stock_code: str,
        period: str = "daily",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[StockHistory]:
        """
        获取个股历史行情数据
        优先使用 AKShare，失败时自动降级到 GM

        Args:
            stock_code: 股票代码，如"000001"
            period: 周期，可选 daily(日线), weekly(周线), monthly(月线)
            start_date: 开始日期，格式YYYYMMDD，如"20210101"
            end_date: 结束日期，格式YYYYMMDD，如"20210630"

        Returns:
            List[StockHistory]: 历史行情数据列表

        Raises:
            ValueError: 当获取数据失败或参数错误时抛出
        """
        logger.info(
            f"获取个股历史行情: {stock_code}, 周期: {period}, 开始日期: {start_date}, 结束日期: {end_date}"
        )

        try:
            # 标准化股票代码（去掉市场前缀）
            if stock_code.startswith(("sh", "sz", "bj")):
                stock_code = stock_code[2:]

            # 设置默认日期范围（如果未提供）
            if not start_date:
                # 默认获取最近30天数据
                start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")

            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")

            # 调用AKShare接口获取历史行情数据，使用前复权(qfq)
            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust="qfq",  # 使用前复权数据
            )

            if df.empty:
                logger.warning(f"未找到股票代码 {stock_code} 的历史行情数据")
                raise ValueError(f"未找到股票代码 {stock_code} 的历史行情数据")

            # 将DataFrame转换为StockHistory对象列表
            result = []
            for _, row in df.iterrows():
                # 确保日期是字符串类型
                if isinstance(row["日期"], (datetime, pd.Timestamp, pd.DatetimeIndex)):
                    trade_date_str = row["日期"].strftime("%Y-%m-%d")
                else:
                    trade_date_str = str(row["日期"])

                history = StockHistory(
                    stock_code=stock_code,
                    trade_date=trade_date_str,  # 使用字符串格式的日期
                    open=float(row["开盘"]),
                    close=float(row["收盘"]),
                    high=float(row["最高"]),
                    low=float(row["最低"]),
                    volume=int(row["成交量"]),
                    amount=float(row["成交额"]),
                    amplitude=float(row["振幅"]),
                    change_percent=float(row["涨跌幅"]),
                    change_amount=float(row["涨跌额"]),
                    turnover=float(row["换手率"]),
                )
                result.append(history)

            return result

        except Exception as e:
            logger.warning(f"AKShare 获取个股历史行情失败: {str(e)}，尝试使用证券宝")

            # 尝试证券宝
            if baostock_source.is_available():
                try:
                    return await self._get_stock_history_from_baostock(
                        stock_code, period, start_date, end_date
                    )
                except Exception as bs_error:
                    logger.warning(f"证券宝获取个股历史行情失败: {str(bs_error)}")

            # 尝试掘金量化
            if gm_service.is_available():
                try:
                    return await self._get_stock_history_from_gm(
                        stock_code, period, start_date, end_date
                    )
                except Exception as gm_error:
                    logger.error(f"GM 获取个股历史行情失败: {str(gm_error)}")

            raise ValueError(f"无法获取股票 {stock_code} 的历史行情，所有数据源均失败")

    async def _get_stock_history_from_baostock(
        self,
        stock_code: str,
        period: str = "daily",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[StockHistory]:
        """从证券宝获取个股历史行情"""
        logger.info(f"使用证券宝获取个股历史行情: {stock_code}, 周期: {period}")

        try:
            period_map = {"daily": "d", "weekly": "w", "monthly": "m"}
            bs_period = period_map.get(period, "d")

            klines = await baostock_source.get_history_kline_async(
                stock_code=stock_code,
                start_date=start_date or "",
                end_date=end_date or "",
                period=bs_period,
                adjust="2",
            )

            if not klines:
                logger.warning(f"证券宝未找到股票 {stock_code} 的历史行情数据")
                raise ValueError(f"未找到股票 {stock_code} 的历史行情数据")

            result = []
            for kline in klines:
                history = StockHistory(
                    stock_code=stock_code,
                    trade_date=kline.trade_date,
                    open=kline.open,
                    close=kline.close,
                    high=kline.high,
                    low=kline.low,
                    volume=int(kline.volume) if kline.volume else 0,
                    amount=kline.amount,
                    amplitude=kline.amplitude,
                    change_percent=kline.change_percent,
                    change_amount=kline.change_amount,
                    turnover=kline.turnover,
                )
                result.append(history)

            return result

        except Exception as e:
            logger.error(f"证券宝获取个股历史行情失败: {str(e)}")
            raise

    async def _get_stock_history_from_gm(
        self,
        stock_code: str,
        period: str = "daily",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[StockHistory]:
        """
        从 GM 服务获取个股历史行情
        """
        logger.info(f"使用 GM 获取个股历史行情: {stock_code}, 周期: {period}")

        try:
            # 映射周期参数
            period_map = {"daily": "1d", "weekly": "1w", "monthly": "1M"}
            gm_period = period_map.get(period, "1d")

            # 转换日期格式
            start_dt = (
                datetime.strptime(start_date, "%Y%m%d")
                if start_date
                else (datetime.now() - timedelta(days=30))
            )
            end_dt = (
                datetime.strptime(end_date, "%Y%m%d") if end_date else datetime.now()
            )

            # 转换为 GM 需要的格式
            gm_symbol = self._convert_to_gm_symbol(stock_code)
            start_time = start_dt.strftime("%Y-%m-%d")
            end_time = end_dt.strftime("%Y-%m-%d")

            # 使用 GM 的 history 方法获取历史行情
            quotes = gm_service.gm.history(
                symbol=gm_symbol,
                frequency=gm_period,
                start_time=start_time,
                end_time=end_time,
                adjust="none",  # 不复权
            )

            if not quotes or len(quotes) == 0:
                logger.warning(f"GM 未找到股票 {stock_code} 的历史行情数据")
                raise ValueError(f"未找到股票 {stock_code} 的历史行情数据")

            # 转换为 StockHistory 对象列表
            result = []
            for quote in quotes:
                # 处理日期格式
                trade_date_str = quote.get("eob", quote.get("timestamp", ""))
                if isinstance(trade_date_str, (datetime, pd.Timestamp)):
                    trade_date_str = trade_date_str.strftime("%Y-%m-%d")
                elif trade_date_str and " " in str(trade_date_str):
                    trade_date_str = str(trade_date_str).split(" ")[0]

                history = StockHistory(
                    stock_code=stock_code,
                    trade_date=trade_date_str,
                    open=float(quote.get("open", 0)),
                    close=float(quote.get("close", 0)),
                    high=float(quote.get("high", 0)),
                    low=float(quote.get("low", 0)),
                    volume=int(quote.get("volume", 0)),
                    amount=float(quote.get("amount", 0)),
                    amplitude=self._calc_amplitude_gm(quote),
                    change_percent=self._calc_change_percent(
                        float(quote.get("close", 0)), float(quote.get("pre_close", 0))
                    ),
                    change_amount=float(
                        quote.get("close", 0) - quote.get("pre_close", 0)
                    ),
                    turnover=float(quote.get("turnover", 0))
                    if quote.get("turnover")
                    else 0.0,
                )
                result.append(history)

            return result

        except Exception as e:
            logger.error(f"GM 获取个股历史行情失败: {str(e)}")
            raise

    def _convert_to_gm_symbol(self, stock_code: str) -> str:
        """
        将股票代码转换为 GM 需要的格式
        GM 格式: 交易所.代码，如 SHSE.600000

        Args:
            stock_code: 股票代码，如 "600000" 或 "SZ000001"

        Returns:
            str: GM 格式的股票代码
        """
        # 去除可能的前缀
        if stock_code.startswith(("sh", "sz", "bj", "SH", "SZ", "BJ")):
            market = stock_code[:2].upper()
            code = stock_code[2:]
        else:
            # 根据代码判断市场
            if stock_code.startswith("6"):
                market = "SH"
            elif stock_code.startswith(("0", "3")):
                market = "SZ"
            elif stock_code.startswith("8"):
                market = "BJ"
            else:
                market = "SH"  # 默认
            code = stock_code

        # 映射市场代码
        market_map = {"SH": "SHSE", "SZ": "SZSE", "BJ": "BJSE"}

        gm_market = market_map.get(market, "SHSE")
        return f"{gm_market}.{code}"

    def _calc_amplitude_gm(self, quote: Dict[str, Any]) -> float:
        """
        计算 GM 数据的振幅

        Args:
            quote: GM 返回的行情数据字典

        Returns:
            float: 振幅（百分比）
        """
        high = float(quote.get("high", 0))
        low = float(quote.get("low", 0))
        pre_close = float(quote.get("pre_close", 0))

        if pre_close and pre_close != 0:
            return round((high - low) / pre_close * 100, 2)
        return 0.0

    def _calc_amplitude(self, quote: Dict[str, Any]) -> float:
        """
        计算振幅

        Args:
            quote: 行情数据字典

        Returns:
            float: 振幅（百分比）
        """
        high = quote.get("high", 0)
        low = quote.get("low", 0)
        pre_close = quote.get("pre_close", 0)

        if pre_close and pre_close != 0:
            return round((high - low) / pre_close * 100, 2)
        return 0.0

    @cache_result(expire=300)
    async def get_all_stock_list(self) -> List[Dict[str, Any]]:
        """
        获取所有A股股票列表
        使用 AKShare 的 stock_zh_a_spot_em 接口

        Returns:
            List[Dict[str, Any]]: 股票列表，包含代码、名称、最新价等信息

        Raises:
            ValueError: 当获取数据失败时抛出
        """
        logger.info("开始获取所有A股股票列表")

        try:
            # 调用AKShare接口获取A股实时行情
            logger.info("正在调用 ak.stock_zh_a_spot_em()...")
            df = ak.stock_zh_a_spot_em()
            logger.info(f"ak.stock_zh_a_spot_em() 返回，数据行数: {len(df)}")

            if df.empty:
                logger.warning("未获取到A股股票列表数据")
                raise ValueError("未获取到A股股票列表数据")

            # 字段映射
            column_mapping = {
                "代码": "stock_code",
                "名称": "stock_name",
                "最新价": "current_price",
                "涨跌幅": "change_percent",
                "涨跌额": "change_amount",
                "成交量": "volume",
                "成交额": "amount",
                "振幅": "amplitude",
                "最高": "high_price",
                "最低": "low_price",
                "今开": "open_price",
                "昨收": "previous_close",
                "量比": "volume_ratio",
                "换手率": "turnover_rate",
                "市盈率-动态": "pe_ratio",
                "市净率": "pb_ratio",
                "总市值": "total_market_cap",
                "流通市值": "circulating_market_cap",
                "涨速": "change_speed",
                "5分钟涨跌": "change_5min",
                "60日涨跌幅": "change_60day",
                "年初至今涨跌幅": "change_ytd",
            }

            # 重命名列
            df = df.rename(columns=column_mapping)

            # 将DataFrame转换为列表
            result = []
            for _, row in df.iterrows():
                try:
                    stock_code = str(row["stock_code"])

                    if not stock_code:
                        continue

                    stock = {
                        "code": stock_code,
                        "name": str(row["stock_name"])
                        if pd.notna(row["stock_name"])
                        else "",
                        "price": float(row["current_price"])
                        if pd.notna(row["current_price"])
                        else None,
                        "change_amount": float(row["change_amount"])
                        if pd.notna(row["change_amount"])
                        else None,
                        "change_percent": float(row["change_percent"])
                        if pd.notna(row["change_percent"])
                        else None,
                        "open": float(row["open_price"])
                        if pd.notna(row["open_price"])
                        else None,
                        "high": float(row["high_price"])
                        if pd.notna(row["high_price"])
                        else None,
                        "low": float(row["low_price"])
                        if pd.notna(row["low_price"])
                        else None,
                        "volume": float(row["volume"])
                        if pd.notna(row["volume"])
                        else None,
                        "amount": float(row["amount"])
                        if pd.notna(row["amount"])
                        else None,
                        "turnover_rate": float(row["turnover_rate"])
                        if pd.notna(row["turnover_rate"])
                        else None,
                        "volume_ratio": float(row["volume_ratio"])
                        if pd.notna(row["volume_ratio"])
                        else None,
                        "amplitude": float(row["amplitude"])
                        if pd.notna(row["amplitude"])
                        else None,
                        "pe_ratio": float(row["pe_ratio"])
                        if pd.notna(row["pe_ratio"])
                        else None,
                        "pb_ratio": float(row["pb_ratio"])
                        if pd.notna(row["pb_ratio"])
                        else None,
                        "market_cap": float(row["total_market_cap"])
                        if pd.notna(row["total_market_cap"])
                        else None,
                        "circulating_market_cap": float(row["circulating_market_cap"])
                        if pd.notna(row["circulating_market_cap"])
                        else None,
                        "change_speed": float(row["change_speed"])
                        if pd.notna(row["change_speed"])
                        else None,
                        "change_5min": float(row["change_5min"])
                        if pd.notna(row["change_5min"])
                        else None,
                        "change_60day": float(row["change_60day"])
                        if pd.notna(row["change_60day"])
                        else None,
                        "change_ytd": float(row["change_ytd"])
                        if pd.notna(row["change_ytd"])
                        else None,
                        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    result.append(stock)
                except Exception as e:
                    logger.warning(f"处理股票数据失败: {str(e)}")
                    continue

            logger.info(f"成功获取 {len(result)} 只A股股票列表")
            return result

        except Exception as e:
            logger.error(f"获取A股股票列表失败: {str(e)}")
            raise ValueError(f"获取A股股票列表失败: {str(e)}")

    # ========== 扩展接口 ==========

    @cache_result(expire=60)
    async def get_minute_data(
        self, stock_code: str, period: str = "1", adjust: str = ""
    ) -> List[Dict[str, Any]]:
        """获取分时数据 (1/5/15/30/60分钟)"""
        logger.info(f"获取分时数据: {stock_code}, 周期: {period}分钟")

        try:
            period_map = {"1": "1", "5": "5", "15": "15", "30": "30", "60": "60"}
            ak_period = period_map.get(str(period), "1")

            df = ak.stock_zh_a_hist_min_em(
                symbol=stock_code, period=ak_period, adjust=adjust
            )

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "time": str(row.get("时间", "")),
                        "open": self._safe_float(row.get("开盘")),
                        "close": self._safe_float(row.get("收盘")),
                        "high": self._safe_float(row.get("最高")),
                        "low": self._safe_float(row.get("最低")),
                        "volume": self._safe_float(row.get("成交量")),
                        "amount": self._safe_float(row.get("成交额")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取分时数据失败: {e}")
            return []

    @cache_result(expire=30)
    async def get_quote_detail(self, stock_code: str) -> Dict[str, Any]:
        """获取五档买卖盘详情"""
        logger.info(f"获取五档买卖盘: {stock_code}")

        try:
            df = ak.stock_zh_a_spot_em()
            row = df[df["代码"] == stock_code]

            if row.empty:
                return {"stock_code": stock_code, "data": None}

            r = row.iloc[0]
            return {
                "stock_code": stock_code,
                "stock_name": str(r.get("名称", "")),
                "price": self._safe_float(r.get("最新价")),
                "open": self._safe_float(r.get("今开")),
                "high": self._safe_float(r.get("最高")),
                "low": self._safe_float(r.get("最低")),
                "pre_close": self._safe_float(r.get("昨收")),
                "volume": self._safe_float(r.get("成交量")),
                "amount": self._safe_float(r.get("成交额")),
                "bid1": self._safe_float(r.get("买一")),
                "bid1_vol": self._safe_float(r.get("买一量")),
                "bid2": self._safe_float(r.get("买二")),
                "bid2_vol": self._safe_float(r.get("买二量")),
                "bid3": self._safe_float(r.get("买三")),
                "bid3_vol": self._safe_float(r.get("买三量")),
                "bid4": self._safe_float(r.get("买四")),
                "bid4_vol": self._safe_float(r.get("买四量")),
                "bid5": self._safe_float(r.get("买五")),
                "bid5_vol": self._safe_float(r.get("买五量")),
                "ask1": self._safe_float(r.get("卖一")),
                "ask1_vol": self._safe_float(r.get("卖一量")),
                "ask2": self._safe_float(r.get("卖二")),
                "ask2_vol": self._safe_float(r.get("卖二量")),
                "ask3": self._safe_float(r.get("卖三")),
                "ask3_vol": self._safe_float(r.get("卖三量")),
                "ask4": self._safe_float(r.get("卖四")),
                "ask4_vol": self._safe_float(r.get("卖四量")),
                "ask5": self._safe_float(r.get("卖五")),
                "ask5_vol": self._safe_float(r.get("卖五量")),
            }

        except Exception as e:
            logger.warning(f"获取五档买卖盘失败: {e}")
            return {"stock_code": stock_code, "data": None, "error": str(e)}

    @cache_result(expire=3600)
    async def get_stock_sectors(self, stock_code: str) -> Dict[str, Any]:
        """获取股票所属板块"""
        logger.info(f"获取股票所属板块: {stock_code}")

        try:
            df = ak.stock_individual_info_em(symbol=stock_code)

            if df.empty:
                return {"stock_code": stock_code, "sectors": []}

            info = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

            sectors = []
            if info.get("行业"):
                sectors.append({"type": "industry", "name": info.get("行业")})
            if info.get("概念"):
                concepts = info.get("概念", "").split(";")
                for c in concepts[:10]:
                    if c.strip():
                        sectors.append({"type": "concept", "name": c.strip()})

            return {"stock_code": stock_code, "sectors": sectors}

        except Exception as e:
            logger.warning(f"获取股票板块失败: {e}")
            return {"stock_code": stock_code, "sectors": [], "error": str(e)}

    @cache_result(expire=300)
    async def get_suspend_info(self, stock_code: str) -> Dict[str, Any]:
        """获取停复牌信息"""
        logger.info(f"获取停复牌信息: {stock_code}")

        try:
            df = ak.stock_tfp_em()

            if df.empty:
                return {"stock_code": stock_code, "status": "正常", "data": None}

            row = df[df["代码"] == stock_code]

            if row.empty:
                return {"stock_code": stock_code, "status": "正常", "data": None}

            r = row.iloc[0]
            return {
                "stock_code": stock_code,
                "status": str(r.get("停牌状态", "停牌")),
                "suspend_date": str(r.get("停牌日期", "")),
                "resume_date": str(r.get("预计复牌日期", "")),
                "reason": str(r.get("停牌原因", "")),
            }

        except Exception as e:
            logger.warning(f"获取停复牌信息失败: {e}")
            return {"stock_code": stock_code, "status": "未知", "error": str(e)}

    @cache_result(expire=3600)
    async def get_stock_notices(
        self, stock_code: str, page: int = 1
    ) -> List[Dict[str, Any]]:
        """获取股票公告"""
        logger.info(f"获取股票公告: {stock_code}")

        try:
            df = ak.stock_notice_report(symbol=stock_code)

            if df.empty:
                return []

            result = []
            for _, row in df.head(20).iterrows():
                result.append(
                    {
                        "title": str(row.get("公告标题", "")),
                        "date": str(row.get("公告日期", "")),
                        "type": str(row.get("公告类型", "")),
                        "url": str(row.get("公告链接", "")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取股票公告失败: {e}")
            return []

    @cache_result(expire=3600)
    async def get_share_pledge(self, stock_code: str) -> Dict[str, Any]:
        """获取股权质押数据"""
        logger.info(f"获取股权质押: {stock_code}")

        try:
            df = ak.stock_gpZY_profile_em(symbol=stock_code)

            if df.empty:
                return {"stock_code": stock_code, "data": []}

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "shareholder": str(row.get("股东名称", "")),
                        "pledged_shares": self._safe_float(row.get("质押股份数量")),
                        "pledged_ratio": self._safe_float(row.get("质押股份占比")),
                        "total_shares": self._safe_float(row.get("持股数量")),
                        "update_date": str(row.get("公告日期", "")),
                    }
                )

            return {"stock_code": stock_code, "data": result}

        except Exception as e:
            logger.warning(f"获取股权质押失败: {e}")
            return {"stock_code": stock_code, "data": [], "error": str(e)}

    @cache_result(expire=86400)
    async def get_unlock_schedule(self, stock_code: str) -> List[Dict[str, Any]]:
        """获取限售解禁计划"""
        logger.info(f"获取限售解禁: {stock_code}")

        try:
            df = ak.stock_restricted_release_summary_em(symbol=stock_code)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "unlock_date": str(row.get("解禁日期", "")),
                        "unlock_shares": self._safe_float(row.get("解禁股数")),
                        "unlock_ratio": self._safe_float(row.get("解禁股占总股本比例")),
                        "unlock_amount": self._safe_float(row.get("解禁市值")),
                        "unlock_type": str(row.get("解禁类型", "")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取限售解禁失败: {e}")
            return []

    @cache_result(expire=86400)
    async def get_adjust_factor(self, stock_code: str) -> List[Dict[str, Any]]:
        """获取复权因子"""
        logger.info(f"获取复权因子: {stock_code}")

        try:
            df = ak.stock_qsjy_em(symbol=stock_code)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "date": str(row.get("日期", "")),
                        "factor": self._safe_float(row.get("复权因子")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取复权因子失败: {e}")
            return []

    @cache_result(expire=60)
    async def search_stock(self, keyword: str, limit: int = 20) -> List[Dict[str, Any]]:
        """搜索股票"""
        logger.info(f"搜索股票: {keyword}")

        try:
            df = ak.stock_zh_a_spot_em()

            if df.empty:
                return []

            df = df[
                df["名称"].str.contains(keyword, na=False)
                | df["代码"].str.contains(keyword, na=False)
            ]

            result = []
            for _, row in df.head(limit).iterrows():
                result.append(
                    {
                        "code": str(row.get("代码", "")),
                        "name": str(row.get("名称", "")),
                        "price": self._safe_float(row.get("最新价")),
                        "change_percent": self._safe_float(row.get("涨跌幅")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"搜索股票失败: {e}")
            return []

    @cache_result(expire=3600)
    async def get_stock_rating(self, stock_code: str) -> Dict[str, Any]:
        """获取股票评级"""
        logger.info(f"获取股票评级: {stock_code}")

        try:
            df = ak.stock_rank_forecast_cninfo(symbol=stock_code)

            if df.empty:
                return {"stock_code": stock_code, "data": []}

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "org_name": str(row.get("机构名称", "")),
                        "rating": str(row.get("评级", "")),
                        "rating_change": str(row.get("评级变动", "")),
                        "target_price": self._safe_float(row.get("目标价")),
                        "report_date": str(row.get("报告日期", "")),
                    }
                )

            return {"stock_code": stock_code, "data": result[:10]}

        except Exception as e:
            logger.warning(f"获取股票评级失败: {e}")
            return {"stock_code": stock_code, "data": [], "error": str(e)}

    @cache_result(expire=86400)
    async def get_stock_report(self, stock_code: str) -> List[Dict[str, Any]]:
        """获取研报"""
        logger.info(f"获取研报: {stock_code}")

        try:
            df = ak.stock_research_report_em(symbol=stock_code)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "title": str(row.get("报告名称", "")),
                        "org_name": str(row.get("机构名称", "")),
                        "author": str(row.get("作者", "")),
                        "date": str(row.get("报告日期", "")),
                        "rating": str(row.get("评级", "")),
                    }
                )

            return result[:20]

        except Exception as e:
            logger.warning(f"获取研报失败: {e}")
            return []

    @cache_result(expire=300)
    async def get_realtime_quote(self, stock_code: str) -> Dict[str, Any]:
        """获取实时行情（新浪接口，更快响应）"""
        logger.info(f"获取实时行情: {stock_code}")

        try:
            market = "sh" if stock_code.startswith("6") else "sz"
            df = ak.stock_zh_a_spot()

            if df.empty:
                return {"stock_code": stock_code, "data": None}

            row = df[df["代码"] == stock_code]

            if row.empty:
                return {"stock_code": stock_code, "data": None}

            r = row.iloc[0]
            return {
                "stock_code": stock_code,
                "stock_name": str(r.get("名称", "")),
                "price": self._safe_float(r.get("现价")),
                "open": self._safe_float(r.get("今开")),
                "high": self._safe_float(r.get("最高")),
                "low": self._safe_float(r.get("最低")),
                "volume": self._safe_float(r.get("成交量")),
                "amount": self._safe_float(r.get("成交额")),
                "time": str(r.get("时间", "")),
            }

        except Exception as e:
            logger.warning(f"获取实时行情失败: {e}")
            return {"stock_code": stock_code, "data": None, "error": str(e)}


stock_service = StockService()
