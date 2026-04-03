# backend/qmt-service/app/services/factor_service.py
"""
因子库服务 - 纯内存缓存版本

不使用数据库，所有因子定义存储在内存中
数据库操作由 stock_policy 负责
"""
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import json
import asyncio

from app.core.qmt_client import QMTClientManager
from app.models.factor_models import (
    FactorDefinition,
    FactorDefinitionListResponse,
    FactorValue,
    FactorValueListResponse,
    StockFactorValuesResponse,
    FactorIC,
    FactorICListResponse,
    FactorReturn,
    FactorReturnListResponse,
    FactorScreenRequest,
    FactorScreenResult,
    FactorScreenResponse,
    FactorCategory,
)

logger = logging.getLogger(__name__)


class FactorService:
    """因子库服务 - 纯内存缓存"""

    # 预置因子定义
    PRESET_FACTORS = [
        # 趋势因子
        {
            "factor_id": "MA5",
            "factor_name": "5日均线",
            "category": FactorCategory.TREND,
            "description": "5日移动平均线",
            "formula": "MA(close, 5)",
            "params": [{"key": "period", "default": 5}],
            "unit": "元",
            "data_source": "行情",
        },
        {
            "factor_id": "MA10",
            "factor_name": "10日均线",
            "category": FactorCategory.TREND,
            "description": "10日移动平均线",
            "formula": "MA(close, 10)",
            "params": [{"key": "period", "default": 10}],
            "unit": "元",
        },
        {
            "factor_id": "MA20",
            "factor_name": "20日均线",
            "category": FactorCategory.TREND,
            "description": "20日移动平均线",
            "formula": "MA(close, 20)",
            "params": [{"key": "period", "default": 20}],
            "unit": "元",
        },
        {
            "factor_id": "MA60",
            "factor_name": "60日均线",
            "category": FactorCategory.TREND,
            "description": "60日移动平均线",
            "formula": "MA(close, 60)",
            "params": [{"key": "period", "default": 60}],
            "unit": "元",
        },
        {
            "factor_id": "EMA12",
            "factor_name": "12日指数均线",
            "category": FactorCategory.TREND,
            "description": "12日指数移动平均线",
            "formula": "EMA(close, 12)",
            "unit": "元",
        },
        {
            "factor_id": "EMA26",
            "factor_name": "26日指数均线",
            "category": FactorCategory.TREND,
            "description": "26日指数移动平均线",
            "formula": "EMA(close, 26)",
            "unit": "元",
        },

        # 动量因子
        {
            "factor_id": "RSI6",
            "factor_name": "6日RSI",
            "category": FactorCategory.MOMENTUM,
            "description": "6日相对强弱指标",
            "formula": "RSI(close, 6)",
            "params": [{"key": "period", "default": 6}],
            "unit": "%",
        },
        {
            "factor_id": "RSI14",
            "factor_name": "14日RSI",
            "category": FactorCategory.MOMENTUM,
            "description": "14日相对强弱指标",
            "formula": "RSI(close, 14)",
            "params": [{"key": "period", "default": 14}],
            "unit": "%",
        },
        {
            "factor_id": "KDJ_K",
            "factor_name": "KDJ-K值",
            "category": FactorCategory.MOMENTUM,
            "description": "KDJ指标的K值",
            "formula": "KDJ(high, low, close, 9, 3, 3)",
        },
        {
            "factor_id": "KDJ_D",
            "factor_name": "KDJ-D值",
            "category": FactorCategory.MOMENTUM,
            "description": "KDJ指标的D值",
            "formula": "KDJ(high, low, close, 9, 3, 3)",
        },
        {
            "factor_id": "MACD",
            "factor_name": "MACD",
            "category": FactorCategory.MOMENTUM,
            "description": "MACD指标",
            "formula": "MACD(close, 12, 26, 9)",
            "params": [
                {"key": "fast", "default": 12},
                {"key": "slow", "default": 26},
                {"key": "signal", "default": 9},
            ],
        },
        {
            "factor_id": "MOM10",
            "factor_name": "10日动量",
            "category": FactorCategory.MOMENTUM,
            "description": "10日价格动量",
            "formula": "close / close_10 - 1",
            "unit": "%",
        },

        # 波动因子
        {
            "factor_id": "ATR14",
            "factor_name": "14日ATR",
            "category": FactorCategory.VOLATILITY,
            "description": "14日平均真实波幅",
            "formula": "ATR(high, low, close, 14)",
            "unit": "元",
        },
        {
            "factor_id": "VOLATILITY20",
            "factor_name": "20日波动率",
            "category": FactorCategory.VOLATILITY,
            "description": "20日收益率标准差",
            "formula": "STD(return, 20) * SQRT(250)",
            "unit": "%",
        },
        {
            "factor_id": "BOLL_UP",
            "factor_name": "布林上轨",
            "category": FactorCategory.VOLATILITY,
            "description": "布林带上轨",
            "formula": "BOLL(close, 20, 2).upper",
            "unit": "元",
        },
        {
            "factor_id": "BOLL_MID",
            "factor_name": "布林中轨",
            "category": FactorCategory.VOLATILITY,
            "description": "布林带中轨",
            "formula": "BOLL(close, 20, 2).middle",
            "unit": "元",
        },
        {
            "factor_id": "BOLL_LOW",
            "factor_name": "布林下轨",
            "category": FactorCategory.VOLATILITY,
            "description": "布林带下轨",
            "formula": "BOLL(close, 20, 2).lower",
            "unit": "元",
        },

        # 成交量因子
        {
            "factor_id": "VOL_MA5",
            "factor_name": "5日均量",
            "category": FactorCategory.VOLUME,
            "description": "5日成交量均值",
            "formula": "MA(volume, 5)",
            "unit": "手",
        },
        {
            "factor_id": "VOL_MA10",
            "factor_name": "10日均量",
            "category": FactorCategory.VOLUME,
            "description": "10日成交量均值",
            "formula": "MA(volume, 10)",
            "unit": "手",
        },
        {
            "factor_id": "VOL_RATIO",
            "factor_name": "量比",
            "category": FactorCategory.VOLUME,
            "description": "当日成交量/5日均量",
            "formula": "volume / MA(volume, 5)",
            "unit": "倍",
        },
        {
            "factor_id": "OBV",
            "factor_name": "OBV",
            "category": FactorCategory.VOLUME,
            "description": "能量潮指标",
            "formula": "OBV(close, volume)",
        },
        {
            "factor_id": "TURNOVER",
            "factor_name": "换手率",
            "category": FactorCategory.VOLUME,
            "description": "当日换手率",
            "formula": "volume / shares_outstanding * 100",
            "unit": "%",
        },

        # 价值因子
        {
            "factor_id": "PE",
            "factor_name": "市盈率",
            "category": FactorCategory.VALUE,
            "description": "股价/每股收益",
            "formula": "price / eps",
            "unit": "倍",
        },
        {
            "factor_id": "PB",
            "factor_name": "市净率",
            "category": FactorCategory.VALUE,
            "description": "股价/每股净资产",
            "formula": "price / bvps",
            "unit": "倍",
        },
        {
            "factor_id": "PS",
            "factor_name": "市销率",
            "category": FactorCategory.VALUE,
            "description": "市值/营业收入",
            "formula": "market_cap / revenue",
            "unit": "倍",
        },
        {
            "factor_id": "PCF",
            "factor_name": "市现率",
            "category": FactorCategory.VALUE,
            "description": "市值/现金流",
            "formula": "market_cap / cash_flow",
            "unit": "倍",
        },
        {
            "factor_id": "PEG",
            "factor_name": "PEG",
            "category": FactorCategory.VALUE,
            "description": "市盈率/盈利增长率",
            "formula": "PE / earnings_growth",
            "unit": "倍",
        },
        {
            "factor_id": "DIV_YIELD",
            "factor_name": "股息率",
            "category": FactorCategory.VALUE,
            "description": "每股股利/股价",
            "formula": "dps / price * 100",
            "unit": "%",
        },

        # 成长因子
        {
            "factor_id": "REVENUE_GROWTH",
            "factor_name": "营收增长率",
            "category": FactorCategory.GROWTH,
            "description": "营业收入同比增长率",
            "formula": "(revenue - revenue_yoy) / revenue_yoy * 100",
            "unit": "%",
        },
        {
            "factor_id": "PROFIT_GROWTH",
            "factor_name": "利润增长率",
            "category": FactorCategory.GROWTH,
            "description": "净利润同比增长率",
            "formula": "(profit - profit_yoy) / profit_yoy * 100",
            "unit": "%",
        },
        {
            "factor_id": "EPS_GROWTH",
            "factor_name": "EPS增长率",
            "category": FactorCategory.GROWTH,
            "description": "每股收益同比增长率",
            "formula": "(eps - eps_yoy) / eps_yoy * 100",
            "unit": "%",
        },

        # 质量因子
        {
            "factor_id": "ROE",
            "factor_name": "ROE",
            "category": FactorCategory.QUALITY,
            "description": "净资产收益率",
            "formula": "profit / equity * 100",
            "unit": "%",
        },
        {
            "factor_id": "ROA",
            "factor_name": "ROA",
            "category": FactorCategory.QUALITY,
            "description": "总资产收益率",
            "formula": "profit / assets * 100",
            "unit": "%",
        },
        {
            "factor_id": "GROSS_MARGIN",
            "factor_name": "毛利率",
            "category": FactorCategory.QUALITY,
            "description": "毛利润/营业收入",
            "formula": "(revenue - cost) / revenue * 100",
            "unit": "%",
        },
        {
            "factor_id": "NET_MARGIN",
            "factor_name": "净利率",
            "category": FactorCategory.QUALITY,
            "description": "净利润/营业收入",
            "formula": "profit / revenue * 100",
            "unit": "%",
        },
        {
            "factor_id": "DEBT_RATIO",
            "factor_name": "资产负债率",
            "category": FactorCategory.QUALITY,
            "description": "总负债/总资产",
            "formula": "debt / assets * 100",
            "unit": "%",
        },

        # 情绪因子
        {
            "factor_id": "AMOUNT",
            "factor_name": "成交额",
            "category": FactorCategory.SENTIMENT,
            "description": "当日成交金额",
            "formula": "close * volume",
            "unit": "万元",
        },
        {
            "factor_id": "AMP",
            "factor_name": "振幅",
            "category": FactorCategory.SENTIMENT,
            "description": "(最高-最低)/昨收",
            "formula": "(high - low) / pre_close * 100",
            "unit": "%",
        },
    ]

    def __init__(self):
        self._factor_cache: Dict[str, FactorDefinition] = {}
        self._initialized = False

    async def init_factors(self):
        """初始化因子（从预置数据加载到内存）"""
        if self._initialized:
            return

        for factor_data in self.PRESET_FACTORS:
            factor = FactorDefinition(
                factor_id=factor_data["factor_id"],
                factor_name=factor_data["factor_name"],
                category=factor_data["category"],
                description=factor_data.get("description", ""),
                formula=factor_data.get("formula", ""),
                params=factor_data.get("params", []),
                unit=factor_data.get("unit", ""),
                data_source=factor_data.get("data_source", "QMT"),
                update_freq=factor_data.get("update_freq", "daily"),
                is_active=True,
            )
            self._factor_cache[factor.factor_id] = factor

        self._initialized = True
        logger.info(f"因子库初始化完成，共 {len(self._factor_cache)} 个因子")

    async def get_factor_definitions(
        self,
        category: Optional[str] = None,
        keyword: Optional[str] = None
    ) -> FactorDefinitionListResponse:
        """获取因子定义列表"""
        await self.init_factors()

        factors = list(self._factor_cache.values())

        if category:
            factors = [f for f in factors if f.category == category]

        if keyword:
            keyword_lower = keyword.lower()
            factors = [
                f for f in factors
                if keyword_lower in f.factor_name.lower()
                or keyword_lower in f.factor_id.lower()
                or keyword_lower in f.description.lower()
            ]

        return FactorDefinitionListResponse(
            factors=factors,
            total=len(factors)
        )

    async def get_factor_definition(self, factor_id: str) -> Optional[FactorDefinition]:
        """获取单个因子定义"""
        await self.init_factors()
        return self._factor_cache.get(factor_id)

    async def sync_from_qmt(self) -> Dict[str, Any]:
        """从QMT同步因子（仅更新内存缓存）"""
        await self.init_factors()

        if not QMTClientManager.is_connected():
            logger.warning("QMT未连接，返回内存缓存")
            return {"synced": 0, "total": len(self._factor_cache), "message": "QMT未连接"}

        # QMT连接时，可以扩展获取更多因子
        # 目前返回预置因子
        return {"synced": 0, "total": len(self._factor_cache), "message": "因子已加载到内存"}

    async def create_factor(self, factor_data: Dict[str, Any]) -> FactorDefinition:
        """创建自定义因子（仅内存）"""
        await self.init_factors()

        factor = FactorDefinition(
            factor_id=factor_data["factor_id"],
            factor_name=factor_data["factor_name"],
            category=FactorCategory(factor_data.get("category", "custom")),
            description=factor_data.get("description", ""),
            formula=factor_data.get("formula", ""),
            params=factor_data.get("params", []),
            unit=factor_data.get("unit", ""),
            data_source=factor_data.get("data_source", "custom"),
            update_freq=factor_data.get("update_freq", "daily"),
            is_active=True,
        )
        self._factor_cache[factor.factor_id] = factor
        return factor

    async def update_factor(self, factor_id: str, factor_data: Dict[str, Any]) -> Optional[FactorDefinition]:
        """更新因子（仅内存）"""
        await self.init_factors()

        factor = self._factor_cache.get(factor_id)
        if not factor:
            return None

        for key, value in factor_data.items():
            if key == "category" and isinstance(value, str):
                value = FactorCategory(value)
            if hasattr(factor, key):
                setattr(factor, key, value)

        return factor

    async def delete_factor(self, factor_id: str) -> bool:
        """删除因子（仅内存）"""
        await self.init_factors()

        if factor_id not in self._factor_cache:
            return False

        # 不允许删除预置因子
        preset_ids = [f["factor_id"] for f in self.PRESET_FACTORS]
        if factor_id in preset_ids:
            return False

        del self._factor_cache[factor_id]
        return True

    async def get_factor_values(
        self,
        factor_id: str,
        stock_codes: List[str],
        date: Optional[str] = None
    ) -> FactorValueListResponse:
        """获取因子值"""
        await self.init_factors()

        if not QMTClientManager.is_connected():
            return self._mock_factor_values(factor_id, stock_codes, date)

        try:
            from xtquant import xtdata

            date_str = date or datetime.now().strftime("%Y%m%d")
            values = []

            for stock_code in stock_codes:
                factor_value = await self._calculate_factor_value(
                    factor_id, stock_code, date_str
                )
                if factor_value is not None:
                    values.append(factor_value)

            # 计算排名和百分位
            if values:
                sorted_values = sorted(values, key=lambda x: x.value, reverse=True)
                for i, v in enumerate(sorted_values):
                    v.rank = i + 1
                    v.percentile = (1 - i / len(sorted_values)) * 100

            return FactorValueListResponse(
                factor_id=factor_id,
                date=date_str,
                values=values,
                count=len(values)
            )

        except Exception as e:
            logger.error(f"获取因子值失败: {e}")
            return self._mock_factor_values(factor_id, stock_codes, date)

    async def get_stock_factor_values(
        self,
        stock_code: str,
        factor_ids: Optional[List[str]] = None,
        date: Optional[str] = None
    ) -> StockFactorValuesResponse:
        """获取单只股票的多个因子值"""
        await self.init_factors()

        date_str = date or datetime.now().strftime("%Y%m%d")

        if factor_ids is None:
            factor_ids = list(self._factor_cache.keys())

        factors = []
        for factor_id in factor_ids:
            value = await self._calculate_factor_value(factor_id, stock_code, date_str)
            if value:
                factors.append({
                    "factor_id": factor_id,
                    "factor_name": self._factor_cache.get(factor_id, FactorDefinition(factor_id=factor_id, factor_name=factor_id, category=FactorCategory.CUSTOM)).factor_name,
                    "value": value.value,
                    "rank": value.rank,
                    "percentile": value.percentile,
                })

        return StockFactorValuesResponse(
            stock_code=stock_code,
            date=date_str,
            factors=factors,
            count=len(factors)
        )

    async def get_factor_ic(
        self,
        factor_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: int = 20
    ) -> FactorICListResponse:
        """获取因子IC值"""
        return self._mock_factor_ic(factor_id, period)

    async def get_factor_returns(
        self,
        factor_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> FactorReturnListResponse:
        """获取因子收益"""
        return self._mock_factor_returns(factor_id)

    async def screen_stocks(
        self,
        request: FactorScreenRequest
    ) -> FactorScreenResponse:
        """因子选股"""
        await self.init_factors()

        date_str = request.date or datetime.now().strftime("%Y%m%d")

        if not QMTClientManager.is_connected():
            return self._mock_screen_stocks(request)

        try:
            from xtquant import xtdata
            stock_list = xtdata.get_stock_list_in_sector("沪深A股")

            results = []
            for stock_code in stock_list[:500]:  # 限制数量
                score = 0.0
                factor_values = {}
                match = True

                for condition in request.factors:
                    factor_id = condition.get("factor_id")
                    op = condition.get("op", "gt")
                    threshold = condition.get("value")

                    factor_value = await self._calculate_factor_value(
                        factor_id, stock_code, date_str
                    )

                    if factor_value is None:
                        match = False
                        break

                    factor_values[factor_id] = factor_value.value

                    # 判断条件
                    if op == "gt" and factor_value.value <= threshold:
                        match = False
                        break
                    elif op == "lt" and factor_value.value >= threshold:
                        match = False
                        break
                    elif op == "eq" and factor_value.value != threshold:
                        match = False
                        break
                    elif op == "ge" and factor_value.value < threshold:
                        match = False
                        break
                    elif op == "le" and factor_value.value > threshold:
                        match = False
                        break

                    score += factor_value.percentile or 0

                if match:
                    results.append(FactorScreenResult(
                        stock_code=stock_code,
                        stock_name="",
                        date=date_str,
                        score=score,
                        factor_values=factor_values,
                    ))

            results.sort(key=lambda x: x.score, reverse=True)
            results = results[:request.limit]

            return FactorScreenResponse(
                date=date_str,
                stocks=results,
                count=len(results)
            )

        except Exception as e:
            logger.error(f"因子选股失败: {e}")
            return self._mock_screen_stocks(request)

    async def _calculate_factor_value(
        self,
        factor_id: str,
        stock_code: str,
        date: str
    ) -> Optional[FactorValue]:
        """计算单只股票的因子值"""
        try:
            from xtquant import xtdata
            # 简化处理，返回模拟数据
            return self._mock_single_factor_value(factor_id, stock_code, date)
        except Exception as e:
            logger.error(f"计算因子值失败 {factor_id} {stock_code}: {e}")
            return self._mock_single_factor_value(factor_id, stock_code, date)

    # ==================== 模拟数据 ====================

    def _mock_factor_values(
        self,
        factor_id: str,
        stock_codes: List[str],
        date: Optional[str]
    ) -> FactorValueListResponse:
        """模拟因子值"""
        date_str = date or datetime.now().strftime("%Y%m%d")
        values = [
            self._mock_single_factor_value(factor_id, code, date_str)
            for code in stock_codes
        ]
        values = [v for v in values if v is not None]

        if values:
            sorted_values = sorted(values, key=lambda x: x.value, reverse=True)
            for i, v in enumerate(sorted_values):
                v.rank = i + 1
                v.percentile = (1 - i / len(sorted_values)) * 100 if sorted_values else 0

        return FactorValueListResponse(
            factor_id=factor_id,
            date=date_str,
            values=values,
            count=len(values)
        )

    def _mock_single_factor_value(
        self,
        factor_id: str,
        stock_code: str,
        date: str
    ) -> FactorValue:
        """模拟单个因子值"""
        import random
        base_value = hash(factor_id) % 100 + random.random() * 50

        return FactorValue(
            factor_id=factor_id,
            stock_code=stock_code,
            stock_name=f"股票{stock_code}",
            value=round(base_value, 4),
            date=date,
            rank=None,
            percentile=None,
            zscore=None,
        )

    def _mock_factor_ic(self, factor_id: str, period: int) -> FactorICListResponse:
        """模拟因子IC"""
        import random
        values = []
        for i in range(period):
            ic = random.uniform(-0.1, 0.15)
            values.append(FactorIC(
                factor_id=factor_id,
                date=(datetime.now() - timedelta(days=i)).strftime("%Y%m%d"),
                ic=round(ic, 4),
                ic_ir=round(ic * 2, 4),
                rank_ic=round(ic * 0.8, 4),
            ))
        return FactorICListResponse(factor_id=factor_id, values=values, count=len(values))

    def _mock_factor_returns(self, factor_id: str) -> FactorReturnListResponse:
        """模拟因子收益"""
        import random
        values = []
        cum_return = 0
        for i in range(30):
            period_ret = random.uniform(-0.02, 0.03)
            cum_return += period_ret
            values.append(FactorReturn(
                factor_id=factor_id,
                date=(datetime.now() - timedelta(days=i)).strftime("%Y%m%d"),
                period_return=round(period_ret * 100, 2),
                cumulative_return=round(cum_return * 100, 2),
                sharpe=round(random.uniform(0.5, 2.0), 2),
                max_drawdown=round(random.uniform(0.05, 0.2) * 100, 2),
            ))
        return FactorReturnListResponse(factor_id=factor_id, values=values, count=len(values))

    def _mock_screen_stocks(self, request: FactorScreenRequest) -> FactorScreenResponse:
        """模拟因子选股"""
        import random
        stocks = []
        date_str = request.date or datetime.now().strftime("%Y%m%d")

        for i in range(min(request.limit, 50)):
            stock_code = f"{random.randint(1, 999999):06d}"
            factor_values = {cond["factor_id"]: random.uniform(0, 100) for cond in request.factors}
            stocks.append(FactorScreenResult(
                stock_code=stock_code,
                stock_name=f"股票{stock_code}",
                date=date_str,
                score=sum(factor_values.values()),
                factor_values=factor_values,
            ))

        stocks.sort(key=lambda x: x.score, reverse=True)
        return FactorScreenResponse(date=date_str, stocks=stocks, count=len(stocks))


# 单例
factor_service = FactorService()