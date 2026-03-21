# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : tencent_source.py
# @IDE            : PyCharm
# @desc           : 腾讯财经数据源 - 高成功率实时行情接口

import asyncio
import json
import re
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
import aiohttp

from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)


@dataclass
class TencentQuote:
    stock_code: str
    stock_name: str
    price: Optional[float]
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    pre_close: Optional[float]
    volume: Optional[float]
    amount: Optional[float]
    bid1: Optional[float]
    bid1_vol: Optional[float]
    ask1: Optional[float]
    ask1_vol: Optional[float]
    change: Optional[float]
    change_percent: Optional[float]
    time: Optional[str]
    source: str = "tencent"


class TencentFinanceSource:
    """腾讯财经数据源 - 成功率高，响应快"""

    BASE_URL = "https://qt.gtimg.cn/q="

    # 市场代码映射
    MARKET_MAP = {
        "sh": "sh",  # 上海
        "sz": "sz",  # 深圳
        "bj": "bj",  # 北京
    }

    def _get_tencent_code(self, stock_code: str) -> str:
        """转换为腾讯股票代码格式"""
        code = stock_code.lower()

        if code.startswith(("sh", "sz", "bj")):
            return code

        if code.startswith("6"):
            return f"sh{code}"
        elif code.startswith(("0", "3")):
            return f"sz{code}"
        elif code.startswith("8"):
            return f"bj{code}"
        else:
            return f"sz{code}"

    def _parse_quote_data(self, data: str, stock_code: str) -> Optional[TencentQuote]:
        """解析腾讯行情数据"""
        try:
            # 腾讯返回格式: v_sh000001="1~上证指数~000001~3267.93~..."
            if not data or "~" not in data:
                return None

            # 提取引号内的数据
            match = re.search(r'"([^"]+)"', data)
            if not match:
                return None

            parts = match.group(1).split("~")

            if len(parts) < 35:
                return None

            price = float(parts[3]) if parts[3] else None
            pre_close = float(parts[4]) if parts[4] else None

            change = None
            change_percent = None
            if price and pre_close and pre_close != 0:
                change = price - pre_close
                change_percent = (change / pre_close) * 100

            return TencentQuote(
                stock_code=stock_code,
                stock_name=parts[1],
                price=price,
                open=float(parts[5]) if parts[5] else None,
                high=float(parts[33]) if len(parts) > 33 and parts[33] else None,
                low=float(parts[34]) if len(parts) > 34 and parts[34] else None,
                pre_close=pre_close,
                volume=float(parts[6]) if parts[6] else None,
                amount=float(parts[37]) if len(parts) > 37 and parts[37] else None,
                bid1=float(parts[9]) if parts[9] else None,
                bid1_vol=float(parts[10]) if parts[10] else None,
                ask1=float(parts[19]) if len(parts) > 19 and parts[19] else None,
                ask1_vol=float(parts[20]) if len(parts) > 20 and parts[20] else None,
                change=change,
                change_percent=change_percent,
                time=parts[30] if len(parts) > 30 else None,
            )
        except Exception as e:
            logger.warning(f"解析腾讯行情数据失败: {e}")
            return None

    @cache_result(expire=30)
    async def get_quote(self, stock_code: str) -> Optional[TencentQuote]:
        """获取单只股票实时行情"""
        tencent_code = self._get_tencent_code(stock_code)
        url = f"{self.BASE_URL}{tencent_code}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status != 200:
                        return None

                    text = await resp.text(encoding="gbk")
                    return self._parse_quote_data(text, stock_code)

        except asyncio.TimeoutError:
            logger.warning(f"腾讯财经获取行情超时: {stock_code}")
            return None
        except Exception as e:
            logger.warning(f"腾讯财经获取行情失败: {e}")
            return None

    @cache_result(expire=30)
    async def get_quotes_batch(self, stock_codes: List[str]) -> List[TencentQuote]:
        """批量获取股票行情"""
        if not stock_codes:
            return []

        tencent_codes = [self._get_tencent_code(code) for code in stock_codes]
        url = f"{self.BASE_URL}{','.join(tencent_codes)}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status != 200:
                        return []

                    text = await resp.text(encoding="gbk")

                    results = []
                    lines = text.strip().split("\n")

                    for i, line in enumerate(lines):
                        if i < len(stock_codes):
                            quote = self._parse_quote_data(line, stock_codes[i])
                            if quote:
                                results.append(quote)

                    return results

        except Exception as e:
            logger.warning(f"腾讯财经批量获取行情失败: {e}")
            return []

    async def get_index_quote(self, index_code: str) -> Optional[TencentQuote]:
        """获取指数行情"""
        index_map = {
            "000001": "sh000001",  # 上证指数
            "399001": "sz399001",  # 深证成指
            "399006": "sz399006",  # 创业板指
            "000688": "sh000688",  # 科创50
            "000016": "sh000016",  # 上证50
            "000300": "sh000300",  # 沪深300
            "000905": "sh000905",  # 中证500
            "000852": "sh000852",  # 中证1000
        }

        tencent_code = index_map.get(index_code, self._get_tencent_code(index_code))
        url = f"{self.BASE_URL}{tencent_code}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status != 200:
                        return None

                    text = await resp.text(encoding="gbk")
                    return self._parse_quote_data(text, index_code)

        except Exception as e:
            logger.warning(f"腾讯财经获取指数行情失败: {e}")
            return None

    async def get_all_quotes(self) -> List[TencentQuote]:
        """获取全市场行情（分批获取）"""
        # 获取沪深A股列表
        all_codes = []

        # 沪市主板 600xxx-605xxx
        for i in range(600000, 605000):
            all_codes.append(f"sh{i}")

        # 深市主板 000xxx-002xxx
        for i in range(1, 3000):
            all_codes.append(f"sz{str(i).zfill(6)}")

        # 创业板 300xxx-301xxx
        for i in range(300000, 302000):
            all_codes.append(f"sz{i}")

        # 分批获取，每批500只
        batch_size = 500
        all_quotes = []

        for i in range(0, min(len(all_codes), 5000), batch_size):  # 限制最多5000只
            batch = all_codes[i : i + batch_size]
            quotes = await self.get_quotes_batch(batch)
            all_quotes.extend(quotes)
            await asyncio.sleep(0.1)  # 避免请求过快

        return all_quotes

    async def check_available(self) -> bool:
        """检查腾讯财经接口是否可用"""
        try:
            quote = await self.get_quote("000001")
            return quote is not None
        except:
            return False


tencent_source = TencentFinanceSource()
