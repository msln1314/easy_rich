import logging
import numpy as np
import pandas as pd
import torch
from typing import List, Dict
from datetime import datetime, timedelta
from transformers import AutoModelForCausalLM, AutoTokenizer

from .stock_service import StockService
from apps.admin.stock.schemas  import (
    PredictionOut, PredictionError,
    PredictionPoint, ConfidenceInterval
)
from apps.admin.stock.params import PredictionParams
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
            tokenizer_path = os.path.join(backend_dir, 'apps', 'module_prediction', 'model', 'Kronos-Tokenizer-base')
            model_path = os.path.join(backend_dir, 'apps', 'module_prediction', 'model', 'Kronos-base')
            logger.info(f"tokenizer_path: {tokenizer_path}")
            logger.info(f"model_path: {model_path}")

            # 检查本地模型是否存在
            if not os.path.exists(tokenizer_path):
                raise FileNotFoundError(f"Tokenizer 模型文件不存在: {tokenizer_path}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"模型文件不存在: {model_path}")

            # 加载 Tokenizer 配置
            tokenizer_config_file = os.path.join(tokenizer_path, 'config.json')
            tokenizer_weight_file = os.path.join(tokenizer_path, 'model.safetensors')

            with open(tokenizer_config_file, 'r') as f:
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
            model_config_file = os.path.join(model_path, 'config.json')
            model_weight_file = os.path.join(model_path, 'model.safetensors')

            with open(model_config_file, 'r') as f:
                model_config = json.load(f)
            logger.info(f"模型配置: {model_config}")

            model = Kronos(**model_config)
            logger.info("模型初始化成功")

            # 加载模型权重
            if os.path.exists(model_weight_file):
                model_state = load_file(model_weight_file)
                model.load_state_dict(model_state, strict=False)
                logger.info("模型权重加载成功")

            self.predictor = KronosPredictor(model, tokenizer, device=self.device, max_context=512)
            self._model_loaded = True
            logger.info("Kronos 模型加载成功")

        except Exception as e:
            logger.error(f"Kronos 模型加载失败: {str(e)}")
            raise PredictionError(f"模型加载失败: {str(e)}")

    async def predict_stock_price(self, request: PredictionParams,historical_data) -> PredictionOut:
        """执行股票价格预测"""
        # historical_data = await self._get_historical_data(request.stock_code, request.historical_days)

        try:
            logger.info(f"开始预测股票 {request.stock_code}，预测天数: {request.prediction_days}，历史数据天数: {request.historical_days}")

            await self.load_model()
     
            # 转换为 DataFrame
            df = pd.DataFrame(historical_data)
            df['timestamps'] = pd.to_datetime(df['date'])
            x_df = df[['open', 'high', 'low', 'close']].copy()
            x_ts = df['timestamps']

            # 构造预测时间戳
            last_date = x_ts.iloc[-1]
            y_dates = []
            while len(y_dates) < request.prediction_days:
                last_date += timedelta(days=1)
                if last_date.weekday() < 5:  # 跳过周末
                    y_dates.append(last_date)
            y_ts = pd.Series(y_dates)

            # 使用 Kronos 预测
            logger.info(f"开始模型推理，输入数据形状: {x_df.shape}, 预测步数: {request.prediction_days}")
            pred_df = self.predictor.predict(
                df=x_df,
                x_timestamp=x_ts,
                y_timestamp=y_ts,
                pred_len=request.prediction_days,
                T=1.0,
                top_p=0.9,
                sample_count=1
            )
            logger.info(f"预测完成，输出数据形状: {pred_df.shape}")

            # 格式化预测结果
            prediction_points = []
            for date, row in pred_df.iterrows():
                prediction_points.append(
                    PredictionPoint(
                        date=date.strftime('%Y-%m-%d'),
                        predicted_close=round(float(row['close']), 2)
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
                        upper_bound=point.predicted_close + margin
                    )
                )

            return PredictionOut(
                stock_code=request.stock_code,
                prediction_days=request.prediction_days,
                predictions=prediction_points,
                confidence_intervals=confidence_intervals,
                historical_data_count=len(historical_data),
                historical_data=historical_data
            )

        except Exception as e:
            logger.error(f"预测服务错误: {str(e)}")
            raise PredictionError(f"预测服务错误: {str(e)}")

    async def _get_historical_data(self, stock_code: str, historical_days: int = 100) -> List[Dict]:
        """获取历史股票数据"""
        end_date = datetime.now()
        # 为了确保获取到足够的交易日数据，我们获取更多天数（考虑周末和节假日）
        calendar_days = int(historical_days * 1.5)  # 增加50%的缓冲
        start_date = end_date - timedelta(days=calendar_days)
        
        result = await self.stock_service.get_historical_data(
            stock_code,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        if not result or not result.get('data'):
            raise PredictionError(f"股票 {stock_code} 没有可用的历史数据")
        
        # 取最近的指定天数的数据
        data = result['data']
        if len(data) > historical_days:
            data = data[-historical_days:]
        
        logger.info(f"获取到 {len(data)} 天的历史数据用于预测")
        return data
