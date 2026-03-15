# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/15
# @File           : pytdx_source.py
# @IDE            : PyCharm
# @desc           : pytdx 数据源 - 通达信行情接口

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor
from app.core.logging import get_logger

logger = get_logger(__name__)

# pytdx 导入
try:
    from pytdx.hq import TdxHq_API
    PYTDX_AVAILABLE = True
except ImportError:
    PYTDX_AVAILABLE = False
    logger.warning("pytdx 未安装，该数据源不可用")

# 通达信服务器列表
TDX_SERVERS = [
    ('119.147.212.81', 7709),
    ('14.215.128.18', 7709),
    ('59.173.18.140', 7709),
    ('180.153.18.170', 7709),
    ('180.153.18.171', 7709),
    ('180.153.39.51', 7709),
    ('218.75.126.9', 7709),
    ('115.238.56.198', 7709),
    ('115.238.90.165', 7709),
    ('124.160.88.183', 7709),
    ('60.12.136.250', 7709),
    ('60.191.117.167', 7709),
    ('61.152.107.171', 7709),
]


class PytdxDataSource:
    """pytdx 数据源 - 通达信行情"""

    def __init__(self):
        self.api = None
        self.connected = False
        self._executor = ThreadPoolExecutor(max_workers=1)

    def _connect(self) -> bool:
        """连接到通达信服务器"""
        if not PYTDX_AVAILABLE:
            return False

        try:
            self.api = TdxHq_API()
            # 尝试连接服务器
            for host, port in TDX_SERVERS:
                try:
                    if self.api.connect(host, port):
                        self.connected = True
                        logger.info(f"pytdx 连接成功: {host}:{port}")
                        return True
                except Exception as e:
                    logger.debug(f"pytdx 连接 {host}:{port} 失败: {e}")
                    continue

            logger.warning("pytdx 所有服务器连接失败")
            return False
        except Exception as e:
            logger.error(f"pytdx 初始化失败: {e}")
            return False

    def _disconnect(self):
        """断开连接"""
        if self.api:
            try:
                self.api.disconnect()
            except:
                pass
        self.connected = False

    def _ensure_connection(self) -> bool:
        """确保连接"""
        if not self.connected:
            return self._connect()
        return True

    async def get_market_summary(self) -> Optional[Dict[str, Any]]:
        """
        获取市场汇总数据

        Returns:
            市场汇总数据字典
        """
        if not PYTDX_AVAILABLE:
            return None

        try:
            # 在线程池中执行同步操作
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self._executor,
                self._get_market_summary_sync
            )
            return result
        except Exception as e:
            logger.error(f"pytdx 获取市场汇总失败: {e}")
            return None

    def _get_market_summary_sync(self) -> Optional[Dict[str, Any]]:
        """同步获取市场汇总"""
        if not self._ensure_connection():
            return None

        try:
            # 获取所有股票行情
            all_stocks = []

            # 获取上海市场
            for start in range(0, 3000, 1000):
                data = self.api.get_security_list(1, start)
                if data:
                    all_stocks.extend(data)

            # 获取深圳市场
            for start in range(0, 3000, 1000):
                data = self.api.get_security_list(0, start)
                if data:
                    all_stocks.extend(data)

            if not all_stocks:
                return None

            # 统计涨跌
            up_count = 0
            down_count = 0
            flat_count = 0
            limit_up = 0
            limit_down = 0
            total_amount = 0
            total_volume = 0

            for stock in all_stocks:
                code = stock.get('code', '')
                if not code:
                    continue

                # 获取实时行情
                quote = self.api.get_security_quotes([(1 if code.startswith('6') else 0, code)])
                if quote and len(quote) > 0:
                    q = quote[0]
                    price = q.get('price', 0)
                    last_close = q.get('last_close', 0)

                    if last_close > 0 and price > 0:
                        change_pct = (price - last_close) / last_close * 100

                        if change_pct > 0:
                            up_count += 1
                            if change_pct >= 9.9:
                                limit_up += 1
                        elif change_pct < 0:
                            down_count += 1
                            if change_pct <= -9.9:
                                limit_down += 1
                        else:
                            flat_count += 1

                        total_amount += q.get('amount', 0)
                        total_volume += q.get('vol', 0)

            total_stocks = up_count + down_count + flat_count

            logger.info(f"pytdx 获取市场汇总成功: {total_stocks}只股票")

            return {
                "total_stocks": total_stocks,
                "up_stocks": up_count,
                "down_stocks": down_count,
                "flat_stocks": flat_count,
                "total_amount": total_amount,
                "total_volume": total_volume,
                "limit_up_count": limit_up,
                "limit_down_count": limit_down,
                "trade_date": str(date.today()),
                "update_time": datetime.now().isoformat(),
                "source": "pytdx"
            }

        except Exception as e:
            logger.error(f"pytdx 同步获取市场汇总失败: {e}")
            self._disconnect()
            return None

    async def get_stock_list(self, limit: int = 100) -> Optional[List[Dict[str, Any]]]:
        """
        获取股票列表行情

        Args:
            limit: 返回数量限制

        Returns:
            股票行情列表
        """
        if not PYTDX_AVAILABLE:
            return None

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self._executor,
                lambda: self._get_stock_list_sync(limit)
            )
            return result
        except Exception as e:
            logger.error(f"pytdx 获取股票列表失败: {e}")
            return None

    def _get_stock_list_sync(self, limit: int) -> Optional[List[Dict[str, Any]]]:
        """同步获取股票列表"""
        if not self._ensure_connection():
            return None

        try:
            stocks = []

            # 获取上海市场股票
            for start in range(0, min(limit, 2000), 100):
                data = self.api.get_security_list(1, start)
                if data:
                    for item in data:
                        code = item.get('code', '')
                        name = item.get('name', '')
                        if code and not name.startswith('ST'):
                            stocks.append({
                                'code': code,
                                'name': name,
                                'market': 1 if code.startswith('6') else 0
                            })

            # 获取深圳市场股票
            for start in range(0, min(limit, 2000), 100):
                data = self.api.get_security_list(0, start)
                if data:
                    for item in data:
                        code = item.get('code', '')
                        name = item.get('name', '')
                        if code and not name.startswith('ST'):
                            stocks.append({
                                'code': code,
                                'name': name,
                                'market': 0
                            })

            # 获取实时行情
            result = []
            batch_size = 80  # pytdx 每次最多查询80只股票

            for i in range(0, min(len(stocks), limit), batch_size):
                batch = stocks[i:i + batch_size]
                quotes_params = [(s['market'], s['code']) for s in batch]
                quotes = self.api.get_security_quotes(quotes_params)

                if quotes:
                    for q in quotes:
                        code = q.get('code', '')
                        price = q.get('price', 0)
                        last_close = q.get('last_close', 0)

                        change_pct = 0
                        change_amt = 0
                        if last_close > 0 and price > 0:
                            change_pct = (price - last_close) / last_close * 100
                            change_amt = price - last_close

                        result.append({
                            '代码': code,
                            '名称': q.get('name', ''),
                            '最新价': price,
                            '涨跌幅': round(change_pct, 2),
                            '涨跌额': round(change_amt, 2),
                            '成交量': q.get('vol', 0),
                            '成交额': q.get('amount', 0),
                            '换手率': None,  # pytdx 不直接提供换手率
                        })

            logger.info(f"pytdx 获取到 {len(result)} 条股票行情")
            return result

        except Exception as e:
            logger.error(f"pytdx 同步获取股票列表失败: {e}")
            self._disconnect()
            return None

    async def get_index_quotes(self) -> Optional[List[Dict[str, Any]]]:
        """
        获取主要指数行情

        Returns:
            指数行情列表
        """
        if not PYTDX_AVAILABLE:
            return None

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self._executor,
                self._get_index_quotes_sync
            )
            return result
        except Exception as e:
            logger.error(f"pytdx 获取指数行情失败: {e}")
            return None

    def _get_index_quotes_sync(self) -> Optional[List[Dict[str, Any]]]:
        """同步获取指数行情"""
        if not self._ensure_connection():
            return None

        try:
            # 主要指数代码
            indices = [
                (1, '000001', '上证指数'),
                (0, '399001', '深证成指'),
                (0, '399006', '创业板指'),
                (1, '000688', '科创50'),
            ]

            result = []
            quotes_params = [(m, c) for m, c, _ in indices]
            quotes = self.api.get_security_quotes(quotes_params)

            if quotes:
                for i, q in enumerate(quotes):
                    price = q.get('price', 0)
                    last_close = q.get('last_close', 0)
                    change_pct = 0
                    change_amt = 0

                    if last_close > 0 and price > 0:
                        change_pct = (price - last_close) / last_close * 100
                        change_amt = price - last_close

                    result.append({
                        'code': indices[i][1],
                        'name': indices[i][2],
                        'price': price,
                        'change_percent': round(change_pct, 2),
                        'change': round(change_amt, 2),
                        'volume': q.get('vol', 0),
                        'amount': q.get('amount', 0),
                    })

            logger.info(f"pytdx 获取到 {len(result)} 条指数行情")
            return result

        except Exception as e:
            logger.error(f"pytdx 同步获取指数行情失败: {e}")
            self._disconnect()
            return None


# 创建全局实例
pytdx_source = PytdxDataSource()