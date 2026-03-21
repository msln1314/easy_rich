# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/19
# @File           : sina_source.py
# @IDE            : PyCharm
# @desc           : 新浪财经数据源 - 全市场行情接口

import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from app.core.logging import get_logger

logger = get_logger(__name__)


class SinaFinanceSource:
    BASE_URL = "http://hq.sinajs.cn/list="

    # 市场代码范围
    MARKET_CODES = {
        "sh": list(range(600000, 605000)),  # 沪市主板
        "sz_main": list(range(1, 3000)),  # 深市主板
        "sz_gem": list(range(300000, 302000)),  # 创业板
    }

    async def get_all_quotes(self, limit: int = 5000) -> List[Dict[str, Any]]:
        """获取全市场行情数据"""
        all_quotes = []

        async with aiohttp.ClientSession() as session:
            # 构建股票代码列表
            codes = []
            for code in range(600000, 605000):
                codes.append(f"sh{code}")
            for code in range(1, 3000):
                codes.append(f"sz{str(code).zfill(6)}")
            for code in range(300000, 302000):
                codes.append(f"sz{code}")

            # 分批获取，每批500只
            batch_size = 500
            for i in range(0, min(len(codes), limit), batch_size):
                batch = codes[i : i + batch_size]
                try:
                    quotes = await self._fetch_batch(session, batch)
                    all_quotes.extend(quotes)
                    await asyncio.sleep(0.1)
                except Exception as e:
                    logger.warning(f"新浪批量获取失败: {e}")
                    continue

        logger.info(f"新浪财经获取到 {len(all_quotes)} 条股票数据")
        return all_quotes

    async def _fetch_batch(
        self, session: aiohttp.ClientSession, codes: List[str]
    ) -> List[Dict[str, Any]]:
        """批量获取股票行情"""
        url = f"{self.BASE_URL}{','.join(codes)}"
        headers = {"Referer": "http://finance.sina.com.cn"}

        async with session.get(
            url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)
        ) as resp:
            if resp.status != 200:
                return []

            text = await resp.text(encoding="gbk")
            return self._parse_quotes(text)

    def _parse_quotes(self, text: str) -> List[Dict[str, Any]]:
        """解析新浪行情数据"""
        quotes = []

        for line in text.strip().split("\n"):
            if not line or "hq_str_" not in line:
                continue

            try:
                parts = line.split('="')
                if len(parts) != 2:
                    continue

                code = parts[0].replace("var hq_str_", "").upper()
                data = parts[1].rstrip('";').split(",")

                if len(data) < 10:
                    continue

                name = data[0]
                if not name or "ST" in name or "退" in name:
                    continue

                open_price = float(data[1]) if data[1] else None
                pre_close = float(data[2]) if data[2] else None
                price = float(data[3]) if data[3] else None
                high = float(data[4]) if data[4] else None
                low = float(data[5]) if data[5] else None
                volume = float(data[8]) if data[8] else None
                amount = float(data[9]) if data[9] else None

                if not price or price == 0:
                    continue

                change = round(price - pre_close, 2) if price and pre_close else None
                change_percent = (
                    round((price - pre_close) / pre_close * 100, 2)
                    if price and pre_close and pre_close != 0
                    else None
                )

                # 转换代码格式: SH600000 -> 600000
                std_code = code[2:] if code.startswith(("SH", "SZ")) else code

                quotes.append(
                    {
                        "代码": std_code,
                        "名称": name,
                        "最新价": price,
                        "涨跌幅": change_percent,
                        "涨跌额": change,
                        "成交量": volume,
                        "成交额": amount,
                        "今开": open_price,
                        "最高": high,
                        "最低": low,
                        "昨收": pre_close,
                        "换手率": None,  # 新浪不直接提供
                    }
                )
            except Exception as e:
                continue

        return quotes


async def get_down_ranking(self, limit: int = 50) -> List[Dict[str, Any]]:
    """获取跌幅排行 - 优化版本，只获取部分数据"""
    all_quotes = []

    async with aiohttp.ClientSession() as session:
        # 只获取活跃股票代码范围，减少请求量
        codes = []
        # 沪市主板活跃股
        for code in range(600000, 603000):
            codes.append(f"sh{code}")
        # 深市主板
        for code in range(1, 3000):
            codes.append(f"sz{str(code).zfill(6)}")
        # 创业板
        for code in range(300000, 301500):
            codes.append(f"sz{code}")

        # 分批获取，每批800只，并行请求
        batch_size = 800
        tasks = []
        for i in range(0, len(codes), batch_size):
            batch = codes[i : i + batch_size]
            tasks.append(self._fetch_batch(session, batch))

        # 并行执行所有批次
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, list):
                all_quotes.extend(result)

    # 筛选跌幅为负的股票
    down_quotes = [
        q for q in all_quotes if q.get("涨跌幅") is not None and q["涨跌幅"] < 0
    ]

    # 按跌幅排序
    down_quotes.sort(key=lambda x: x.get("涨跌幅", 0))

    logger.info(f"新浪数据源获取跌幅榜 {len(down_quotes)} 条")
    return down_quotes[:limit]


sina_source = SinaFinanceSource()
