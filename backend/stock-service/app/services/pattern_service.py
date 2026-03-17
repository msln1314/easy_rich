# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : pattern_service.py
# @IDE            : PyCharm
# @desc           : K线形态识别服务 - W底、M头、头肩顶等形态识别

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field

import akshare as ak
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)


@dataclass
class PatternResult:
    stock_code: str
    stock_name: str
    pattern_type: str
    pattern_name: str
    confidence: float
    signal: str  # buy/sell/hold
    price: Optional[float]
    target_price: Optional[float]
    stop_loss: Optional[float]
    description: str
    detected_time: str = field(default_factory=lambda: datetime.now().isoformat())


class PatternService:
    async def _get_kline_data(self, stock_code: str, days: int = 60) -> pd.DataFrame:
        try:
            start_date = (datetime.now() - timedelta(days=days * 2)).strftime("%Y%m%d")
            end_date = datetime.now().strftime("%Y%m%d")

            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq",
            )

            if df.empty:
                return pd.DataFrame()

            df = df.rename(
                columns={
                    "日期": "date",
                    "开盘": "open",
                    "收盘": "close",
                    "最高": "high",
                    "最低": "low",
                    "成交量": "volume",
                }
            )

            return df.tail(days)
        except Exception as e:
            logger.warning(f"获取K线数据失败: {e}")
            return pd.DataFrame()

    def _find_peaks(self, series: pd.Series, window: int = 5) -> List[int]:
        peaks = []
        for i in range(window, len(series) - window):
            if all(series[i] >= series[i - window : i]) and all(
                series[i] >= series[i + 1 : i + window + 1]
            ):
                peaks.append(i)
        return peaks

    def _find_troughs(self, series: pd.Series, window: int = 5) -> List[int]:
        troughs = []
        for i in range(window, len(series) - window):
            if all(series[i] <= series[i - window : i]) and all(
                series[i] <= series[i + 1 : i + window + 1]
            ):
                troughs.append(i)
        return troughs

    async def detect_w_bottom(self, stock_code: str) -> Optional[PatternResult]:
        """检测W底（双底）形态"""
        df = await self._get_kline_data(stock_code, 60)
        if df.empty or len(df) < 30:
            return None

        lows = df["low"]
        troughs = self._find_troughs(lows, window=3)

        if len(troughs) < 2:
            return None

        for i in range(len(troughs) - 1):
            t1, t2 = troughs[i], troughs[i + 1]

            if t2 - t1 < 10:
                continue

            low1, low2 = lows.iloc[t1], lows.iloc[t2]

            if abs(low1 - low2) / low1 < 0.03:
                between_high = df["high"].iloc[t1:t2].max()
                neckline = between_high

                if (between_high - low1) / low1 > 0.1:
                    current_price = df["close"].iloc[-1]

                    return PatternResult(
                        stock_code=stock_code,
                        stock_name="",
                        pattern_type="W_BOTTOM",
                        pattern_name="W底（双底）",
                        confidence=0.75,
                        signal="buy",
                        price=current_price,
                        target_price=current_price * 1.15,
                        stop_loss=low1 * 0.97,
                        description=f"检测到W底形态，两个低点分别为{low1:.2f}和{low2:.2f}，颈线位{neckline:.2f}",
                    )

        return None

    async def detect_m_top(self, stock_code: str) -> Optional[PatternResult]:
        """检测M头（双顶）形态"""
        df = await self._get_kline_data(stock_code, 60)
        if df.empty or len(df) < 30:
            return None

        highs = df["high"]
        peaks = self._find_peaks(highs, window=3)

        if len(peaks) < 2:
            return None

        for i in range(len(peaks) - 1):
            p1, p2 = peaks[i], peaks[i + 1]

            if p2 - p1 < 10:
                continue

            high1, high2 = highs.iloc[p1], highs.iloc[p2]

            if abs(high1 - high2) / high1 < 0.03:
                between_low = df["low"].iloc[p1:p2].min()
                neckline = between_low

                if (high1 - between_low) / between_low > 0.1:
                    current_price = df["close"].iloc[-1]

                    return PatternResult(
                        stock_code=stock_code,
                        stock_name="",
                        pattern_type="M_TOP",
                        pattern_name="M头（双顶）",
                        confidence=0.75,
                        signal="sell",
                        price=current_price,
                        target_price=current_price * 0.85,
                        stop_loss=high1 * 1.03,
                        description=f"检测到M头形态，两个高点分别为{high1:.2f}和{high2:.2f}，颈线位{neckline:.2f}",
                    )

        return None

    async def detect_head_shoulders(self, stock_code: str) -> Optional[PatternResult]:
        """检测头肩顶/头肩底形态"""
        df = await self._get_kline_data(stock_code, 90)
        if df.empty or len(df) < 60:
            return None

        highs = df["high"]
        lows = df["low"]

        peaks = self._find_peaks(highs, window=5)
        troughs = self._find_troughs(lows, window=5)

        if len(peaks) >= 3 and len(troughs) >= 2:
            for i in range(len(peaks) - 2):
                left_shoulder = peaks[i]
                head = peaks[i + 1]
                right_shoulder = peaks[i + 2] if i + 2 < len(peaks) else None

                if right_shoulder is None:
                    continue

                if not (left_shoulder < head > right_shoulder):
                    continue

                ls_high = highs.iloc[left_shoulder]
                head_high = highs.iloc[head]
                rs_high = highs.iloc[right_shoulder]

                if abs(ls_high - rs_high) / ls_high < 0.05:
                    if (head_high - ls_high) / ls_high > 0.05:
                        neckline = min(lows.iloc[left_shoulder : right_shoulder + 1])
                        current_price = df["close"].iloc[-1]

                        return PatternResult(
                            stock_code=stock_code,
                            stock_name="",
                            pattern_type="HEAD_SHOULDERS_TOP",
                            pattern_name="头肩顶",
                            confidence=0.80,
                            signal="sell",
                            price=current_price,
                            target_price=current_price * 0.80,
                            stop_loss=head_high * 1.02,
                            description=f"检测到头肩顶形态，左肩{ls_high:.2f}，头部{head_high:.2f}，右肩{rs_high:.2f}",
                        )

        return None

    async def detect_breakout(self, stock_code: str) -> Optional[PatternResult]:
        """检测突破形态"""
        df = await self._get_kline_data(stock_code, 30)
        if df.empty or len(df) < 20:
            return None

        recent_high = df["high"].iloc[:-1].max()
        recent_low = df["low"].iloc[:-1].min()
        current_price = df["close"].iloc[-1]
        current_high = df["high"].iloc[-1]

        if current_high > recent_high:
            return PatternResult(
                stock_code=stock_code,
                stock_name="",
                pattern_type="BREAKOUT_UP",
                pattern_name="向上突破",
                confidence=0.70,
                signal="buy",
                price=current_price,
                target_price=current_price * 1.10,
                stop_loss=recent_high * 0.97,
                description=f"股价突破近期高点{recent_high:.2f}，当前价{current_price:.2f}",
            )

        if current_price < recent_low:
            return PatternResult(
                stock_code=stock_code,
                stock_name="",
                pattern_type="BREAKOUT_DOWN",
                pattern_name="向下突破",
                confidence=0.70,
                signal="sell",
                price=current_price,
                target_price=current_price * 0.90,
                stop_loss=recent_low * 1.03,
                description=f"股价跌破近期低点{recent_low:.2f}，当前价{current_price:.2f}",
            )

        return None

    async def detect_all_patterns(self, stock_code: str) -> List[PatternResult]:
        """检测所有形态"""
        results = []

        w_bottom = await self.detect_w_bottom(stock_code)
        if w_bottom:
            results.append(w_bottom)

        m_top = await self.detect_m_top(stock_code)
        if m_top:
            results.append(m_top)

        head_shoulders = await self.detect_head_shoulders(stock_code)
        if head_shoulders:
            results.append(head_shoulders)

        breakout = await self.detect_breakout(stock_code)
        if breakout:
            results.append(breakout)

        return results

    async def scan_patterns(
        self, stock_codes: List[str], pattern_type: Optional[str] = None
    ) -> List[PatternResult]:
        """批量扫描形态"""
        results = []

        for code in stock_codes[:50]:
            try:
                if pattern_type == "W_BOTTOM":
                    result = await self.detect_w_bottom(code)
                    if result:
                        results.append(result)
                elif pattern_type == "M_TOP":
                    result = await self.detect_m_top(code)
                    if result:
                        results.append(result)
                elif pattern_type == "HEAD_SHOULDERS":
                    result = await self.detect_head_shoulders(code)
                    if result:
                        results.append(result)
                elif pattern_type == "BREAKOUT":
                    result = await self.detect_breakout(code)
                    if result:
                        results.append(result)
                else:
                    patterns = await self.detect_all_patterns(code)
                    results.extend(patterns)
            except Exception as e:
                logger.warning(f"扫描 {code} 形态失败: {e}")
                continue

        return results


pattern_service = PatternService()
