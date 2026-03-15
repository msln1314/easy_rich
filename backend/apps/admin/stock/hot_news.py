#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/14
# @File           : hot_news.py
# @IDE            : PyCharm
# @desc           : 热门头条 API 接口

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Body

from apps.admin.auth.utils.current import OpenAuth, Auth
from apps.admin.stock.services.hot_news_service import (
    get_hot_news,
    get_hot_news_batch,
    get_all_sources,
    get_sources_by_column,
)
from utils.response import SuccessResponse, ErrorResponse
from core.logger import logger

router = APIRouter(tags=["热门头条"])


@router.get("/hot-news/sources", summary="获取所有数据源列表")
async def get_sources(
    column: Optional[str] = Query(None, description="分类筛选: finance/china/tech"),
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取所有支持的数据源列表

    参数：
    - column: 分类筛选 (finance=财经, china=综合, tech=科技)
    """
    try:
        result = await get_all_sources(column)
        if result.get("code") != 200:
            return ErrorResponse(result.get("message", "获取数据源列表失败"))
        return SuccessResponse(result.get("data", {}))

    except Exception as e:
        logger.error(f"获取数据源列表失败: {str(e)}")
        return ErrorResponse(f"获取数据源列表失败: {str(e)}")


@router.get("/hot-news/{source_id}", summary="获取指定数据源的热门新闻")
async def get_news_by_source(
    source_id: str,
    auth: Auth = Depends(OpenAuth()),
):
    """
    获取指定数据源的热门新闻

    支持的数据源ID：
    - weibo: 微博实时热搜
    - zhihu: 知乎热榜
    - xueqiu: 雪球热门股票
    - jin10: 金十数据快讯
    - wallstreetcn-quick: 华尔街见闻快讯
    - wallstreetcn-news: 华尔街见闻新闻
    - wallstreetcn-hot: 华尔街见闻热门
    - baidu: 百度热搜
    - hackernews: Hacker News热门
    """
    try:
        result = await get_hot_news(source_id)
        if result.get("code") != 200:
            return ErrorResponse(result.get("message", "获取热门新闻失败"))
        return SuccessResponse(result.get("data", {}))

    except Exception as e:
        logger.error(f"获取热门新闻失败: {str(e)}")
        return ErrorResponse(f"获取热门新闻失败: {str(e)}")


@router.post("/hot-news/batch", summary="批量获取多个数据源的热门新闻")
async def get_news_batch(
    source_ids: List[str] = Body(..., description="数据源ID列表", examples=[["weibo", "zhihu", "xueqiu"]]),
    auth: Auth = Depends(OpenAuth()),
):
    """
    批量获取多个数据源的热门新闻

    请求体示例：
    ["weibo", "zhihu", "xueqiu"]

    返回每个数据源的新闻列表
    """
    try:
        if not source_ids:
            return ErrorResponse("数据源ID列表不能为空")

        if len(source_ids) > 10:
            return ErrorResponse("单次查询数据源数量不能超过10个")

        result = await get_hot_news_batch(source_ids)
        if result.get("code") != 200:
            return ErrorResponse(result.get("message", "批量获取热门新闻失败"))
        return SuccessResponse(result.get("data", {}))

    except Exception as e:
        logger.error(f"批量获取热门新闻失败: {str(e)}")
        return ErrorResponse(f"批量获取热门新闻失败: {str(e)}")


@router.get("/hot-news/column/{column}", summary="按分类获取热门新闻")
async def get_news_by_column_api(
    column: str,
    auth: Auth = Depends(OpenAuth()),
):
    """
    按分类获取热门新闻

    支持的分类：
    - finance: 财经类（雪球、金十数据、华尔街见闻等）
    - china: 综合类（微博、知乎、百度热搜等）
    - tech: 科技类（Hacker News、IT之家等）
    """
    try:
        valid_columns = ["finance", "china", "tech"]
        if column not in valid_columns:
            return ErrorResponse(f"无效的分类: {column}，支持: {', '.join(valid_columns)}")

        result = await get_sources_by_column(column)
        if result.get("code") != 200:
            return ErrorResponse(result.get("message", "按分类获取热门新闻失败"))
        return SuccessResponse(result.get("data", {}))

    except Exception as e:
        logger.error(f"按分类获取热门新闻失败: {str(e)}")
        return ErrorResponse(f"按分类获取热门新闻失败: {str(e)}")