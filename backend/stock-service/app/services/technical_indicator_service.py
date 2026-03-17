# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : technical_indicator_service.py
# @IDE            : PyCharm
# @desc           : 技术指标计算服务 - MACD、KDJ、RSI、BOLL、MA等

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field

import akshare as ak
from app.core.logging import get_logger
from app.utils.cache import cache_result
from app.utils.akshare_wrapper import handle_akshare_exception

logger = get_logger(__name__)


@dataclass
class MACDResult:
    """MACD指标结果"""

    date: str
    dif: Optional[float]
    dea: Optional[float]
    macd: Optional[float]
    signal: str = ""  # buy/sell/hold


@dataclass
class KDJResult:
    """KDJ指标结果"""

    date: str
    k: Optional[float]
    d: Optional[float]
    j: Optional[float]
    signal: str = ""


@dataclass
class RSIResult:
    """RSI指标结果"""

    date: str
    rsi_6: Optional[float]
    rsi_12: Optional[float]
    rsi_24: Optional[float]
    signal: str = ""


@dataclass
class BOLLResult:
    """布林带指标结果"""

    date: str
    upper: Optional[float]
    middle: Optional[float]
    lower: Optional[float]
    price: Optional[float]
    bandwidth: Optional[float]
    signal: str = ""


@dataclass
class MAResult:
    """均线指标结果"""

    date: str
    ma5: Optional[float]
    ma10: Optional[float]
    ma20: Optional[float]
    ma60: Optional[float]
    price: Optional[float]
    trend: str = ""


@dataclass
class VolumeResult:
    """成交量指标结果"""

    date: str
    volume: Optional[float]
    volume_ma5: Optional[float]
    volume_ma10: Optional[float]
    obv: Optional[float]
    signal: str = ""


@dataclass
class TechnicalAnalysis:
    """综合技术分析结果"""

    stock_code: str
    date: str
    price: Optional[float]
    macd_signal: str
    kdj_signal: str
    rsi_signal: str
    boll_signal: str
    ma_trend: str
    volume_signal: str
    overall_signal: str
    score: int


class TechnicalIndicatorService:
    """技术指标计算服务"""

    async def _get_history_data(self, stock_code: str, days: int = 120) -> pd.DataFrame:
        """获取历史数据用于计算"""
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
                    "成交额": "amount",
                }
            )

            return df.tail(days)

        except Exception as e:
            logger.warning(f"获取历史数据失败: {e}")
            return pd.DataFrame()

    # ========== MACD ==========

    @cache_result(expire=300)
    async def calculate_macd(
        self,
        stock_code: str,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
        days: int = 60,
    ) -> List[MACDResult]:
        """计算MACD指标"""
        logger.info(f"计算MACD: {stock_code}")

        df = await self._get_history_data(stock_code, days + 50)
        if df.empty:
            return []

        close = df["close"].astype(float)

        ema_fast = close.ewm(span=fast_period, adjust=False).mean()
        ema_slow = close.ewm(span=slow_period, adjust=False).mean()
        dif = ema_fast - ema_slow
        dea = dif.ewm(span=signal_period, adjust=False).mean()
        macd = (dif - dea) * 2

        results = []
        for i in range(len(df) - days, len(df)):
            if i < 0:
                continue

            macd_val = macd.iloc[i]
            prev_macd = macd.iloc[i - 1] if i > 0 else 0

            signal = "hold"
            if macd_val > 0 and prev_macd <= 0:
                signal = "buy"
            elif macd_val < 0 and prev_macd >= 0:
                signal = "sell"

            results.append(
                MACDResult(
                    date=str(df["date"].iloc[i]),
                    dif=round(dif.iloc[i], 4) if not np.isnan(dif.iloc[i]) else None,
                    dea=round(dea.iloc[i], 4) if not np.isnan(dea.iloc[i]) else None,
                    macd=round(macd_val, 4) if not np.isnan(macd_val) else None,
                    signal=signal,
                )
            )

        return results

    # ========== KDJ ==========

    @cache_result(expire=300)
    async def calculate_kdj(
        self, stock_code: str, n: int = 9, m1: int = 3, m2: int = 3, days: int = 60
    ) -> List[KDJResult]:
        """计算KDJ指标"""
        logger.info(f"计算KDJ: {stock_code}")

        df = await self._get_history_data(stock_code, days + 50)
        if df.empty:
            return []

        low_n = df["low"].astype(float).rolling(window=n, min_periods=1).min()
        high_n = df["high"].astype(float).rolling(window=n, min_periods=1).min()

        rsv = (df["close"].astype(float) - low_n) / (high_n - low_n + 0.0001) * 100

        k = rsv.ewm(alpha=1 / m1, adjust=False).mean()
        d = k.ewm(alpha=1 / m2, adjust=False).mean()
        j = 3 * k - 2 * d

        results = []
        for i in range(len(df) - days, len(df)):
            if i < 0:
                continue

            k_val = k.iloc[i]
            d_val = d.iloc[i]

            signal = "hold"
            if k_val > d_val and k.iloc[i - 1] <= d.iloc[i - 1] if i > 0 else False:
                signal = "buy"
            elif k_val < d_val and k.iloc[i - 1] >= d.iloc[i - 1] if i > 0 else False:
                signal = "sell"

            results.append(
                KDJResult(
                    date=str(df["date"].iloc[i]),
                    k=round(k_val, 2) if not np.isnan(k_val) else None,
                    d=round(d_val, 2) if not np.isnan(d_val) else None,
                    j=round(j.iloc[i], 2) if not np.isnan(j.iloc[i]) else None,
                    signal=signal,
                )
            )

        return results

    # ========== RSI ==========

    @cache_result(expire=300)
    async def calculate_rsi(
        self,
        stock_code: str,
        periods: Tuple[int, int, int] = (6, 12, 24),
        days: int = 60,
    ) -> List[RSIResult]:
        """计算RSI指标"""
        logger.info(f"计算RSI: {stock_code}")

        df = await self._get_history_data(stock_code, days + 50)
        if df.empty:
            return []

        close = df["close"].astype(float)
        delta = close.diff()

        rsi_values = {}
        for period in periods:
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=period, min_periods=1).mean()
            avg_loss = loss.rolling(window=period, min_periods=1).mean()
            rs = avg_gain / (avg_loss + 0.0001)
            rsi_values[period] = 100 - (100 / (1 + rs))

        results = []
        for i in range(len(df) - days, len(df)):
            if i < 0:
                continue

            rsi_6 = rsi_values[6].iloc[i]

            signal = "hold"
            if rsi_6 < 30:
                signal = "oversold"
            elif rsi_6 > 70:
                signal = "overbought"

            results.append(
                RSIResult(
                    date=str(df["date"].iloc[i]),
                    rsi_6=round(rsi_values[6].iloc[i], 2)
                    if not np.isnan(rsi_values[6].iloc[i])
                    else None,
                    rsi_12=round(rsi_values[12].iloc[i], 2)
                    if not np.isnan(rsi_values[12].iloc[i])
                    else None,
                    rsi_24=round(rsi_values[24].iloc[i], 2)
                    if not np.isnan(rsi_values[24].iloc[i])
                    else None,
                    signal=signal,
                )
            )

        return results

    # ========== BOLL ==========

    @cache_result(expire=300)
    async def calculate_boll(
        self, stock_code: str, n: int = 20, k: float = 2.0, days: int = 60
    ) -> List[BOLLResult]:
        """计算布林带指标"""
        logger.info(f"计算BOLL: {stock_code}")

        df = await self._get_history_data(stock_code, days + 50)
        if df.empty:
            return []

        close = df["close"].astype(float)
        middle = close.rolling(window=n, min_periods=1).mean()
        std = close.rolling(window=n, min_periods=1).std()
        upper = middle + k * std
        lower = middle - k * std
        bandwidth = (upper - lower) / middle * 100

        results = []
        for i in range(len(df) - days, len(df)):
            if i < 0:
                continue

            price = close.iloc[i]
            upper_val = upper.iloc[i]
            lower_val = lower.iloc[i]

            signal = "hold"
            if price >= upper_val:
                signal = "overbought"
            elif price <= lower_val:
                signal = "oversold"

            results.append(
                BOLLResult(
                    date=str(df["date"].iloc[i]),
                    upper=round(upper_val, 2) if not np.isnan(upper_val) else None,
                    middle=round(middle.iloc[i], 2)
                    if not np.isnan(middle.iloc[i])
                    else None,
                    lower=round(lower_val, 2) if not np.isnan(lower_val) else None,
                    price=round(price, 2),
                    bandwidth=round(bandwidth.iloc[i], 2)
                    if not np.isnan(bandwidth.iloc[i])
                    else None,
                    signal=signal,
                )
            )

        return results

    # ========== MA ==========

    @cache_result(expire=300)
    async def calculate_ma(
        self,
        stock_code: str,
        periods: Tuple[int, int, int, int] = (5, 10, 20, 60),
        days: int = 60,
    ) -> List[MAResult]:
        """计算均线指标"""
        logger.info(f"计算MA: {stock_code}")

        df = await self._get_history_data(stock_code, days + 70)
        if df.empty:
            return []

        close = df["close"].astype(float)
        ma_values = {p: close.rolling(window=p, min_periods=1).mean() for p in periods}

        results = []
        for i in range(len(df) - days, len(df)):
            if i < 0:
                continue

            ma5 = ma_values[5].iloc[i]
            ma10 = ma_values[10].iloc[i]
            ma20 = ma_values[20].iloc[i]
            ma60 = ma_values[60].iloc[i] if 60 in ma_values else None
            price = close.iloc[i]

            trend = "neutral"
            if ma5 > ma10 > ma20:
                trend = "bullish"
            elif ma5 < ma10 < ma20:
                trend = "bearish"

            results.append(
                MAResult(
                    date=str(df["date"].iloc[i]),
                    ma5=round(ma5, 2) if not np.isnan(ma5) else None,
                    ma10=round(ma10, 2) if not np.isnan(ma10) else None,
                    ma20=round(ma20, 2) if not np.isnan(ma20) else None,
                    ma60=round(ma60, 2) if ma60 and not np.isnan(ma60) else None,
                    price=round(price, 2),
                    trend=trend,
                )
            )

        return results

    # ========== 成交量指标 ==========

    @cache_result(expire=300)
    async def calculate_volume(
        self, stock_code: str, days: int = 60
    ) -> List[VolumeResult]:
        """计算成交量指标"""
        logger.info(f"计算成交量指标: {stock_code}")

        df = await self._get_history_data(stock_code, days + 20)
        if df.empty:
            return []

        volume = df["volume"].astype(float)
        volume_ma5 = volume.rolling(window=5, min_periods=1).mean()
        volume_ma10 = volume.rolling(window=10, min_periods=1).mean()

        close = df["close"].astype(float)
        direction = np.where(close.diff() >= 0, 1, -1)
        obv = (volume * direction).cumsum()

        results = []
        for i in range(len(df) - days, len(df)):
            if i < 0:
                continue

            vol = volume.iloc[i]
            vol_ma5 = volume_ma5.iloc[i]

            signal = "normal"
            if vol > vol_ma5 * 2:
                signal = "volume_surge"
            elif vol < vol_ma5 * 0.5:
                signal = "volume_shrink"

            results.append(
                VolumeResult(
                    date=str(df["date"].iloc[i]),
                    volume=vol,
                    volume_ma5=round(vol_ma5, 0) if not np.isnan(vol_ma5) else None,
                    volume_ma10=round(volume_ma10.iloc[i], 0)
                    if not np.isnan(volume_ma10.iloc[i])
                    else None,
                    obv=round(obv.iloc[i], 0) if not np.isnan(obv.iloc[i]) else None,
                    signal=signal,
                )
            )

        return results

    # ========== 综合分析 ==========

    async def analyze_all(self, stock_code: str) -> TechnicalAnalysis:
        """综合技术分析"""
        logger.info(f"综合技术分析: {stock_code}")

        macd = await self.calculate_macd(stock_code, days=5)
        kdj = await self.calculate_kdj(stock_code, days=5)
        rsi = await self.calculate_rsi(stock_code, days=5)
        boll = await self.calculate_boll(stock_code, days=5)
        ma = await self.calculate_ma(stock_code, days=5)
        volume = await self.calculate_volume(stock_code, days=5)

        if not macd or not kdj or not rsi or not boll or not ma or not volume:
            return TechnicalAnalysis(
                stock_code=stock_code,
                date=datetime.now().strftime("%Y-%m-%d"),
                price=None,
                macd_signal="unknown",
                kdj_signal="unknown",
                rsi_signal="unknown",
                boll_signal="unknown",
                ma_trend="unknown",
                volume_signal="unknown",
                overall_signal="unknown",
                score=0,
            )

        latest_macd = macd[-1]
        latest_kdj = kdj[-1]
        latest_rsi = rsi[-1]
        latest_boll = boll[-1]
        latest_ma = ma[-1]
        latest_volume = volume[-1]

        score = 0
        if latest_macd.signal == "buy":
            score += 20
        elif latest_macd.signal == "sell":
            score -= 20

        if latest_kdj.signal == "buy":
            score += 15
        elif latest_kdj.signal == "sell":
            score -= 15

        if latest_rsi.signal == "oversold":
            score += 15
        elif latest_rsi.signal == "overbought":
            score -= 15

        if latest_boll.signal == "oversold":
            score += 15
        elif latest_boll.signal == "overbought":
            score -= 15

        if latest_ma.trend == "bullish":
            score += 20
        elif latest_ma.trend == "bearish":
            score -= 20

        if latest_volume.signal == "volume_surge":
            score += 10

        overall = "neutral"
        if score >= 50:
            overall = "strong_buy"
        elif score >= 30:
            overall = "buy"
        elif score <= -50:
            overall = "strong_sell"
        elif score <= -30:
            overall = "sell"

        return TechnicalAnalysis(
            stock_code=stock_code,
            date=latest_macd.date,
            price=latest_ma.price,
            macd_signal=latest_macd.signal,
            kdj_signal=latest_kdj.signal,
            rsi_signal=latest_rsi.signal,
            boll_signal=latest_boll.signal,
            ma_trend=latest_ma.trend,
            volume_signal=latest_volume.signal,
            overall_signal=overall,
            score=score,
        )


technical_indicator_service = TechnicalIndicatorService()
