import logging
import numpy as np
import pandas as pd
import torch
from typing import List, Dict
from datetime import datetime, timedelta

from .stock_service import StockService
from apps.admin.stock.schemas import (
    PredictionOut,
    PredictionError,
    PredictionPoint,
    ConfidenceInterval,
)
from apps.admin.stock.params import PredictionParams
from apps.admin.stock.services.gm_service import gm_service
import os
import json

from apps.module_prediction.model import Kronos, KronosTokenizer, KronosPredictor
from safetensors.torch import load_file

logger = logging.getLogger(__name__)


class PredictionService:
    """使用 Kronos-small 模型的股票价格预测服务"""

    def __init__(self):
        self.stock_service = StockService()
        self.predictor = None
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self._model_loaded = False
        print(f"Using device: {self.device}")

    async def load_model(self):
        """加载 Kronos-base 模型（本地离线模型）"""
        if self._model_loaded:
            return

        try:
            logger.info("正在加载 Kronos 模型: 本地离线模型")
            # 获取 backend 目录
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            tokenizer_path = os.path.join(
                backend_dir,
                "apps",
                "module_prediction",
                "model",
                "Kronos-Tokenizer-base",
            )
            model_path = os.path.join(
                backend_dir, "apps", "module_prediction", "model", "Kronos-base"
            )
            logger.info(f"tokenizer_path: {tokenizer_path}")
            logger.info(f"model_path: {model_path}")

            # 检查本地模型是否存在
            if not os.path.exists(tokenizer_path):
                raise FileNotFoundError(f"Tokenizer 模型文件不存在: {tokenizer_path}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"模型文件不存在: {model_path}")

            # 加载 Tokenizer 配置
            tokenizer_config_file = os.path.join(tokenizer_path, "config.json")
            tokenizer_weight_file = os.path.join(tokenizer_path, "model.safetensors")

            with open(tokenizer_config_file, "r") as f:
                tokenizer_config = json.load(f)
            logger.info(f"Tokenizer 配置: {tokenizer_config}")

            tokenizer = KronosTokenizer(**tokenizer_config)
            logger.info("Tokenizer 初始化成功")

            # 加载 Tokenizer 权重
            if os.path.exists(tokenizer_weight_file):
                tokenizer_state = load_file(tokenizer_weight_file)
                tokenizer.load_state_dict(tokenizer_state, strict=False)
                logger.info("Tokenizer 权重加载成功")

            # 加载模型配置
            model_config_file = os.path.join(model_path, "config.json")
            model_weight_file = os.path.join(model_path, "model.safetensors")

            with open(model_config_file, "r") as f:
                model_config = json.load(f)
            logger.info(f"模型配置: {model_config}")

            model = Kronos(**model_config)
            logger.info("模型初始化成功")

            # 加载模型权重
            if os.path.exists(model_weight_file):
                model_state = load_file(model_weight_file)
                model.load_state_dict(model_state, strict=False)
                logger.info("模型权重加载成功")

            self.predictor = KronosPredictor(
                model, tokenizer, device=self.device, max_context=512
            )
            self._model_loaded = True
            logger.info("Kronos 模型加载成功")

        except Exception as e:
            logger.error(f"Kronos 模型加载失败: {str(e)}")
            raise PredictionError(f"模型加载失败: {str(e)}")

    async def predict_stock_price(
        self, request: PredictionParams, historical_data
    ) -> PredictionOut:
        """执行股票价格预测"""
        # historical_data = await self._get_historical_data(request.stock_code, request.historical_days)

        try:
            logger.info(
                f"开始预测股票 {request.stock_code}，预测天数: {request.prediction_days}，历史数据天数: {request.historical_days}"
            )

            await self.load_model()

            # 转换为 DataFrame
            df = pd.DataFrame(historical_data)
            df["timestamps"] = pd.to_datetime(df["date"])
            x_df = df[["open", "high", "low", "close"]].copy()
            x_ts = df["timestamps"]

            # 构造预测时间戳
            last_date = x_ts.iloc[-1]
            y_dates = []
            while len(y_dates) < request.prediction_days:
                last_date += timedelta(days=1)
                if last_date.weekday() < 5:  # 跳过周末
                    y_dates.append(last_date)
            y_ts = pd.Series(y_dates)

            # 使用 Kronos 预测
            logger.info(
                f"开始模型推理，输入数据形状: {x_df.shape}, 预测步数: {request.prediction_days}"
            )
            pred_df = self.predictor.predict(
                df=x_df,
                x_timestamp=x_ts,
                y_timestamp=y_ts,
                pred_len=request.prediction_days,
                T=1.0,
                top_p=0.9,
                sample_count=1,
            )
            logger.info(f"预测完成，输出数据形状: {pred_df.shape}")

            # 格式化预测结果
            prediction_points = []
            for date, row in pred_df.iterrows():
                prediction_points.append(
                    PredictionPoint(
                        date=date.strftime("%Y-%m-%d"),
                        predicted_close=round(float(row["close"]), 2),
                    )
                )

            # 置信区间（仍用启发式，5% 起步，每天+2%）
            confidence_intervals = []
            for i, point in enumerate(prediction_points):
                factor = 0.05 + i * 0.02
                margin = point.predicted_close * factor
                confidence_intervals.append(
                    ConfidenceInterval(
                        date=point.date,
                        lower_bound=max(0, point.predicted_close - margin),
                        upper_bound=point.predicted_close + margin,
                    )
                )

            return PredictionOut(
                stock_code=request.stock_code,
                prediction_days=request.prediction_days,
                predictions=prediction_points,
                confidence_intervals=confidence_intervals,
                historical_data_count=len(historical_data),
                historical_data=historical_data,
            )

        except Exception as e:
            logger.error(f"预测服务错误: {str(e)}")
            raise PredictionError(f"预测服务错误: {str(e)}")

    async def _get_historical_data(
        self, stock_code: str, historical_days: int = 100
    ) -> List[Dict]:
        """获取历史股票数据（主数据源: akshare, 备用数据源: 掘金量化）"""
        import asyncio
        import random

        end_date = datetime.now()
        calendar_days = int(historical_days * 1.5)
        start_date = end_date - timedelta(days=calendar_days)

        max_retries = 3
        last_error = None

        for attempt in range(max_retries):
            try:
                result = await self.stock_service.get_historical_data(
                    stock_code,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                )
                if not result or not result.get("data"):
                    raise PredictionError(f"股票 {stock_code} 没有可用的历史数据")

                data = result["data"]
                if len(data) > historical_days:
                    data = data[-historical_days:]

                logger.info(f"[akshare] 获取到 {len(data)} 天的历史数据用于预测")
                return data

            except Exception as e:
                last_error = e
                logger.warning(
                    f"[akshare] 获取历史数据失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}"
                )
                if attempt < max_retries - 1:
                    wait_time = (2**attempt) + random.uniform(0, 1)
                    logger.info(f"等待 {wait_time:.1f} 秒后重试...")
                    await asyncio.sleep(wait_time)

        logger.warning(f"[akshare] 所有重试失败，尝试使用掘金量化作为备用数据源...")

        try:
            data = await self._get_historical_data_from_gm(
                stock_code, start_date, end_date, historical_days
            )
            if data:
                logger.info(f"[掘金量化] 获取到 {len(data)} 天的历史数据用于预测")
                return data
        except Exception as gm_error:
            logger.error(f"[掘金量化] 获取历史数据失败: {str(gm_error)}")
            last_error = gm_error

        raise PredictionError(
            f"获取历史数据失败 (akshare 和 掘金量化 均不可用): {str(last_error)}"
        )

    async def _get_historical_data_from_gm(
        self,
        stock_code: str,
        start_date: datetime,
        end_date: datetime,
        historical_days: int,
    ) -> List[Dict]:
        """从掘金量化获取历史数据"""
        if not gm_service.is_available():
            logger.warning("[掘金量化] 服务不可用")
            return None

        gm_symbol = self._convert_to_gm_symbol(stock_code)
        if not gm_symbol:
            logger.warning(f"[掘金量化] 无法转换股票代码: {stock_code}")
            return None

        logger.info(f"[掘金量化] 尝试获取 {gm_symbol} 历史数据...")

        try:
            import asyncio

            history_data = await asyncio.to_thread(
                gm_service.gm.history,
                symbol=gm_symbol,
                frequency="1d",
                start_time=start_date.strftime("%Y-%m-%d %H:%M:%S"),
                end_time=end_date.strftime("%Y-%m-%d %H:%M:%S"),
                adjust=0,
                df=True,
            )

            if history_data is None or history_data.empty:
                logger.warning(f"[掘金量化] 未获取到数据")
                return None

            data = self._convert_gm_to_standard_format(history_data)
            if len(data) > historical_days:
                data = data[-historical_days:]

            return data

        except Exception as e:
            logger.error(f"[掘金量化] 获取历史数据异常: {str(e)}")
            return None

    def _convert_to_gm_symbol(self, stock_code: str) -> str:
        """将股票代码转换为掘金量化格式 (如: SHSE.600000, SZSE.000001)"""
        code = stock_code.replace("sz.", "").replace("sh.", "").replace("bj.", "")

        if code.startswith(("60", "68")):
            return f"SHSE.{code}"
        elif code.startswith(("00", "30")):
            return f"SZSE.{code}"
        elif code.startswith(("43", "83", "87", "88", "920")):
            return f"BJSE.{code}"
        else:
            return None

    def _convert_gm_to_standard_format(self, df: pd.DataFrame) -> List[Dict]:
        """将掘金量化数据转换为标准格式"""
        result = []
        for _, row in df.iterrows():
            item = {
                "date": row.get("eob", row.get("bob", "")).strftime("%Y-%m-%d")
                if pd.notna(row.get("eob", row.get("bob")))
                else "",
                "open": float(row.get("open", 0)) if pd.notna(row.get("open")) else 0.0,
                "high": float(row.get("high", 0)) if pd.notna(row.get("high")) else 0.0,
                "low": float(row.get("low", 0)) if pd.notna(row.get("low")) else 0.0,
                "close": float(row.get("close", 0))
                if pd.notna(row.get("close"))
                else 0.0,
                "volume": int(row.get("volume", 0))
                if pd.notna(row.get("volume"))
                else 0,
                "amount": float(row.get("amount", 0))
                if pd.notna(row.get("amount"))
                else 0.0,
                "data_source": "gm",
            }
            result.append(item)
        return result
