"""Tushare（Tushare Pro）数据服务模块

本模块提供与 Tushare Pro 平台的对接服务，作为 akshare 和 gm 的备用数据源。
主要功能：
1. 提供与 akshare 兼容的接口
2. 统一的数据返回格式
3. 自动降级机制：当 akshare 和 gm 都失败时使用 Tushare 获取数据
"""

import logging
import pandas as pd
import math
from datetime import datetime
from typing import List, Optional, Dict, Any

from app.models.sector_models import (
    ConceptBoard,
    IndustryBoard,
    BoardSpot,
    ConceptBoardSpot,
    IndustryBoardSpot,
    ConceptBoardConstituent,
    IndustryBoardConstituent,
)
from app.models.stock_models import StockInfo, StockQuote
from app.core.logging import get_logger

logger = get_logger(__name__)


def safe_float(value, default=None):
    if value is None or pd.isna(value):
        return default
    try:
        float_value = float(value)
        if math.isnan(float_value) or math.isinf(float_value):
            return default
        return float_value
    except (ValueError, TypeError):
        return default


class TushareService:
    """Tushare Pro 数据服务"""

    def __init__(self, token: Optional[str] = None):
        """
        初始化 Tushare 服务

        Args:
            token: Tushare Pro API token，如果不提供则从配置文件读取
        """
        self.enabled = False
        self.ts = None
        self._init_tushare(token)

    def _init_tushare(self, token: Optional[str] = None):
        """初始化 Tushare Pro 连接"""
        try:
            import tushare as ts

            self.ts = ts

            # 获取 token
            if not token:
                from app.core.config import settings

                token = settings.TUSHARE_TOKEN

            if not token:
                logger.warning("Tushare Pro token 未配置，Tushare 服务将不可用")
                self.enabled = False
                return

            # 设置 token
            ts.set_token(token)
            self.pro = ts.pro_api()
            self.enabled = True
            logger.info("Tushare Pro SDK 初始化成功")
        except ImportError:
            logger.warning("Tushare Pro SDK 未安装，Tushare 服务将不可用")
            self.enabled = False
        except PermissionError as e:
            logger.error(f"Tushare Pro SDK 初始化失败（权限错误）: {str(e)}")
            logger.warning("请检查 Tushare SDK 的临时文件目录权限，或以管理员权限运行")
            self.enabled = False
        except Exception as e:
            logger.error(f"Tushare Pro SDK 初始化失败: {str(e)}")
            self.enabled = False

    def is_available(self) -> bool:
        """检查 Tushare 服务是否可用"""
        return self.enabled

    def _calc_change_percent(self, current: float, pre_close: float) -> float:
        """计算涨跌幅"""
        if pre_close and pre_close != 0:
            return round((current - pre_close) / pre_close * 100, 2)
        return 0.0

    def _calc_amplitude(self, quote: Dict) -> float:
        """计算振幅"""
        high = quote.get("high", 0)
        low = quote.get("low", 0)
        pre_close = quote.get("pre_close", 0)
        if pre_close and pre_close != 0:
            return round((high - low) / pre_close * 100, 2)
        return 0.0

    # 概念板块相关接口

    async def get_concept_boards(self) -> List[ConceptBoard]:
        """
        获取概念板块列表（Tushare 版本）

        Returns:
            List[ConceptBoard]: 概念板块列表
        """
        if not self.is_available():
            logger.warning("Tushare 服务不可用，无法获取概念板块")
            raise ValueError("Tushare 服务不可用")

        logger.info("使用 Tushare 获取概念板块列表")

        try:
            df = self.pro.concept(src="ts")

            if df is None or df.empty:
                logger.warning("Tushare 未返回概念板块数据")
                return []

            result = []
            for _, row in df.iterrows():
                board = ConceptBoard(
                    code=str(row.get("code", "")),
                    name=str(row.get("name", "")),
                    change_percent=safe_float(row.get("change")) or 0,
                    change=safe_float(row.get("change")) or 0,
                    price=safe_float(row.get("close")) or 0,
                    up_count=0,
                    down_count=0,
                    update_time=datetime.now(),
                )
                result.append(board)

            logger.info(f"Tushare 获取到 {len(result)} 个概念板块")
            return result

        except Exception as e:
            logger.error(f"Tushare 获取概念板块失败: {str(e)}")
            raise ValueError(f"Tushare 获取概念板块失败: {str(e)}")

    async def get_industry_boards(self) -> List[IndustryBoard]:
        """
        获取行业板块列表（Tushare 版本）

        Returns:
            List[IndustryBoard]: 行业板块列表
        """
        if not self.is_available():
            logger.warning("Tushare 服务不可用，无法获取行业板块")
            raise ValueError("Tushare 服务不可用")

        logger.info("使用 Tushare 获取行业板块列表")

        try:
            df = self.pro.index_classify(level="L1", src="TS")

            if df is None or df.empty:
                logger.warning("Tushare 未返回行业板块数据")
                return []

            result = []
            for _, row in df.iterrows():
                board = IndustryBoard(
                    code=str(row.get("index_code", "")),
                    name=str(row.get("industry_name", "")),
                    change_percent=safe_float(row.get("change")) or 0,
                    change=safe_float(row.get("change")) or 0,
                    price=safe_float(row.get("close")) or 0,
                    up_count=0,
                    down_count=0,
                    update_time=datetime.now(),
                )
                result.append(board)

            logger.info(f"Tushare 获取到 {len(result)} 个行业板块")
            return result

        except Exception as e:
            logger.error(f"Tushare 获取行业板块失败: {str(e)}")
            raise ValueError(f"Tushare 获取行业板块失败: {str(e)}")


# 创建全局 Tushare 服务实例
tushare_service = TushareService()
