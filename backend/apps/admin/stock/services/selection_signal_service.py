#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/21
# @File           : selection_signal_service.py
# @IDE            : PyCharm
# @desc           : 选股信号生成服务

import pandas as pd
import numpy as np
import json
from datetime import date, datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from apps.admin.stock.models.stock_basic_info import StockBasicInfo
from apps.admin.stock.models.stock_selection_signal import StockSelectionSignal
from apps.module_task.stock_service_client import StockServiceClient
from utils.stock import StockUtils
from core.logger import logger


class SelectionSignalService:
    """选股信号生成服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_signals_for_stock(
        self, stock_code: str, stock_name: str = None, days: int = 60
    ) -> Optional[Dict[str, Any]]:
        """
        为单只股票生成选股信号

        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            days: 历史数据天数

        Returns:
            Dict: 信号数据
        """
        try:
            async with StockServiceClient() as client:
                history_data = await client.get_stock_history(
                    stock_code, period="daily"
                )

            if not history_data or len(history_data) < 10:
                return None

            df = pd.DataFrame(history_data)
            df = df.rename(
                columns={
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "close": "close",
                    "volume": "volume",
                    "amount": "amount",
                }
            )

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            elif "trade_date" in df.columns:
                df["date"] = pd.to_datetime(df["trade_date"])

            df = df.sort_values("date").tail(days)

            if len(df) < 10:
                return None

            indicators = self._calculate_indicators(df)

            signals = self._detect_signals(df, indicators)

            scores = self._calculate_scores(df, indicators)

            total_score, recommend, confidence = self._generate_recommendation(
                signals, scores
            )

            signal_detail = {
                "signals": {k: v for k, v in signals.items() if v is not None},
                "scores": {k: round(v, 2) for k, v in scores.items() if v is not None},
            }

            latest = df.iloc[-1]
            signal_data = {
                "stock_code": stock_code,
                "stock_name": stock_name,
                "full_code": StockUtils.get_full_code(stock_code),
                "market": "SH" if stock_code.startswith("6") else "SZ",
                "signal_date": date.today(),
                "current_price": float(latest.get("close", 0)),
                "change_percent": float(latest.get("change_percent", 0))
                if "change_percent" in latest
                else None,
                "volume": float(latest.get("volume", 0)),
                "amount": float(latest.get("amount", 0)),
                "ma_signal": signals.get("ma_signal"),
                "macd_signal": signals.get("macd_signal"),
                "kdj_signal": signals.get("kdj_signal"),
                "rsi_signal": signals.get("rsi_signal"),
                "boll_signal": signals.get("boll_signal"),
                "volume_signal": signals.get("volume_signal"),
                "ma5": float(indicators.get("ma5", [0])[-1])
                if indicators.get("ma5") is not None
                else None,
                "ma10": float(indicators.get("ma10", [0])[-1])
                if indicators.get("ma10") is not None
                else None,
                "ma20": float(indicators.get("ma20", [0])[-1])
                if indicators.get("ma20") is not None
                else None,
                "dif": float(indicators.get("dif", [0])[-1])
                if indicators.get("dif") is not None
                else None,
                "dea": float(indicators.get("dea", [0])[-1])
                if indicators.get("dea") is not None
                else None,
                "macd": float(indicators.get("macd", [0])[-1])
                if indicators.get("macd") is not None
                else None,
                "k_value": float(indicators.get("k", [0])[-1])
                if indicators.get("k") is not None
                else None,
                "d_value": float(indicators.get("d", [0])[-1])
                if indicators.get("d") is not None
                else None,
                "j_value": float(indicators.get("j", [0])[-1])
                if indicators.get("j") is not None
                else None,
                "rsi_value": float(indicators.get("rsi", [0])[-1])
                if indicators.get("rsi") is not None
                else None,
                "macd_score": scores.get("macd_score"),
                "kdj_score": scores.get("kdj_score"),
                "rsi_score": scores.get("rsi_score"),
                "ma_score": scores.get("ma_score"),
                "volume_score": scores.get("volume_score"),
                "trend_score": scores.get("trend_score"),
                "potential_score": scores.get("potential_score"),
                "total_score": total_score,
                "recommend": recommend,
                "signal_strength": self._calculate_signal_strength(
                    signals, total_score
                ),
                "confidence": confidence,
                "volatility": scores.get("volatility"),
                "max_drawdown": scores.get("max_drawdown"),
                "signal_detail": json.dumps(signal_detail, ensure_ascii=False),
                "data_from": "system",
                "data_time": datetime.now(),
            }

            return signal_data

        except Exception as e:
            logger.error(f"生成股票 {stock_code} 信号失败: {str(e)}")
            return None

    def _calculate_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """计算技术指标"""
        indicators = {}

        try:
            close = df["close"]

            indicators["ma5"] = close.rolling(window=5).mean()
            indicators["ma10"] = close.rolling(window=10).mean()
            indicators["ma20"] = close.rolling(window=20).mean()

            exp_fast = close.ewm(span=12, adjust=False).mean()
            exp_slow = close.ewm(span=26, adjust=False).mean()
            indicators["dif"] = exp_fast - exp_slow
            indicators["dea"] = indicators["dif"].ewm(span=9, adjust=False).mean()
            indicators["macd"] = 2 * (indicators["dif"] - indicators["dea"])

            low_n = df["low"].rolling(window=9).min()
            high_n = df["high"].rolling(window=9).max()
            rsv = (close - low_n) / (high_n - low_n) * 100
            indicators["k"] = rsv.ewm(span=3, adjust=False).mean()
            indicators["d"] = indicators["k"].ewm(span=3, adjust=False).mean()
            indicators["j"] = 3 * indicators["k"] - 2 * indicators["d"]

            diff = close.diff()
            gain = (diff.where(diff > 0, 0)).rolling(window=14).mean()
            loss = (-diff.where(diff < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            indicators["rsi"] = 100 - (100 / (1 + rs))

            indicators["volume_ma5"] = df["volume"].rolling(window=5).mean()

        except Exception as e:
            logger.error(f"计算技术指标失败: {str(e)}")

        return indicators

    def _detect_signals(
        self, df: pd.DataFrame, indicators: Dict[str, Any]
    ) -> Dict[str, Optional[int]]:
        """检测技术信号"""
        signals = {
            "ma_signal": 0,
            "macd_signal": 0,
            "kdj_signal": 0,
            "rsi_signal": 0,
            "boll_signal": 0,
            "volume_signal": 0,
        }

        try:
            close = df["close"].iloc[-1]
            ma5 = indicators["ma5"].iloc[-1]
            ma10 = indicators["ma10"].iloc[-1]
            ma20 = indicators["ma20"].iloc[-1]

            ma5_prev = indicators["ma5"].iloc[-2]
            ma10_prev = indicators["ma10"].iloc[-2]

            if ma5 > ma10 and ma5_prev <= ma10_prev:
                signals["ma_signal"] = 1
            elif ma5 < ma10 and ma5_prev >= ma10_prev:
                signals["ma_signal"] = -1

            dif = indicators["dif"].iloc[-1]
            dea = indicators["dea"].iloc[-1]
            dif_prev = indicators["dif"].iloc[-2]
            dea_prev = indicators["dea"].iloc[-2]

            if dif > dea and dif_prev <= dea_prev:
                signals["macd_signal"] = 1
            elif dif < dea and dif_prev >= dea_prev:
                signals["macd_signal"] = -1

            k = indicators["k"].iloc[-1]
            d = indicators["d"].iloc[-1]
            k_prev = indicators["k"].iloc[-2]
            d_prev = indicators["d"].iloc[-2]

            if k > d and k_prev <= d_prev:
                signals["kdj_signal"] = 1
            elif k < d and k_prev >= d_prev:
                signals["kdj_signal"] = -1

            rsi = indicators["rsi"].iloc[-1]
            if rsi < 30:
                signals["rsi_signal"] = 1
            elif rsi > 70:
                signals["rsi_signal"] = -1

            volume = df["volume"].iloc[-1]
            volume_ma5 = indicators["volume_ma5"].iloc[-1]
            if volume > volume_ma5 * 1.5:
                signals["volume_signal"] = 1
            elif volume < volume_ma5 * 0.5:
                signals["volume_signal"] = -1

        except Exception as e:
            logger.error(f"检测信号失败: {str(e)}")

        return signals

    def _calculate_scores(
        self, df: pd.DataFrame, indicators: Dict[str, Any]
    ) -> Dict[str, Optional[float]]:
        """计算分项评分"""
        scores = {}

        try:
            close = df["close"].iloc[-1]

            macd = indicators["macd"].iloc[-1]
            dif = indicators["dif"].iloc[-1]
            dea = indicators["dea"].iloc[-1]
            dif_prev = indicators["dif"].iloc[-2]
            dea_prev = indicators["dea"].iloc[-2]

            macd_score = 0
            if macd > 0:
                macd_score += 10
            if dif > dea and dif_prev <= dea_prev:
                macd_score += 10
            scores["macd_score"] = macd_score

            k = indicators["k"].iloc[-1]
            d = indicators["d"].iloc[-1]
            j = indicators["j"].iloc[-1]
            k_prev = indicators["k"].iloc[-2]
            d_prev = indicators["d"].iloc[-2]

            kdj_score = 0
            if k < 30 and d < 30:
                kdj_score += 10
            if j < 20:
                kdj_score += 5
            if k > d and k_prev <= d_prev:
                kdj_score += 5
            scores["kdj_score"] = kdj_score

            rsi = indicators["rsi"].iloc[-1]
            rsi_score = 0
            if rsi < 30:
                rsi_score = 20
            elif rsi < 40:
                rsi_score = 15
            elif rsi < 50:
                rsi_score = 10
            scores["rsi_score"] = rsi_score

            ma5 = indicators["ma5"].iloc[-1]
            ma10 = indicators["ma10"].iloc[-1]
            ma20 = indicators["ma20"].iloc[-1]

            ma_score = 0
            if ma5 > ma10 > ma20:
                ma_score += 10
            if close > ma5:
                ma_score += 4
            if close > ma10:
                ma_score += 3
            if close > ma20:
                ma_score += 3
            scores["ma_score"] = ma_score

            volume = df["volume"].iloc[-1]
            volume_ma5 = indicators["volume_ma5"].iloc[-1]

            vol_score = 0
            if volume > volume_ma5:
                vol_score += 10
            if len(df) >= 3:
                volume_prev = df["volume"].iloc[-2]
                volume_prev2 = df["volume"].iloc[-3]
                if volume > volume_prev > volume_prev2:
                    vol_score += 10
            scores["volume_score"] = vol_score

            trend_score = 0
            if len(df) >= 5:
                short_term = df["close"].iloc[-5:].pct_change().mean()
                if len(df) >= 20:
                    long_term = df["close"].iloc[-20:].pct_change().mean()
                else:
                    long_term = df["close"].pct_change().mean()

                if short_term > long_term:
                    trend_score += 10

                if close > df["close"].iloc[-5]:
                    trend_score += 5
                if (
                    close > df["close"].iloc[-20]
                    if len(df) >= 20
                    else df["close"].iloc[0]
                ):
                    trend_score += 5
            scores["trend_score"] = trend_score

            potential_score = 0
            if len(df) >= 5:
                recent_high = df["high"].iloc[-5:].max()
                if close > recent_high:
                    potential_score += 8

                volume_avg_10 = (
                    df["volume"].iloc[-10:].mean()
                    if len(df) >= 10
                    else df["volume"].mean()
                )
                if volume > volume_avg_10 * 1.5:
                    potential_score += 7

                if macd > 0 and dif > dea and dif_prev <= dea_prev:
                    potential_score += 10

                if k < 30 and d < 30 and k > d:
                    potential_score += 8
            scores["potential_score"] = potential_score

            volatility = df["close"].pct_change().std()
            scores["volatility"] = (
                float(volatility) if not pd.isna(volatility) else None
            )

            max_drawdown = 0
            cummax = df["close"].cummax()
            drawdown = (cummax - df["close"]) / cummax
            max_drawdown = drawdown.max()
            scores["max_drawdown"] = (
                float(max_drawdown) if not pd.isna(max_drawdown) else None
            )

        except Exception as e:
            logger.error(f"计算评分失败: {str(e)}")

        return scores

    def _generate_recommendation(
        self, signals: Dict[str, int], scores: Dict[str, float]
    ) -> Tuple[float, str, float]:
        """生成推荐信号"""
        try:
            total_score = sum(v for v in scores.values() if isinstance(v, (int, float)))

            buy_signals = sum(1 for v in signals.values() if v == 1)
            sell_signals = sum(1 for v in signals.values() if v == -1)

            if total_score >= 60 and buy_signals >= 3:
                recommend = "strong_buy"
                confidence = 0.85
            elif total_score >= 45 and buy_signals >= 2:
                recommend = "buy"
                confidence = 0.70
            elif total_score <= 25 and sell_signals >= 3:
                recommend = "strong_sell"
                confidence = 0.85
            elif total_score <= 35 and sell_signals >= 2:
                recommend = "sell"
                confidence = 0.70
            else:
                recommend = "hold"
                confidence = 0.50

            return total_score, recommend, confidence

        except Exception as e:
            logger.error(f"生成推荐失败: {str(e)}")
            return 0, "hold", 0.5

    def _calculate_signal_strength(
        self, signals: Dict[str, int], total_score: float
    ) -> int:
        """计算信号强度"""
        buy_signals = sum(1 for v in signals.values() if v == 1)
        sell_signals = sum(1 for v in signals.values() if v == -1)

        if total_score >= 70 or buy_signals >= 4:
            return 5
        elif total_score >= 55 or buy_signals >= 3:
            return 4
        elif total_score >= 40 or buy_signals >= 2:
            return 3
        elif total_score >= 25:
            return 2
        else:
            return 1


async def sync_selection_signals(db: AsyncSession, limit: int = 500) -> dict:
    """
    同步选股信号数据

    Args:
        db: 数据库会话
        limit: 处理股票数量上限

    Returns:
        dict: 同步结果
    """
    try:
        print("开始生成选股信号...")

        service = SelectionSignalService(db)

        query = (
            select(StockBasicInfo)
            .filter(
                StockBasicInfo.status == "L", StockBasicInfo.trade_status == "交易中"
            )
            .limit(limit)
        )
        result = await db.execute(query)
        stocks = result.scalars().all()

        current_date = date.today()

        delete_stmt = delete(StockSelectionSignal).where(
            StockSelectionSignal.signal_date == current_date
        )
        await db.execute(delete_stmt)

        added_count = 0
        error_count = 0

        for stock in stocks:
            try:
                signal_data = await service.generate_signals_for_stock(
                    stock.stock_code, stock.stock_name
                )

                if signal_data:
                    signal_data["industry"] = stock.industry
                    signal_record = StockSelectionSignal(**signal_data)
                    db.add(signal_record)
                    added_count += 1

            except Exception as e:
                error_count += 1
                if error_count <= 5:
                    print(f"处理股票 {stock.stock_code} 失败: {str(e)}")
                continue

        await db.commit()

        query = (
            select(StockSelectionSignal)
            .filter(StockSelectionSignal.signal_date == current_date)
            .order_by(StockSelectionSignal.total_score.desc())
        )

        result = await db.execute(query)
        signals = result.scalars().all()

        for rank, signal in enumerate(signals, 1):
            signal.score_rank = rank

        await db.commit()

        message = f"成功生成 {added_count} 条选股信号"
        print(message)
        return {"is_success": True, "message": message, "added_count": added_count}

    except Exception as e:
        await db.rollback()
        print(f"同步选股信号失败: {str(e)}")
        return {"is_success": False, "message": str(e)}
