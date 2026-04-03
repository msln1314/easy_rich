# backend/qmt-service/app/services/quote_service.py
"""
L2行情服务

提供十档行情、逐笔成交、分时数据等L2级别行情功能
"""
import logging
from datetime import datetime
from typing import List, Optional
import asyncio

from app.core.qmt_client import QMTClientManager
from app.models.quote_models import (
    L2Quote,
    L2QuoteListResponse,
    Tick,
    TickListResponse,
    MinuteBar,
    MinuteBarListResponse,
    OrderBook,
    DepthResponse,
    QuoteStatus,
)

logger = logging.getLogger(__name__)


class QuoteService:
    """L2行情服务"""

    # 缓存行情数据
    _quote_cache: dict = {}
    _subscribed_codes: set = set()
    _l2_enabled: bool = False

    async def get_l2_quote(self, stock_code: str) -> Optional[L2Quote]:
        """获取单只股票L2十档行情"""
        if not QMTClientManager.is_connected():
            return self._mock_l2_quote(stock_code)

        try:
            from xtquant import xtdata

            # 获取完整行情数据
            full_tick = xtdata.get_full_tick([stock_code])
            if not full_tick or stock_code not in full_tick:
                logger.warning(f"未获取到 {stock_code} 的行情数据")
                return self._mock_l2_quote(stock_code)

            tick_data = full_tick[stock_code]
            return self._convert_l2_quote(stock_code, tick_data)

        except ImportError:
            logger.warning("xtquant未安装，使用模拟数据")
            return self._mock_l2_quote(stock_code)
        except Exception as e:
            logger.error(f"获取L2行情失败: {e}")
            return self._mock_l2_quote(stock_code)

    async def get_l2_quotes(self, stock_codes: List[str]) -> L2QuoteListResponse:
        """批量获取L2十档行情"""
        if not QMTClientManager.is_connected():
            return self._mock_l2_quotes(stock_codes)

        try:
            from xtquant import xtdata

            full_tick = xtdata.get_full_tick(stock_codes)
            quotes = []

            for code in stock_codes:
                if code in full_tick:
                    quotes.append(self._convert_l2_quote(code, full_tick[code]))
                else:
                    # 尝试获取单只
                    quote = await self.get_l2_quote(code)
                    if quote:
                        quotes.append(quote)

            return L2QuoteListResponse(quotes=quotes, count=len(quotes))

        except Exception as e:
            logger.error(f"批量获取L2行情失败: {e}")
            return self._mock_l2_quotes(stock_codes)

    async def get_ticks(
        self,
        stock_code: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        count: int = 100
    ) -> TickListResponse:
        """获取逐笔成交数据"""
        if not QMTClientManager.is_connected():
            return self._mock_ticks(stock_code, count)

        try:
            from xtquant import xtdata

            # 获取逐笔成交
            ticks_data = xtdata.get_market_data(
                stock_list=[stock_code],
                period='tick',
                start_time=start_time or '',
                end_time=end_time or '',
                count=count
            )

            if ticks_data is None or ticks_data.empty:
                return self._mock_ticks(stock_code, count)

            ticks = []
            for idx, row in ticks_data.iterrows():
                tick = Tick(
                    tick_id=f"{stock_code}_{idx.timestamp()}",
                    stock_code=stock_code,
                    price=float(row.get('lastPrice', 0)),
                    volume=int(row.get('lastVolume', 0)),
                    direction=self._get_tick_direction(row),
                    trade_time=idx.to_pydatetime(),
                    order_type=self._get_order_type(row)
                )
                ticks.append(tick)

            return TickListResponse(stock_code=stock_code, ticks=ticks, count=len(ticks))

        except Exception as e:
            logger.error(f"获取逐笔成交失败: {e}")
            return self._mock_ticks(stock_code, count)

    async def get_minute_bars(
        self,
        stock_code: str,
        date: Optional[str] = None
    ) -> MinuteBarListResponse:
        """获取分时数据"""
        if not QMTClientManager.is_connected():
            return self._mock_minute_bars(stock_code, date)

        try:
            from xtquant import xtdata

            # 获取分时数据
            if date:
                start_time = f"{date} 09:30:00"
                end_time = f"{date} 15:00:00"
            else:
                today = datetime.now().strftime("%Y%m%d")
                start_time = f"{today} 09:30:00"
                end_time = f"{today} 15:00:00"

            data = xtdata.get_market_data(
                stock_list=[stock_code],
                period='1m',
                start_time=start_time,
                end_time=end_time
            )

            if data is None or data.empty:
                return self._mock_minute_bars(stock_code, date)

            bars = []
            for idx, row in data.iterrows():
                bar = MinuteBar(
                    stock_code=stock_code,
                    time=idx.to_pydatetime(),
                    price=float(row.get('close', 0)),
                    volume=int(row.get('volume', 0)),
                    amount=float(row.get('amount', 0)),
                    avg_price=float(row.get('amount', 0)) / max(int(row.get('volume', 1)), 1),
                    open=float(row.get('open', 0)),
                    high=float(row.get('high', 0)),
                    low=float(row.get('low', 0))
                )
                bars.append(bar)

            return MinuteBarListResponse(
                stock_code=stock_code,
                date=date or datetime.now().strftime("%Y%m%d"),
                bars=bars,
                count=len(bars)
            )

        except Exception as e:
            logger.error(f"获取分时数据失败: {e}")
            return self._mock_minute_bars(stock_code, date)

    async def get_depth(self, stock_code: str) -> DepthResponse:
        """获取订单簿深度"""
        quote = await self.get_l2_quote(stock_code)

        bid_levels = [
            {"price": quote.bid_price1, "volume": quote.bid_volume1},
            {"price": quote.bid_price2, "volume": quote.bid_volume2},
            {"price": quote.bid_price3, "volume": quote.bid_volume3},
            {"price": quote.bid_price4, "volume": quote.bid_volume4},
            {"price": quote.bid_price5, "volume": quote.bid_volume5},
            {"price": quote.bid_price6, "volume": quote.bid_volume6},
            {"price": quote.bid_price7, "volume": quote.bid_volume7},
            {"price": quote.bid_price8, "volume": quote.bid_volume8},
            {"price": quote.bid_price9, "volume": quote.bid_volume9},
            {"price": quote.bid_price10, "volume": quote.bid_volume10},
        ]

        ask_levels = [
            {"price": quote.ask_price1, "volume": quote.ask_volume1},
            {"price": quote.ask_price2, "volume": quote.ask_volume2},
            {"price": quote.ask_price3, "volume": quote.ask_volume3},
            {"price": quote.ask_price4, "volume": quote.ask_volume4},
            {"price": quote.ask_price5, "volume": quote.ask_volume5},
            {"price": quote.ask_price6, "volume": quote.ask_volume6},
            {"price": quote.ask_price7, "volume": quote.ask_volume7},
            {"price": quote.ask_price8, "volume": quote.ask_volume8},
            {"price": quote.ask_price9, "volume": quote.ask_volume9},
            {"price": quote.ask_price10, "volume": quote.ask_volume10},
        ]

        order_book = OrderBook(
            stock_code=stock_code,
            price=quote.price,
            bid_levels=[l for l in bid_levels if l["price"] > 0],
            ask_levels=[l for l in ask_levels if l["price"] > 0],
            updated_time=quote.updated_time
        )

        return DepthResponse(stock_code=stock_code, depth=order_book)

    async def subscribe_quotes(self, stock_codes: List[str]) -> QuoteStatus:
        """订阅行情"""
        if not QMTClientManager.is_connected():
            self._subscribed_codes.update(stock_codes)
            return QuoteStatus(
                subscribed=True,
                stock_codes=list(self._subscribed_codes),
                l2_enabled=False,
                message="模拟模式订阅成功"
            )

        try:
            from xtquant import xtdata

            # 订阅行情
            for code in stock_codes:
                xtdata.subscribe_quote(
                    stock_code=code,
                    callback=self._quote_callback
                )
                self._subscribed_codes.add(code)

            self._l2_enabled = True

            return QuoteStatus(
                subscribed=True,
                stock_codes=list(self._subscribed_codes),
                l2_enabled=self._l2_enabled,
                message=f"已订阅 {len(stock_codes)} 只股票行情"
            )

        except Exception as e:
            logger.error(f"订阅行情失败: {e}")
            return QuoteStatus(
                subscribed=False,
                stock_codes=[],
                l2_enabled=False,
                message=f"订阅失败: {str(e)}"
            )

    async def unsubscribe_quotes(self, stock_codes: List[str] = None) -> QuoteStatus:
        """取消订阅"""
        if stock_codes:
            self._subscribed_codes -= set(stock_codes)
        else:
            self._subscribed_codes.clear()

        return QuoteStatus(
            subscribed=len(self._subscribed_codes) > 0,
            stock_codes=list(self._subscribed_codes),
            l2_enabled=self._l2_enabled,
            message="取消订阅成功"
        )

    def get_subscription_status(self) -> QuoteStatus:
        """获取订阅状态"""
        return QuoteStatus(
            subscribed=len(self._subscribed_codes) > 0,
            stock_codes=list(self._subscribed_codes),
            l2_enabled=self._l2_enabled,
            message="订阅状态正常" if self._subscribed_codes else "未订阅任何股票"
        )

    def _quote_callback(self, data):
        """行情回调"""
        try:
            if data and 'stock_code' in data:
                self._quote_cache[data['stock_code']] = data
        except Exception as e:
            logger.error(f"行情回调处理失败: {e}")

    def _convert_l2_quote(self, stock_code: str, tick_data) -> L2Quote:
        """转换L2行情数据"""
        now = datetime.now()

        try:
            return L2Quote(
                stock_code=stock_code,
                stock_name=tick_data.get('stock_name', ''),
                price=float(tick_data.get('lastPrice', 0)),
                open=float(tick_data.get('open', 0)),
                high=float(tick_data.get('high', 0)),
                low=float(tick_data.get('low', 0)),
                pre_close=float(tick_data.get('lastClose', 0)),
                volume=int(tick_data.get('volume', 0)),
                amount=float(tick_data.get('amount', 0)),

                # 买盘
                bid_price1=float(tick_data.get('bidPrice1', 0)),
                bid_volume1=int(tick_data.get('bidVol1', 0)),
                bid_price2=float(tick_data.get('bidPrice2', 0)),
                bid_volume2=int(tick_data.get('bidVol2', 0)),
                bid_price3=float(tick_data.get('bidPrice3', 0)),
                bid_volume3=int(tick_data.get('bidVol3', 0)),
                bid_price4=float(tick_data.get('bidPrice4', 0)),
                bid_volume4=int(tick_data.get('bidVol4', 0)),
                bid_price5=float(tick_data.get('bidPrice5', 0)),
                bid_volume5=int(tick_data.get('bidVol5', 0)),

                # 卖盘
                ask_price1=float(tick_data.get('askPrice1', 0)),
                ask_volume1=int(tick_data.get('askVol1', 0)),
                ask_price2=float(tick_data.get('askPrice2', 0)),
                ask_volume2=int(tick_data.get('askVol2', 0)),
                ask_price3=float(tick_data.get('askPrice3', 0)),
                ask_volume3=int(tick_data.get('askVol3', 0)),
                ask_price4=float(tick_data.get('askPrice4', 0)),
                ask_volume4=int(tick_data.get('askVol4', 0)),
                ask_price5=float(tick_data.get('askPrice5', 0)),
                ask_volume5=int(tick_data.get('askVol5', 0)),

                # L2扩展档位 (需要L2权限)
                bid_price6=float(tick_data.get('bidPrice6', 0)),
                bid_volume6=int(tick_data.get('bidVol6', 0)),
                bid_price7=float(tick_data.get('bidPrice7', 0)),
                bid_volume7=int(tick_data.get('bidVol7', 0)),
                bid_price8=float(tick_data.get('bidPrice8', 0)),
                bid_volume8=int(tick_data.get('bidVol8', 0)),
                bid_price9=float(tick_data.get('bidPrice9', 0)),
                bid_volume9=int(tick_data.get('bidVol9', 0)),
                bid_price10=float(tick_data.get('bidPrice10', 0)),
                bid_volume10=int(tick_data.get('bidVol10', 0)),

                ask_price6=float(tick_data.get('askPrice6', 0)),
                ask_volume6=int(tick_data.get('askVol6', 0)),
                ask_price7=float(tick_data.get('askPrice7', 0)),
                ask_volume7=int(tick_data.get('askVol7', 0)),
                ask_price8=float(tick_data.get('askPrice8', 0)),
                ask_volume8=int(tick_data.get('askVol8', 0)),
                ask_price9=float(tick_data.get('askPrice9', 0)),
                ask_volume9=int(tick_data.get('askVol9', 0)),
                ask_price10=float(tick_data.get('askPrice10', 0)),
                ask_volume10=int(tick_data.get('askVol10', 0)),

                updated_time=now
            )
        except Exception as e:
            logger.error(f"转换行情数据失败: {e}")
            return self._mock_l2_quote(stock_code)

    def _get_tick_direction(self, row) -> str:
        """判断逐笔成交方向"""
        try:
            # 根据成交价与买卖价判断
            last_price = row.get('lastPrice', 0)
            bid_price = row.get('bidPrice1', 0)
            ask_price = row.get('askPrice1', 0)

            if bid_price and ask_price:
                mid_price = (bid_price + ask_price) / 2
                if last_price >= mid_price:
                    return "buy"
                else:
                    return "sell"
        except:
            pass
        return "neutral"

    def _get_order_type(self, row) -> str:
        """判断订单类型"""
        try:
            volume = row.get('lastVolume', 0)
            # 简单判断：大于10万股为大单
            if volume >= 100000:
                return "block"
            elif volume >= 10000:
                return "large"
        except:
            pass
        return "normal"

    # ==================== 模拟数据 ====================

    def _mock_l2_quote(self, stock_code: str) -> L2Quote:
        """模拟L2行情"""
        now = datetime.now()
        base_price = 10.0 + hash(stock_code) % 100

        return L2Quote(
            stock_code=stock_code,
            stock_name=f"股票{stock_code}",
            price=base_price,
            open=base_price - 0.2,
            high=base_price + 0.3,
            low=base_price - 0.5,
            pre_close=base_price - 0.1,
            volume=1000000,
            amount=base_price * 1000000,

            # 买盘
            bid_price1=base_price - 0.01,
            bid_volume1=1000,
            bid_price2=base_price - 0.02,
            bid_volume2=2000,
            bid_price3=base_price - 0.03,
            bid_volume3=3000,
            bid_price4=base_price - 0.04,
            bid_volume4=4000,
            bid_price5=base_price - 0.05,
            bid_volume5=5000,

            # 卖盘
            ask_price1=base_price + 0.01,
            ask_volume1=1500,
            ask_price2=base_price + 0.02,
            ask_volume2=2500,
            ask_price3=base_price + 0.03,
            ask_volume3=3500,
            ask_price4=base_price + 0.04,
            ask_volume4=4500,
            ask_price5=base_price + 0.05,
            ask_volume5=5500,

            # L2扩展档位
            bid_price6=base_price - 0.06,
            bid_volume6=6000,
            bid_price7=base_price - 0.07,
            bid_volume7=7000,
            bid_price8=base_price - 0.08,
            bid_volume8=8000,
            bid_price9=base_price - 0.09,
            bid_volume9=9000,
            bid_price10=base_price - 0.10,
            bid_volume10=10000,

            ask_price6=base_price + 0.06,
            ask_volume6=6500,
            ask_price7=base_price + 0.07,
            ask_volume7=7500,
            ask_price8=base_price + 0.08,
            ask_volume8=8500,
            ask_price9=base_price + 0.09,
            ask_volume9=9500,
            ask_price10=base_price + 0.10,
            ask_volume10=10500,

            updated_time=now
        )

    def _mock_l2_quotes(self, stock_codes: List[str]) -> L2QuoteListResponse:
        """模拟批量L2行情"""
        quotes = [self._mock_l2_quote(code) for code in stock_codes]
        return L2QuoteListResponse(quotes=quotes, count=len(quotes))

    def _mock_ticks(self, stock_code: str, count: int) -> TickListResponse:
        """模拟逐笔成交"""
        now = datetime.now()
        base_price = 10.0 + hash(stock_code) % 100

        ticks = []
        for i in range(min(count, 50)):
            tick = Tick(
                tick_id=f"{stock_code}_{i}",
                stock_code=stock_code,
                price=base_price + (i % 5) * 0.01,
                volume=100 * (i + 1),
                direction="buy" if i % 3 == 0 else ("sell" if i % 3 == 1 else "neutral"),
                trade_time=now,
                order_type="large" if i % 10 == 0 else "normal"
            )
            ticks.append(tick)

        return TickListResponse(stock_code=stock_code, ticks=ticks, count=len(ticks))

    def _mock_minute_bars(self, stock_code: str, date: Optional[str]) -> MinuteBarListResponse:
        """模拟分时数据"""
        now = datetime.now()
        base_price = 10.0 + hash(stock_code) % 100

        bars = []
        # 模拟9:30-11:30, 13:00-15:00的交易时段
        for hour in [9, 10, 11, 13, 14]:
            for minute in range(60):
                if hour == 9 and minute < 30:
                    continue
                if hour == 11 and minute > 30:
                    continue
                if hour == 15 and minute > 0:
                    break

                time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                change = (minute % 10) * 0.01

                bar = MinuteBar(
                    stock_code=stock_code,
                    time=time,
                    price=base_price + change,
                    volume=10000 + minute * 100,
                    amount=(base_price + change) * (10000 + minute * 100),
                    avg_price=base_price + change,
                    open=base_price + change - 0.01,
                    high=base_price + change + 0.02,
                    low=base_price + change - 0.02
                )
                bars.append(bar)

        return MinuteBarListResponse(
            stock_code=stock_code,
            date=date or now.strftime("%Y%m%d"),
            bars=bars,
            count=len(bars)
        )


# 单例
quote_service = QuoteService()