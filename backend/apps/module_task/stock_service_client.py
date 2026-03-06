#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/1
# @File           : stock_service_client.py
# @IDE            : PyCharm
# @desc           : Stock Service HTTP 客户端，只负责调用接口并返回数据

import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime
from core.logger import logger


class StockServiceClient:
    """Stock Service HTTP 客户端"""

    def __init__(self, base_url: str = "http://localhost:8008/api/v1"):
        """
        初始化客户端

        Args:
            base_url: Stock Service 基础 URL
        """
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """异步上下文管理器进入"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self.session:
            await self.session.close()

    async def get_all_stock_list(self) -> List[Dict[str, Any]]:
        """
        获取所有A股股票列表

        Returns:
            List[Dict[str, Any]]: 股票列表
        """
        url = f"{self.base_url}/stock/list"

        try:
            if not self.session:
                self.session = aiohttp.ClientSession()

            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"获取股票列表失败，状态码: {response.status}")
                    raise ValueError(f"HTTP 错误: {response.status}")

                data = await response.json()

                if not data:
                    logger.warning("未获取到股票列表数据")
                    return []

                return data

        except aiohttp.ClientError as e:
            logger.error(f"获取股票列表失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"获取股票列表异常: {str(e)}")
            raise

    async def get_stock_info(self, stock_code: str) -> Dict[str, Any]:
        """
        获取个股基本信息

        Args:
            stock_code: 股票代码

        Returns:
            Dict[str, Any]: 股票信息
        """
        url = f"{self.base_url}/stock/{stock_code}/info"

        try:
            if not self.session:
                self.session = aiohttp.ClientSession()

            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.warning(f"获取股票 {stock_code} 信息失败，状态码: {response.status}")
                    return {}

                data = await response.json()
                return data.get("data", {})

        except aiohttp.ClientError as e:
            logger.error(f"获取股票 {stock_code} 信息失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"获取股票 {stock_code} 信息异常: {str(e)}")
            raise

    async def get_stock_quote(self, stock_code: str) -> Dict[str, Any]:
        """
        获取个股实时行情

        Args:
            stock_code: 股票代码

        Returns:
            Dict[str, Any]: 股票行情
        """
        url = f"{self.base_url}/stock/{stock_code}/quote"

        try:
            if not self.session:
                self.session = aiohttp.ClientSession()

            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.warning(f"获取股票 {stock_code} 行情失败，状态码: {response.status}")
                    return {}

                data = await response.json()
                return data.get("data", {})

        except aiohttp.ClientError as e:
            logger.error(f"获取股票 {stock_code} 行情失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"获取股票 {stock_code} 行情异常: {str(e)}")
            raise

    async def get_stock_history(
        self,
        stock_code: str,
        period: str = "daily",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取个股历史行情

        Args:
            stock_code: 股票代码
            period: 周期，可选 daily(日线), weekly(周线), monthly(月线)
            start_date: 开始日期，格式YYYYMMDD
            end_date: 结束日期，格式YYYYMMDD

        Returns:
            List[Dict[str, Any]]: 历史行情列表
        """
        url = f"{self.base_url}/stock/{stock_code}/history"
        params = {"period": period}

        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        try:
            if not self.session:
                self.session = aiohttp.ClientSession()

            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.warning(f"获取股票 {stock_code} 历史行情失败，状态码: {response.status}")
                    return []

                data = await response.json()
                return data.get("data", [])

        except aiohttp.ClientError as e:
            logger.error(f"获取股票 {stock_code} 历史行情失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"获取股票 {stock_code} 历史行情异常: {str(e)}")
            raise


async def fetch_stock_list() -> List[Dict[str, Any]]:
    """
    获取股票列表（简化函数）

    Returns:
        List[Dict[str, Any]]: 股票列表
    """
    async with StockServiceClient() as client:
        return await client.get_all_stock_list()
