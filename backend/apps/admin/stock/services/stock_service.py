#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/10
# @File           : stock_service.py
# @IDE            : PyCharm
# @desc           : 股票服务层 - 调用 stock-service 接口

from typing import List, Dict, Any, Optional
from datetime import datetime, date
import httpx

from core.logger import logger
from application.settings import settings


def _get_stock_service_url() -> str:
    """获取 stock-service URL"""
    return getattr(settings, "STOCK_SERVICE_URL", "http://localhost:8008")


class StockServiceClient:
    """股票服务客户端 - 调用 stock-service 接口"""

    @classmethod
    async def _call_stock_service(
        cls, endpoint: str, method: str = "GET", params: Dict = None
    ) -> Dict[str, Any]:
        """调用 stock-service 接口"""
        stock_service_url = _get_stock_service_url()
        url = f"{stock_service_url}/api/v1{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                if method == "GET":
                    response = await client.get(url, params=params)
                elif method == "POST":
                    response = await client.post(url, json=params)
                else:
                    raise ValueError(f"不支持的 HTTP 方法: {method}")

                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"调用 stock-service 失败: {url}, 错误: {str(e)}")
            return {"code": 500, "message": str(e)}
        except Exception as e:
            logger.error(f"调用 stock-service 异常: {url}, 错误: {str(e)}")
            return {"code": 500, "message": str(e)}


class StockIndexService:
    """大盘指数服务类"""

    @classmethod
    async def get_index_quote(cls) -> List[Dict[str, Any]]:
        """获取主要指数实时行情"""
        try:
            result = await StockServiceClient._call_stock_service("/index/quotes")
            # stock-service 返回 {"items": [...], "source": "..."}
            if result.get("items"):
                # 转换字段名以匹配后端期望的格式
                items = []
                for item in result["items"]:
                    items.append(
                        {
                            "index_code": item.get("code"),
                            "index_name": item.get("name"),
                            "close_price": item.get("price"),
                            "change_percent": item.get("change_percent"),
                            "change_amount": item.get("change"),
                            "volume": item.get("volume"),
                            "amount": item.get("amount"),
                        }
                    )
                return items
            return []
        except Exception as e:
            logger.error(f"获取指数行情失败: {e}")
            return []

    @classmethod
    async def get_index_history(
        cls,
        index_code: str,
        period: str = "daily",
        start_date: str = None,
        end_date: str = None,
    ) -> List[Dict[str, Any]]:
        """获取指数历史数据"""
        try:
            params = {}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date

            result = await StockServiceClient._call_stock_service(
                f"/index/{index_code}/history", params=params
            )
            if result.get("data"):
                return result["data"]
            return []
        except Exception as e:
            logger.error(f"获取指数历史失败: {e}")
            return []


class StockQuoteService:
    """股票实时行情服务类"""

    @classmethod
    async def get_stock_quote(cls, stock_code: str) -> Optional[Dict[str, Any]]:
        """获取单个股票实时行情"""
        try:
            result = await StockServiceClient._call_stock_service(
                f"/stock/{stock_code}/quote"
            )
            if result.get("data"):
                return result["data"]
            return None
        except Exception as e:
            logger.error(f"获取股票行情失败: {e}")
            return None

    @classmethod
    async def get_stock_quotes(cls, stock_codes: List[str]) -> List[Dict[str, Any]]:
        """批量获取股票实时行情"""
        try:
            result = await StockServiceClient._call_stock_service(
                "/stock/quotes/batch", method="POST", params=stock_codes
            )
            if result.get("data"):
                return result["data"]
            return []
        except Exception as e:
            logger.error(f"批量获取股票行情失败: {e}")
            return []

    @classmethod
    async def get_stock_history(
        cls,
        stock_code: str,
        period: str = "daily",
        start_date: str = None,
        end_date: str = None,
    ) -> List[Dict[str, Any]]:
        """获取股票历史数据"""
        try:
            params = {}
            if period:
                params["period"] = period
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date

            result = await StockServiceClient._call_stock_service(
                f"/stock/{stock_code}/history", params=params
            )
            if result.get("data"):
                return result["data"]
            return []
        except Exception as e:
            logger.error(f"获取股票历史失败: {e}")
            return []


class MarketSummaryService:
    """市场汇总服务类"""

    @classmethod
    async def get_market_summary(cls) -> Dict[str, Any]:
        """获取市场汇总数据"""
        try:
            # 获取市场汇总
            result = await StockServiceClient._call_stock_service("/market/summary")
            # 获取指数数据
            indices_result = await StockServiceClient._call_stock_service(
                "/market/indices"
            )

            # 解析指数数据 - stock-service 返回 {"data": {"items": [...]}}
            indices = []
            if indices_result.get("data") and indices_result["data"].get("items"):
                for item in indices_result["data"]["items"]:
                    indices.append(
                        {
                            "index_code": item.get("index_code"),
                            "index_name": item.get("index_name"),
                            "close_price": item.get("close_price"),
                            "change_percent": item.get("change_percent"),
                            "change_amount": item.get("change_amount"),
                            "volume": item.get("volume"),
                            "amount": item.get("amount"),
                        }
                    )

            # 解析市场汇总数据 - stock-service 返回 {"data": {...}}
            market_data = result.get("data", {})

            return {
                "indices": indices,
                "total_stocks": market_data.get("total_stocks", 0),
                "up_stocks": market_data.get("up_stocks", 0),
                "down_stocks": market_data.get("down_stocks", 0),
                "flat_stocks": market_data.get("flat_stocks", 0),
                "total_amount": market_data.get("total_amount", 0),
                "total_volume": market_data.get("total_volume", 0),
                "limit_up_count": market_data.get("limit_up_count", 0),
                "limit_down_count": market_data.get("limit_down_count", 0),
            }
        except Exception as e:
            logger.error(f"获取市场汇总失败: {e}")
            return {}


class StockRankingService:
    """股票排行服务类"""

    @classmethod
    async def get_realtime_rankings(cls, limit: int = 20) -> Dict[str, Any]:
        """获取实时排行"""
        try:
            result = await StockServiceClient._call_stock_service(
                "/market/rankings", params={"limit": limit}
            )
            if result.get("data"):
                return result["data"]
            return {}
        except Exception as e:
            logger.error(f"获取实时排行失败: {e}")
            return {}

    @classmethod
    async def get_change_percent_ranking(cls, limit: int = 20) -> List[Dict[str, Any]]:
        """获取涨幅排行"""
        try:
            result = await StockServiceClient._call_stock_service(
                "/market/rankings/change", params={"limit": limit}
            )
            if result.get("data"):
                return result["data"]
            return []
        except Exception as e:
            logger.error(f"获取涨幅排行失败: {e}")
            return []

    @classmethod
    async def get_turnover_ranking(cls, limit: int = 20) -> List[Dict[str, Any]]:
        """获取换手率排行"""
        try:
            result = await StockServiceClient._call_stock_service(
                "/market/rankings/turnover", params={"limit": limit}
            )
            if result.get("data"):
                return result["data"]
            return []
        except Exception as e:
            logger.error(f"获取换手率排行失败: {e}")
            return []

    @classmethod
    async def get_amount_ranking(cls, limit: int = 20) -> List[Dict[str, Any]]:
        """获取成交额排行"""
        try:
            result = await StockServiceClient._call_stock_service(
                "/market/rankings/amount", params={"limit": limit}
            )
            if result.get("data"):
                return result["data"]
            return []
        except Exception as e:
            logger.error(f"获取成交额排行失败: {e}")
            return []


class SectorRotationService:
    """板块轮动服务类"""

    @classmethod
    async def get_sector_leaders(
        cls, sector_type: str = "industry", limit: int = 50
    ) -> List[Dict[str, Any]]:
        """获取板块龙头股排行"""
        try:
            result = await StockServiceClient._call_stock_service(
                "/sector/leaders", params={"sector_type": sector_type, "limit": limit}
            )
            if isinstance(result, list):
                return result
            if isinstance(result, dict) and result.get("data"):
                return result["data"]
            return cls._generate_mock_leaders(sector_type, limit)
        except Exception as e:
            logger.error(f"获取板块龙头股排行失败: {e}")
            return cls._generate_mock_leaders(sector_type, limit)

    @classmethod
    async def get_sector_leader_by_code(
        cls, board_code: str, sector_type: str = "industry"
    ) -> Optional[Dict[str, Any]]:
        """获取指定板块的龙头股信息"""
        try:
            endpoint = f"/sector/{sector_type}/{board_code}/leader"
            result = await StockServiceClient._call_stock_service(endpoint)
            if result and not result.get("code"):
                return result
            return None
        except Exception as e:
            logger.error(f"获取板块龙头股失败: {e}")
            return None

    @classmethod
    async def get_sector_realtime_status(
        cls, sector_type: str = "industry"
    ) -> List[Dict[str, Any]]:
        """获取板块实时状态"""
        try:
            result = await StockServiceClient._call_stock_service(
                "/sector/realtime", params={"sector_type": sector_type}
            )
            if isinstance(result, list):
                return result
            if isinstance(result, dict) and result.get("data"):
                return result["data"]
            return cls._generate_mock_realtime(sector_type)
        except Exception as e:
            logger.error(f"获取板块实时状态失败: {e}")
            return cls._generate_mock_realtime(sector_type)

    @classmethod
    async def get_sector_rotation_history(
        cls,
        board_code: str,
        sector_type: str = "industry",
        start_date: str = None,
        end_date: str = None,
    ) -> List[Dict[str, Any]]:
        """获取板块历史行情数据"""
        try:
            params = {"sector_type": sector_type}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date
            result = await StockServiceClient._call_stock_service(
                f"/sector/rotation/history/{board_code}", params=params
            )
            if isinstance(result, list):
                return result
            if isinstance(result, dict) and result.get("data"):
                return result["data"]
            return []
        except Exception as e:
            logger.error(f"获取板块历史行情失败: {e}")
            return []

    @classmethod
    async def get_sector_factors(
        cls, sector_type: str = "industry", limit: int = 30
    ) -> List[Dict[str, Any]]:
        """获取板块多因子数据"""
        try:
            result = await StockServiceClient._call_stock_service(
                "/sector/factors", params={"sector_type": sector_type, "limit": limit}
            )
            if isinstance(result, list):
                return result
            if isinstance(result, dict) and result.get("data"):
                return result["data"]
            return cls._generate_mock_factors(sector_type, limit)
        except Exception as e:
            logger.error(f"获取板块多因子数据失败: {e}")
            return cls._generate_mock_factors(sector_type, limit)

    @classmethod
    async def predict_sector_rotation(
        cls, sector_type: str = "industry"
    ) -> Optional[Dict[str, Any]]:
        """预测板块轮动"""
        try:
            result = await StockServiceClient._call_stock_service(
                "/sector/rotation/predict", params={"sector_type": sector_type}
            )
            if result and not result.get("code"):
                return result
            return cls._generate_mock_prediction(sector_type)
        except Exception as e:
            logger.error(f"预测板块轮动失败: {e}")
            return cls._generate_mock_prediction(sector_type)

    @classmethod
    def _generate_mock_leaders(
        cls, sector_type: str, limit: int
    ) -> List[Dict[str, Any]]:
        """生成模拟龙头股数据"""
        import random

        sector_names = [
            "人工智能",
            "新能源汽车",
            "半导体",
            "医药生物",
            "新材料",
            "5G通信",
            "云计算",
            "大数据",
            "物联网",
            "区块链",
        ]
        stock_names = ["龙头股A", "龙头股B", "龙头股C", "龙头股D", "龙头股E"]

        result = []
        for i in range(min(limit, len(sector_names))):
            result.append(
                {
                    "sector_code": f"BK{1000 + i}",
                    "sector_name": sector_names[i],
                    "sector_type": sector_type,
                    "leader_stock": {
                        "code": f"60{1000 + i}",
                        "name": stock_names[i % len(stock_names)],
                        "price": round(random.uniform(10, 100), 2),
                        "change_percent": round(random.uniform(-5, 10), 2),
                        "change": round(random.uniform(-2, 5), 2),
                        "volume": round(random.uniform(10000, 100000), 0),
                        "amount": round(random.uniform(100000, 1000000), 0),
                        "turnover_rate": round(random.uniform(1, 10), 2),
                        "score": round(random.uniform(50, 100), 1),
                        "is_limit_up": random.random() > 0.9,
                    },
                    "second_leader": None,
                    "third_leader": None,
                    "change_percent": round(random.uniform(-3, 5), 2),
                    "up_count": random.randint(10, 50),
                    "down_count": random.randint(5, 30),
                    "limit_up_count": random.randint(0, 5),
                    "limit_down_count": random.randint(0, 3),
                    "active_stocks": random.randint(5, 20),
                    "fund_inflow": round(random.uniform(-10000, 50000), 0),
                    "total_amount": round(random.uniform(100000, 1000000), 0),
                    "activity_score": round(random.uniform(40, 90), 1),
                }
            )
        return result

    @classmethod
    def _generate_mock_realtime(cls, sector_type: str) -> List[Dict[str, Any]]:
        """生成模拟实时状态数据"""
        import random

        sector_names = [
            "人工智能",
            "新能源汽车",
            "半导体",
            "医药生物",
            "新材料",
            "5G通信",
            "云计算",
            "大数据",
            "物联网",
            "区块链",
        ]

        result = []
        for i, name in enumerate(sector_names):
            result.append(
                {
                    "sector_code": f"BK{1000 + i}",
                    "sector_name": name,
                    "sector_type": sector_type,
                    "change_percent": round(random.uniform(-3, 5), 2),
                    "change": round(random.uniform(-2, 3), 2),
                    "price": round(random.uniform(1000, 5000), 2),
                    "up_count": random.randint(10, 50),
                    "down_count": random.randint(5, 30),
                    "leading_stock": f"领涨股{i}",
                    "leading_stock_change_percent": round(random.uniform(0, 10), 2),
                }
            )
        return result

    @classmethod
    def _generate_mock_factors(
        cls, sector_type: str, limit: int
    ) -> List[Dict[str, Any]]:
        """生成模拟因子数据"""
        import random

        sector_names = [
            "人工智能",
            "新能源汽车",
            "半导体",
            "医药生物",
            "新材料",
            "5G通信",
            "云计算",
            "大数据",
            "物联网",
            "区块链",
        ]

        result = []
        for i, name in enumerate(sector_names[:limit]):
            fund_flow = round(random.uniform(30, 80), 1)
            sentiment = round(random.uniform(30, 80), 1)
            technical = round(random.uniform(30, 80), 1)
            pattern = round(random.uniform(30, 80), 1)
            total = round(
                fund_flow * 0.3 + sentiment * 0.25 + technical * 0.25 + pattern * 0.2, 1
            )

            result.append(
                {
                    "sector_code": f"BK{1000 + i}",
                    "sector_name": name,
                    "sector_type": sector_type,
                    "fund_flow_score": fund_flow,
                    "sentiment_score": sentiment,
                    "technical_score": technical,
                    "pattern_score": pattern,
                    "total_score": total,
                }
            )
        return result

    @classmethod
    def _generate_mock_prediction(cls, sector_type: str) -> Dict[str, Any]:
        """生成模拟预测数据"""
        import random
        from datetime import datetime

        sector_names = [
            "人工智能",
            "新能源汽车",
            "半导体",
            "医药生物",
            "新材料",
            "5G通信",
            "云计算",
            "大数据",
            "物联网",
            "区块链",
        ]

        predictions = []
        for i, name in enumerate(sector_names):
            prob = round(random.uniform(0.2, 0.8), 4)
            predictions.append(
                {
                    "rank": i + 1,
                    "sector_code": f"BK{1000 + i}",
                    "sector_name": name,
                    "probability": prob,
                    "confidence": round(0.5 + prob * 0.3, 4),
                    "factors": {
                        "fund_flow": round(random.uniform(30, 80), 1),
                        "sentiment": round(random.uniform(30, 80), 1),
                        "technical": round(random.uniform(30, 80), 1),
                        "pattern": round(random.uniform(30, 80), 1),
                    },
                }
            )

        predictions.sort(key=lambda x: x["probability"], reverse=True)
        for i, p in enumerate(predictions):
            p["rank"] = i + 1

        return {
            "prediction_id": f"pred_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "prediction_time": datetime.now().isoformat(),
            "target_date": datetime.now().strftime("%Y-%m-%d"),
            "predictions": predictions,
            "model_version": "1.0-mock",
            "confidence": predictions[0]["confidence"] if predictions else 0,
        }


# 全局服务实例
stock_index_service = StockIndexService()
stock_quote_service = StockQuoteService()
market_summary_service = MarketSummaryService()
stock_ranking_service = StockRankingService()
sector_rotation_service = SectorRotationService()
