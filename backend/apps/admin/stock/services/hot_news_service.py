#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/14
# @File           : hot_news_service.py
# @IDE            : PyCharm
# @desc           : 热门新闻服务 - 调用 stock-service 接口

from typing import Optional, List, Dict, Any
import httpx

from core.logger import logger
from application.settings import settings


def _get_stock_service_url() -> str:
    """获取 stock-service URL"""
    return getattr(settings, 'STOCK_SERVICE_URL', 'http://localhost:8008')


class HotNewsService:
    """热门新闻服务 - 调用 stock-service 接口"""

    @classmethod
    async def _call_stock_service(cls, endpoint: str, method: str = "GET", json_data: Any = None) -> Dict[str, Any]:
        """调用 stock-service 接口"""
        stock_service_url = _get_stock_service_url()
        url = f"{stock_service_url}/api/v1{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                if method == "GET":
                    response = await client.get(url)
                elif method == "POST":
                    response = await client.post(url, json=json_data)
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
    async def get_sources(cls, column: Optional[str] = None) -> Dict[str, Any]:
        """
        获取所有数据源列表

        Args:
            column: 分类筛选 (finance/china/tech)
        """
        endpoint = "/hot-news/sources"
        if column:
            endpoint = f"{endpoint}?column={column}"

        result = await cls._call_stock_service(endpoint)
        return result

    @classmethod
    async def get_hot_news(cls, source_id: str) -> Dict[str, Any]:
        """
        获取指定数据源的热门新闻

        Args:
            source_id: 数据源ID，如 weibo, zhihu, xueqiu 等
        """
        endpoint = f"/hot-news/{source_id}"
        result = await cls._call_stock_service(endpoint)
        return result

    @classmethod
    async def get_hot_news_batch(cls, source_ids: List[str]) -> Dict[str, Any]:
        """
        批量获取多个数据源的热门新闻

        Args:
            source_ids: 数据源ID列表
        """
        endpoint = "/hot-news/batch"
        result = await cls._call_stock_service(endpoint, method="POST", json_data=source_ids)
        return result

    @classmethod
    async def get_news_by_column(cls, column: str) -> Dict[str, Any]:
        """
        按分类获取热门新闻

        Args:
            column: 分类 (finance/china/tech)
        """
        endpoint = f"/hot-news/column/{column}"
        result = await cls._call_stock_service(endpoint)
        return result


# 便捷函数
async def get_hot_news(source_id: str) -> Dict[str, Any]:
    """获取指定数据源的热门新闻"""
    return await HotNewsService.get_hot_news(source_id)


async def get_hot_news_batch(source_ids: List[str]) -> Dict[str, Any]:
    """批量获取多个数据源的热门新闻"""
    return await HotNewsService.get_hot_news_batch(source_ids)


async def get_all_sources(column: Optional[str] = None) -> Dict[str, Any]:
    """获取所有数据源列表"""
    return await HotNewsService.get_sources(column)


async def get_sources_by_column(column: str) -> Dict[str, Any]:
    """按分类获取数据源"""
    return await HotNewsService.get_news_by_column(column)