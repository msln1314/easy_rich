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
    return getattr(settings, 'STOCK_SERVICE_URL', 'http://localhost:8008')


class StockServiceClient:
    """股票服务客户端 - 调用 stock-service 接口"""

    @classmethod
    async def _call_stock_service(cls, endpoint: str, method: str = "GET", params: Dict = None) -> Dict[str, Any]:
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
                    items.append({
                        "index_code": item.get("code"),
                        "index_name": item.get("name"),
                        "close_price": item.get("price"),
                        "change_percent": item.get("change_percent"),
                        "change_amount": item.get("change"),
                        "volume": item.get("volume"),
                        "amount": item.get("amount"),
                    })
                return items
            return []
        except Exception as e:
            logger.error(f"获取指数行情失败: {e}")
            return []

    @classmethod
    async def get_index_history(cls, index_code: str, period: str = "daily",
                                start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """获取指数历史数据"""
        try:
            params = {}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date

            result = await StockServiceClient._call_stock_service(f"/index/{index_code}/history", params=params)
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
            result = await StockServiceClient._call_stock_service(f"/stock/{stock_code}/quote")
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
            result = await StockServiceClient._call_stock_service("/stock/quotes/batch", method="POST", params=stock_codes)
            if result.get("data"):
                return result["data"]
            return []
        except Exception as e:
            logger.error(f"批量获取股票行情失败: {e}")
            return []

    @classmethod
    async def get_stock_history(cls, stock_code: str, period: str = "daily",
                                start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """获取股票历史数据"""
        try:
            params = {}
            if period:
                params["period"] = period
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date

            result = await StockServiceClient._call_stock_service(f"/stock/{stock_code}/history", params=params)
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
            indices_result = await StockServiceClient._call_stock_service("/market/indices")

            # 解析指数数据 - stock-service 返回 {"data": {"items": [...]}}
            indices = []
            if indices_result.get("data") and indices_result["data"].get("items"):
                for item in indices_result["data"]["items"]:
                    indices.append({
                        "index_code": item.get("index_code"),
                        "index_name": item.get("index_name"),
                        "close_price": item.get("close_price"),
                        "change_percent": item.get("change_percent"),
                        "change_amount": item.get("change_amount"),
                        "volume": item.get("volume"),
                        "amount": item.get("amount"),
                    })

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
            result = await StockServiceClient._call_stock_service("/market/rankings", params={"limit": limit})
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
            result = await StockServiceClient._call_stock_service("/market/rankings/change", params={"limit": limit})
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
            result = await StockServiceClient._call_stock_service("/market/rankings/turnover", params={"limit": limit})
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
            result = await StockServiceClient._call_stock_service("/market/rankings/amount", params={"limit": limit})
            if result.get("data"):
                return result["data"]
            return []
        except Exception as e:
            logger.error(f"获取成交额排行失败: {e}")
            return []


# 全局服务实例
stock_index_service = StockIndexService()
stock_quote_service = StockQuoteService()
market_summary_service = MarketSummaryService()
stock_ranking_service = StockRankingService()