"""GM（掘金量化）数据服务模块

本模块提供与掘金量化平台的对接服务，作为 akshare 的备用数据源。
主要功能：
1. 提供与 akshare 兼容的接口
2. 统一的数据返回格式
3. 自动降级机制：当 akshare 失败时自动使用 GM 获取数据
"""

import logging
import pandas as pd
import math
from datetime import datetime
from typing import List, Optional, Dict, Any

from app.models.sector_models import (
    ConceptBoard, IndustryBoard, BoardSpot,
    ConceptBoardSpot, IndustryBoardSpot,
    ConceptBoardConstituent, IndustryBoardConstituent
)
from app.models.stock_models import StockInfo, StockQuote
from app.core.logging import get_logger

logger = get_logger(__name__)


class GMService:
    """掘金量化数据服务"""

    def __init__(self, token: Optional[str] = None):
        """
        初始化 GM 服务

        Args:
            token: GM API token（预留，当前 GM SDK 不需要 token）
        """
        self.enabled = False  # GM 服务是否启用
        self.token = token
        self._init_gm()

    def _init_gm(self):
        """初始化掘金量化连接"""
        try:
            from gm import api as gm_api
            self.gm = gm_api

            # 使用 token 进行认证
            if self.token:
                try:
                    self.gm.set_token(self.token)
                    logger.info(f"GM Token 已设置: {self.token[:10]}...")
                except Exception as token_error:
                    logger.warning(f"GM Token 设置失败: {token_error}")

            self.enabled = True
            logger.info("掘金量化 SDK 初始化成功")
        except ImportError:
            logger.warning("掘金量化 SDK 未安装，GM 服务将不可用")
            self.enabled = False
        except Exception as e:
            logger.error(f"掘金量化 SDK 初始化失败: {str(e)}")
            self.enabled = False
        print(self.enabled, "gm 服务是否启用")

    def is_available(self) -> bool:
        """检查 GM 服务是否可用"""
        return self.enabled

    # 辅助方法

    async def get_stock_info(self, symbol: str) -> StockInfo:
        """
        获取股票基本信息
        注意：GM 没有直接的股票基本信息接口，需要通过 get_instruments 获取
        """
        if not self.is_available():
            logger.warning("GM 服务不可用，无法获取股票基本信息")
            raise ValueError("GM 服务不可用")

        logger.info(f"使用 GM 获取股票基本信息: {symbol}")

        try:
            # 使用 GM 的 get_instruments 获取标的列表
            instruments = self.gm.get_instruments(symbols=symbol)

            if not instruments or len(instruments) == 0:
                logger.warning(f"GM 未找到股票 {symbol} 的基本信息")
                raise ValueError(f"未找到股票 {symbol} 的基本信息")

            inst = instruments[0]

            # 转换为 StockInfo 格式
            return StockInfo(
                code=inst.get("symbol", ""),
                name=inst.get("name", ""),
                industry=inst.get("sec_name", ""),  # GM 可能没有行业信息
                listing_date=inst.get("list_date", ""),
                total_market_value=None,  # 需要通过其他方式获取
                circulating_market_value=None,
                total_share=None,
                circulating_share=None
            )
        except Exception as e:
            logger.error(f"GM 获取股票基本信息失败: {str(e)}")
            raise

    async def get_stock_quote(self, symbol: str) -> StockQuote:
        """
        获取股票实时行情
        """
        if not self.is_available():
            logger.warning("GM 服务不可用，无法获取股票实时行情")
            raise ValueError("GM 服务不可用")

        logger.info(f"使用 GM 获取股票实时行情: {symbol}")

        try:
            # 使用 GM 的 current 方法获取当前行情快照
            quotes = self.gm.current(symbols=[symbol])

            if not quotes or len(quotes) == 0:
                logger.warning(f"GM 未找到股票 {symbol} 的行情数据")
                raise ValueError(f"未找到股票 {symbol} 的行情数据")

            quote = quotes[0]

            # 转换为 StockQuote 格式
            return StockQuote(
                code=symbol,
                name=quote.get("name", ""),
                price=float(quote.get("last", 0)),
                change=float(quote.get("last", 0) - quote.get("pre_close", 0)),
                change_percent=self._calc_change_percent(
                    float(quote.get("last", 0)),
                    float(quote.get("pre_close", 0))
                ),
                open=float(quote.get("open", 0)),
                high=float(quote.get("high", 0)),
                low=float(quote.get("low", 0)),
                volume=int(quote.get("volume", 0)),
                amount=float(quote.get("amount", 0)),
                turnover_rate=float(quote.get("turnover", 0)) if quote.get("turnover") else None,
                pe_ratio=None,
                pb_ratio=None,
                market_cap=float(quote.get("market_cap", 0)) if quote.get("market_cap") else None,
                update_time=datetime.now()
            )
        except Exception as e:
            logger.error(f"GM 获取股票实时行情失败: {str(e)}")
            raise

    async def get_stock_history(
        self,
        symbol: str,
        frequency: str = "1d",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取股票历史行情
        """
        if not self.is_available():
            logger.warning("GM 服务不可用，无法获取股票历史行情")
            raise ValueError("GM 服务不可用")

        logger.info(f"使用 GM 获取股票历史行情: {symbol}, 频率: {frequency}")

        try:
            # 使用 GM 的 history 方法获取历史行情
            history_data = self.gm.history(
                symbol=symbol,
                frequency=frequency,
                start_time=start_time,
                end_time=end_time,
                adjust="none"  # 默认不复权
            )

            if not history_data:
                logger.warning(f"GM 未找到股票 {symbol} 的历史行情数据")
                raise ValueError(f"未找到股票 {symbol} 的历史行情数据")

            return history_data
        except Exception as e:
            logger.error(f"GM 获取股票历史行情失败: {str(e)}")
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

    # 概念板块相关接口

    async def get_concept_boards(self) -> List[ConceptBoard]:
        """
        获取概念板块列表（GM 版本）

        注意：GM SDK 不支持获取板块列表功能，此方法仅作为接口兼容性保留
        实际使用时应该使用 AKShare

        Returns:
            List[ConceptBoard]: 概念板块列表

        Raises:
            ValueError: GM SDK 不支持此功能
        """
        logger.warning("GM SDK 不支持获取概念板块列表功能，请使用 AKShare")
        raise ValueError("GM SDK 不支持获取概念板块列表功能")

    async def get_concept_board_constituents(self, symbol: str) -> List[ConceptBoardConstituent]:
        """
        获取概念板块成份股（GM 版本）

        Args:
            symbol: 板块名称或代码

        Returns:
            List[ConceptBoardConstituent]: 概念板块成份股列表
        """
        if not self.is_available():
            logger.warning("GM 服务不可用，无法获取概念板块成份股")
            raise ValueError("GM 服务不可用")

        logger.info(f"使用 GM 获取概念板块成份股: {symbol}")

        try:
            # 获取板块内的股票列表
            stocks = self.gm.get_constituents(sector=symbol)

            result = []
            for i, stock in enumerate(stocks, 1):
                # 获取个股实时行情
                quotes = self.gm.history(
                    symbol=stock["symbol"],
                    frequency='tick',
                    count=1
                )

                if quotes:
                    quote = quotes[0]
                    constituent = ConceptBoardConstituent(
                        rank=i,
                        code=stock["symbol"],
                        name=stock["sec_name"],
                        price=quote.get("close", 0),
                        change_percent=self._calc_change_percent(
                            quote.get("close", 0),
                            quote.get("pre_close", 0)
                        ),
                        change=quote.get("close", 0) - quote.get("pre_close", 0),
                        volume=quote.get("volume", 0),
                        amount=quote.get("amount", 0),
                        amplitude=self._calc_amplitude(quote),
                        high=quote.get("high", 0),
                        low=quote.get("low", 0),
                        open=quote.get("open", 0),
                        pre_close=quote.get("pre_close", 0),
                        turnover_rate=quote.get("turnover_rate", 0),
                        pe_ratio=quote.get("pe_ratio"),
                        pb_ratio=quote.get("pb_ratio"),
                        update_time=datetime.now()
                    )
                    result.append(constituent)

            logger.info(f"GM 获取到 {len(result)} 个成份股")
            return result

        except Exception as e:
            logger.error(f"GM 获取概念板块成份股失败: {str(e)}")
            raise ValueError(f"GM 获取概念板块成份股失败: {str(e)}")

    # 行业板块相关接口

    async def get_industry_boards(self) -> List[IndustryBoard]:
        """
        获取行业板块列表（GM 版本）

        注意：GM SDK 不支持获取板块列表功能，此方法仅作为接口兼容性保留
        实际使用时应该使用 AKShare

        Returns:
            List[IndustryBoard]: 行业板块列表

        Raises:
            ValueError: GM SDK 不支持此功能
        """
        logger.warning("GM SDK 不支持获取行业板块列表功能，请使用 AKShare")
        raise ValueError("GM SDK 不支持获取行业板块列表功能")

    async def get_industry_board_constituents(self, symbol: str) -> List[IndustryBoardConstituent]:
        """
        获取行业板块成份股（GM 版本）

        Args:
            symbol: 板块名称或代码

        Returns:
            List[IndustryBoardConstituent]: 行业板块成份股列表
        """
        if not self.is_available():
            logger.warning("GM 服务不可用，无法获取行业板块成份股")
            raise ValueError("GM 服务不可用")

        logger.info(f"使用 GM 获取行业板块成份股: {symbol}")

        try:
            stocks = self.gm.get_constituents(sector=symbol)

            result = []
            for i, stock in enumerate(stocks, 1):
                quotes = self.gm.history(
                    symbol=stock["symbol"],
                    frequency='tick',
                    count=1
                )

                if quotes:
                    quote = quotes[0]
                    constituent = IndustryBoardConstituent(
                        rank=i,
                        code=stock["symbol"],
                        name=stock["sec_name"],
                        price=quote.get("close", 0),
                        change_percent=self._calc_change_percent(
                            quote.get("close", 0),
                            quote.get("pre_close", 0)
                        ),
                        change=quote.get("close", 0) - quote.get("pre_close", 0),
                        volume=quote.get("volume", 0),
                        amount=quote.get("amount", 0),
                        amplitude=self._calc_amplitude(quote),
                        high=quote.get("high", 0),
                        low=quote.get("low", 0),
                        open=quote.get("open", 0),
                        pre_close=quote.get("pre_close", 0),
                        turnover_rate=quote.get("turnover_rate", 0),
                        pe_ratio=quote.get("pe_ratio"),
                        pb_ratio=quote.get("pb_ratio"),
                        update_time=datetime.now()
                    )
                    result.append(constituent)

            logger.info(f"GM 获取到 {len(result)} 个成份股")
            return result

        except Exception as e:
            logger.error(f"GM 获取行业板块成份股失败: {str(e)}")
            raise ValueError(f"GM 获取行业板块成份股失败: {str(e)}")

    # 辅助方法

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


# 创建全局 GM 服务实例
from app.core.config import settings
gm_service = GMService(token=settings.GM_TOKEN)
