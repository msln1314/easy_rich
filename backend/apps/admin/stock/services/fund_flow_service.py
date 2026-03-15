#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/15
# @File           : fund_flow_service.py
# @IDE            : PyCharm
# @desc           : 资金流向服务 - 调用 stock-service 接口

from typing import Optional, Dict, Any
import httpx

from core.logger import logger
from application.settings import settings


def _get_stock_service_url() -> str:
    """获取 stock-service URL"""
    return getattr(settings, 'STOCK_SERVICE_URL', 'http://localhost:8008')


class FundFlowService:
    """资金流向服务 - 调用 stock-service 接口"""

    @classmethod
    async def _call_stock_service(cls, endpoint: str, method: str = "GET", params: Dict = None) -> Dict[str, Any]:
        """调用 stock-service 接口"""
        stock_service_url = _get_stock_service_url()
        url = f"{stock_service_url}/api/v1{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                if method == "GET":
                    response = await client.get(url, params=params)
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

    @classmethod
    async def get_north_money_realtime(cls) -> Dict[str, Any]:
        """获取实时北向资金"""
        endpoint = "/fund-flow/north-money/realtime"
        result = await cls._call_stock_service(endpoint)
        return result

    @classmethod
    async def get_north_money_flow(cls, days: int = 30) -> Dict[str, Any]:
        """获取北向资金历史流向"""
        endpoint = "/fund-flow/north-money/flow"
        result = await cls._call_stock_service(endpoint, params={"days": days})
        return result

    @classmethod
    async def get_market_fund_flow_today(cls) -> Dict[str, Any]:
        """获取今日市场资金流向"""
        endpoint = "/fund-flow/market/flow/today"
        result = await cls._call_stock_service(endpoint)
        return result

    @classmethod
    async def get_market_fund_flow(cls, days: int = 30) -> Dict[str, Any]:
        """获取市场资金流向历史"""
        endpoint = "/fund-flow/market/flow"
        result = await cls._call_stock_service(endpoint, params={"days": days})
        return result


# 便捷函数
async def get_north_money_realtime() -> Dict[str, Any]:
    """获取实时北向资金"""
    return await FundFlowService.get_north_money_realtime()


async def get_north_money_flow(days: int = 30) -> Dict[str, Any]:
    """获取北向资金历史流向"""
    return await FundFlowService.get_north_money_flow(days)


async def get_market_fund_flow_today() -> Dict[str, Any]:
    """获取今日市场资金流向"""
    return await FundFlowService.get_market_fund_flow_today()


async def get_market_fund_flow(days: int = 30) -> Dict[str, Any]:
    """获取市场资金流向历史"""
    return await FundFlowService.get_market_fund_flow(days)