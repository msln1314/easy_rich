#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/14
# @File           : hot_news_routes.py
# @IDE            : PyCharm
# @desc           : 热门头条 API 路由

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Body

from app.services.hot_news_service import (
    get_hot_news,
    get_hot_news_batch,
    get_all_sources,
    get_sources_by_column,
)

router = APIRouter()


@router.get("/sources")
async def get_sources(column: Optional[str] = Query(None, description="分类筛选: finance/china/tech")):
    """
    获取所有支持的数据源列表

    参数：
    - column: 分类筛选 (finance=财经, china=综合, tech=科技)
    """
    try:
        if column:
            sources = get_sources_by_column(column)
        else:
            sources = get_all_sources()

        return {
            "code": 200,
            "data": {
                "total": len(sources),
                "sources": sources,
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据源列表失败: {str(e)}")


@router.get("/{source_id}")
async def get_news_by_source(source_id: str):
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
        return {
            "code": 200,
            "data": result.to_dict()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取热门新闻失败: {str(e)}")


@router.post("/batch")
async def get_news_batch(source_ids: List[str] = Body(..., description="数据源ID列表", examples=[["weibo", "zhihu", "xueqiu"]])):
    """
    批量获取多个数据源的热门新闻

    请求体示例：
    ["weibo", "zhihu", "xueqiu"]

    返回每个数据源的新闻列表
    """
    try:
        if not source_ids:
            raise HTTPException(status_code=400, detail="数据源ID列表不能为空")

        if len(source_ids) > 10:
            raise HTTPException(status_code=400, detail="单次查询数据源数量不能超过10个")

        results = await get_hot_news_batch(source_ids)

        return {
            "code": 200,
            "data": {
                source_id: result.to_dict()
                for source_id, result in results.items()
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量获取热门新闻失败: {str(e)}")


@router.get("/column/{column}")
async def get_news_by_column(column: str):
    """
    按分类获取热门新闻

    支持的分类：
    - finance: 财经类（雪球、金十数据、华尔街见闻等）
    - china: 综合类（微博、知乎、百度热搜等）
    - tech: 科技类（Hacker News、IT之家等）
    - world: 国际类
    - hottest: 最热（所有热门榜单数据源）
    - realtime: 实时（所有实时快讯数据源）
    """
    try:
        valid_columns = ["finance", "china", "tech", "world", "hottest", "realtime"]
        if column not in valid_columns:
            raise HTTPException(status_code=400, detail=f"无效的分类: {column}，支持: {', '.join(valid_columns)}")

        sources = get_sources_by_column(column)
        available_sources = [s for s in sources if s.get("available")]
        source_ids = [s["id"] for s in available_sources]

        results = await get_hot_news_batch(source_ids)

        return {
            "code": 200,
            "data": {
                "column": column,
                "sources": [
                    {
                        **s,
                        "data": results.get(s["id"]).to_dict() if s["id"] in results else None
                    }
                    for s in available_sources
                ]
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"按分类获取热门新闻失败: {str(e)}")