#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/14
# @File           : hot_news_service.py
# @IDE            : PyCharm
# @desc           : 热门新闻数据获取服务

import re
import json
import time
import asyncio
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class NewsItem:
    """新闻条目"""
    id: str
    title: str
    url: str
    mobile_url: Optional[str] = None
    pub_date: Optional[int] = None
    extra: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SourceResponse:
    """数据源响应"""
    status: str  # success / error
    source_id: str
    source_name: str
    updated_time: int
    items: List[NewsItem] = field(default_factory=list)
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "source_id": self.source_id,
            "source_name": self.source_name,
            "updated_time": self.updated_time,
            "items": [item.to_dict() for item in self.items],
            "message": self.message,
        }


# 数据源定义
# type: "hottest" = 最热榜单, "realtime" = 实时快讯, null = 普通分类
SOURCES = {
    # 财经类
    "xueqiu": {"name": "雪球", "title": "热门股票", "column": "finance", "color": "blue", "type": "hottest"},
    "jin10": {"name": "金十数据", "title": "快讯", "column": "finance", "color": "blue", "type": "realtime"},
    "wallstreetcn-quick": {"name": "华尔街见闻", "title": "快讯", "column": "finance", "color": "blue", "type": "realtime"},
    "wallstreetcn-news": {"name": "华尔街见闻", "title": "新闻", "column": "finance", "color": "blue"},
    "wallstreetcn-hot": {"name": "华尔街见闻", "title": "最热", "column": "finance", "color": "blue", "type": "hottest"},
    "gelonghui": {"name": "格隆汇", "title": "事件", "column": "finance", "color": "blue", "type": "realtime"},
    "cls-telegraph": {"name": "财联社", "title": "电报", "column": "finance", "color": "red", "type": "realtime"},
    "cls-hot": {"name": "财联社", "title": "热门", "column": "finance", "color": "red", "type": "hottest"},
    "fastbull-express": {"name": "法布财经", "title": "快讯", "column": "finance", "color": "emerald", "type": "realtime"},
    "mktnews-flash": {"name": "MKTNews", "title": "快讯", "column": "finance", "color": "indigo", "type": "realtime"},

    # 综合类
    "weibo": {"name": "微博", "title": "实时热搜", "column": "china", "color": "red", "type": "hottest"},
    "zhihu": {"name": "知乎", "title": "热榜", "column": "china", "color": "blue", "type": "hottest"},
    "baidu": {"name": "百度热搜", "title": "热搜", "column": "china", "color": "blue", "type": "hottest"},
    "toutiao": {"name": "今日头条", "title": "热门", "column": "china", "color": "red", "type": "hottest"},
    "douyin": {"name": "抖音", "title": "热门", "column": "china", "color": "gray", "type": "hottest"},
    "thepaper": {"name": "澎湃新闻", "title": "热榜", "column": "china", "color": "gray", "type": "hottest"},

    # 科技类
    "ithome": {"name": "IT之家", "title": "最新", "column": "tech", "color": "red", "type": "realtime"},
    "juejin": {"name": "稀土掘金", "title": "热门", "column": "tech", "color": "blue", "type": "hottest"},
    "hackernews": {"name": "Hacker News", "title": "热门", "column": "tech", "color": "orange", "type": "hottest"},
    "github-trending": {"name": "GitHub", "title": "Today", "column": "tech", "color": "gray", "type": "hottest"},
    "v2ex-share": {"name": "V2EX", "title": "最新分享", "column": "tech", "color": "slate", "type": "realtime"},
    "sspai": {"name": "少数派", "title": "热门", "column": "tech", "color": "red", "type": "hottest"},
}


class HotNewsService:
    """热门新闻服务基类"""

    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    @classmethod
    async def _fetch(cls, url: str, headers: Optional[Dict] = None, timeout: int = 15) -> Optional[str]:
        """HTTP GET 请求"""
        try:
            _headers = {**cls.DEFAULT_HEADERS, **(headers or {})}
            # 增加重试机制
            for attempt in range(3):
                try:
                    async with httpx.AsyncClient(
                        timeout=httpx.Timeout(timeout, connect=10.0),
                        limits=httpx.Limits(max_connections=10)
                    ) as client:
                        response = await client.get(url, headers=_headers, follow_redirects=True)
                        response.raise_for_status()
                        return response.text
                except httpx.ConnectError as e:
                    if attempt < 2:
                        logger.warning(f"连接失败，重试 {attempt + 1}/3: {url}")
                        await asyncio.sleep(1)
                        continue
                    raise e
                except httpx.TimeoutException as e:
                    if attempt < 2:
                        logger.warning(f"请求超时，重试 {attempt + 1}/3: {url}")
                        await asyncio.sleep(1)
                        continue
                    raise e
        except Exception as e:
            logger.error(f"请求失败: {url}, 错误: {str(e)}")
            return None
        return None

    @classmethod
    async def _fetch_json(cls, url: str, headers: Optional[Dict] = None, timeout: int = 15) -> Optional[Any]:
        """HTTP GET 请求返回 JSON"""
        try:
            _headers = {**cls.DEFAULT_HEADERS, **(headers or {})}
            # 增加重试机制
            for attempt in range(3):
                try:
                    async with httpx.AsyncClient(
                        timeout=httpx.Timeout(timeout, connect=10.0),
                        limits=httpx.Limits(max_connections=10)
                    ) as client:
                        response = await client.get(url, headers=_headers, follow_redirects=True)
                        response.raise_for_status()
                        return response.json()
                except httpx.ConnectError as e:
                    if attempt < 2:
                        logger.warning(f"连接失败，重试 {attempt + 1}/3: {url}")
                        await asyncio.sleep(1)
                        continue
                    raise e
                except httpx.TimeoutException as e:
                    if attempt < 2:
                        logger.warning(f"请求超时，重试 {attempt + 1}/3: {url}")
                        await asyncio.sleep(1)
                        continue
                    raise e
        except Exception as e:
            logger.error(f"请求JSON失败: {url}, 错误: {str(e)}")
            return None
        return None

    @classmethod
    def _parse_relative_date(cls, time_str: str, timezone: str = "Asia/Shanghai") -> int:
        """解析相对时间"""
        now = int(time.time())
        if not time_str:
            return now

        # 处理 "X分钟前" 格式
        match = re.match(r"(\d+)分钟前", time_str)
        if match:
            return now - int(match.group(1)) * 60

        # 处理 "X小时前" 格式
        match = re.match(r"(\d+)小时前", time_str)
        if match:
            return now - int(match.group(1)) * 3600

        # 处理 "今天 HH:MM" 格式
        match = re.match(r"今天\s*(\d{1,2}):(\d{2})", time_str)
        if match:
            hour, minute = int(match.group(1)), int(match.group(2))
            today = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            return int(today.timestamp())

        return now


class WeiboService(HotNewsService):
    """微博热搜"""

    @classmethod
    async def get_hot_search(cls) -> SourceResponse:
        """获取微博实时热搜"""
        source_id = "weibo"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://s.weibo.com/top/summary?cate=realtimehot"
            headers = {
                **cls.DEFAULT_HEADERS,
                "Cookie": "SUB=_2AkMWIuNSf8NxqwJRmP8dy2rhaoV2ygrEieKgfhKJJRMxHRl-yT9jqk86tRB6PaLNvQZR6zYUcYVT1zSjoSreQHidcUq7",
                "Referer": url,
            }

            html = await cls._fetch(url, headers)
            if not html:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "微博"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            soup = BeautifulSoup(html, "lxml")
            rows = soup.select("#pl_top_realtimehot table tbody tr")[1:]  # 跳过表头

            items = []
            for row in rows:
                link = row.select_one("td.td-02 a")
                if not link:
                    continue

                href = link.get("href", "")
                if "javascript:void" in href:
                    continue

                title = link.get_text(strip=True)
                if not title:
                    continue

                flag = row.select_one("td.td-03")
                flag_text = flag.get_text(strip=True) if flag else ""

                flag_urls = {
                    "新": "https://simg.s.weibo.com/moter/flags/1_0.png",
                    "热": "https://simg.s.weibo.com/moter/flags/2_0.png",
                    "爆": "https://simg.s.weibo.com/moter/flags/4_0.png",
                }

                items.append(NewsItem(
                    id=title,
                    title=title,
                    url=f"https://s.weibo.com{href}",
                    mobile_url=f"https://s.weibo.com{href}",
                    extra={"icon": {"url": flag_urls.get(flag_text), "scale": 1.5}} if flag_text in flag_urls else None,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "微博"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取微博热搜失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "微博"),
                updated_time=int(time.time()),
                message=str(e),
            )


class ZhihuService(HotNewsService):
    """知乎热榜"""

    @classmethod
    async def get_hot_list(cls) -> SourceResponse:
        """获取知乎热榜"""
        source_id = "zhihu"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-list-web?limit=30&desktop=true"
            headers = {
                **cls.DEFAULT_HEADERS,
                "Referer": "https://www.zhihu.com",
            }

            data = await cls._fetch_json(url, headers)
            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "知乎"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", []):
                target = item.get("target", {})
                title_area = target.get("title_area", {})
                excerpt_area = target.get("excerpt_area", {})
                metrics_area = target.get("metrics_area", {})
                link = target.get("link", {})

                title = title_area.get("text", "")
                url = link.get("url", "")

                if not title or not url:
                    continue

                # 提取ID
                match = re.search(r"(\d+)$", url)
                item_id = match.group(1) if match else url

                items.append(NewsItem(
                    id=item_id,
                    title=title,
                    url=url,
                    extra={
                        "info": metrics_area.get("text", ""),
                        "hover": excerpt_area.get("text", ""),
                    },
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "知乎"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取知乎热榜失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "知乎"),
                updated_time=int(time.time()),
                message=str(e),
            )


class XueqiuService(HotNewsService):
    """雪球热门股票"""

    @classmethod
    async def get_hot_stock(cls) -> SourceResponse:
        """获取雪球热门股票"""
        source_id = "xueqiu"
        source_info = SOURCES.get(source_id, {})

        try:
            # 先获取 cookie
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get("https://xueqiu.com/hq", headers=cls.DEFAULT_HEADERS)
                cookies = dict(resp.cookies)

            url = "https://stock.xueqiu.com/v5/stock/hot_stock/list.json?size=30&_type=10&type=10"
            data = await cls._fetch_json(url, headers={**cls.DEFAULT_HEADERS, "Cookie": "; ".join([f"{k}={v}" for k, v in cookies.items()])})

            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "雪球"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", {}).get("items", []):
                if item.get("ad"):  # 跳过广告
                    continue

                code = item.get("code", "")
                name = item.get("name", "")
                percent = item.get("percent", 0)
                exchange = item.get("exchange", "")

                items.append(NewsItem(
                    id=code,
                    title=name,
                    url=f"https://xueqiu.com/s/{code}",
                    extra={"info": f"{percent}% {exchange}"},
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "雪球"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取雪球热门股票失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "雪球"),
                updated_time=int(time.time()),
                message=str(e),
            )


class Jin10Service(HotNewsService):
    """金十数据快讯"""

    @classmethod
    async def get_flash(cls) -> SourceResponse:
        """获取金十数据快讯"""
        source_id = "jin10"
        source_info = SOURCES.get(source_id, {})

        try:
            timestamp = int(time.time() * 1000)
            url = f"https://www.jin10.com/flash_newest.js?t={timestamp}"

            raw_data = await cls._fetch(url)
            if not raw_data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "金十数据"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            # 解析 JS 变量
            json_str = raw_data.replace("var newest = ", "").rstrip(";").strip()
            data = json.loads(json_str)

            items = []
            for item in data:
                item_data = item.get("data", {})
                content = item_data.get("title") or item_data.get("content", "")
                if not content:
                    continue

                # 跳过特定频道
                if 5 in item.get("channel", []):
                    continue

                # 清理 HTML 标签
                content = re.sub(r"</?b>", "", content)

                # 解析标题
                match = re.match(r"^【([^】]*)】(.*)$", content)
                if match:
                    title = match.group(1)
                    desc = match.group(2)
                else:
                    title = content
                    desc = None

                pub_date = cls._parse_relative_date(item.get("time", ""))

                items.append(NewsItem(
                    id=item.get("id", ""),
                    title=title,
                    url=f"https://flash.jin10.com/detail/{item.get('id')}",
                    pub_date=pub_date,
                    extra={
                        "hover": desc,
                        "info": "✰" if item.get("important") else None,
                    },
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "金十数据"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取金十数据快讯失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "金十数据"),
                updated_time=int(time.time()),
                message=str(e),
            )


class WallstreetcnService(HotNewsService):
    """华尔街见闻"""

    @classmethod
    async def get_quick(cls) -> SourceResponse:
        """获取华尔街见闻快讯"""
        source_id = "wallstreetcn-quick"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://api-one.wallstcn.com/apiv1/content/lives?channel=global-channel&limit=30"
            data = await cls._fetch_json(url)

            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "华尔街见闻"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", {}).get("items", []):
                title = item.get("title") or item.get("content_text", "")
                if not title:
                    continue

                items.append(NewsItem(
                    id=str(item.get("id", "")),
                    title=title,
                    url=item.get("uri", ""),
                    pub_date=item.get("display_time", 0) * 1000 if item.get("display_time") else None,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "华尔街见闻"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取华尔街见闻快讯失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "华尔街见闻"),
                updated_time=int(time.time()),
                message=str(e),
            )

    @classmethod
    async def get_news(cls) -> SourceResponse:
        """获取华尔街见闻新闻"""
        source_id = "wallstreetcn-news"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://api-one.wallstcn.com/apiv1/content/information-flow?channel=global-channel&accept=article&limit=30"
            data = await cls._fetch_json(url)

            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "华尔街见闻"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", {}).get("items", []):
                if item.get("resource_type") in ["theme", "ad"]:
                    continue

                resource = item.get("resource", {})
                if resource.get("type") == "live":
                    continue

                title = resource.get("title") or resource.get("content_short", "")
                uri = resource.get("uri", "")

                if not title or not uri:
                    continue

                items.append(NewsItem(
                    id=str(resource.get("id", "")),
                    title=title,
                    url=uri,
                    pub_date=resource.get("display_time", 0) * 1000 if resource.get("display_time") else None,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "华尔街见闻"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取华尔街见闻新闻失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "华尔街见闻"),
                updated_time=int(time.time()),
                message=str(e),
            )

    @classmethod
    async def get_hot(cls) -> SourceResponse:
        """获取华尔街见闻热门"""
        source_id = "wallstreetcn-hot"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://api-one.wallstcn.com/apiv1/content/articles/hot?period=all"
            data = await cls._fetch_json(url)

            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "华尔街见闻"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", {}).get("day_items", []):
                title = item.get("title")
                if not title:
                    continue

                items.append(NewsItem(
                    id=str(item.get("id", "")),
                    title=title,
                    url=item.get("uri", ""),
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "华尔街见闻"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取华尔街见闻热门失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "华尔街见闻"),
                updated_time=int(time.time()),
                message=str(e),
            )


class BaiduService(HotNewsService):
    """百度热搜"""

    @classmethod
    async def get_hot(cls) -> SourceResponse:
        """获取百度热搜"""
        source_id = "baidu"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://top.baidu.com/board?tab=realtime"
            html = await cls._fetch(url)

            if not html:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "百度热搜"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            soup = BeautifulSoup(html, "lxml")
            items = []

            # 解析热搜列表
            for item in soup.select(".category-wrap_iQLoo.horizontal_1eKyQ"):
                title_elem = item.select_one(".title_dIF3B")
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link_elem = item.select_one("a[href*='www.baidu.com/s']")
                url = link_elem.get("href", "") if link_elem else ""

                if not title:
                    continue

                items.append(NewsItem(
                    id=title,
                    title=title,
                    url=url,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "百度热搜"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取百度热搜失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "百度热搜"),
                updated_time=int(time.time()),
                message=str(e),
            )


class HackerNewsService(HotNewsService):
    """Hacker News"""

    @classmethod
    async def get_top(cls) -> SourceResponse:
        """获取 Hacker News 热门"""
        source_id = "hackernews"
        source_info = SOURCES.get(source_id, {})

        try:
            # 获取热门故事ID列表
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            story_ids = await cls._fetch_json(url)

            if not story_ids:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "Hacker News"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for story_id in story_ids[:30]:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story = await cls._fetch_json(story_url)

                if not story:
                    continue

                title = story.get("title", "")
                url = story.get("url") or f"https://news.ycombinator.com/item?id={story_id}"

                items.append(NewsItem(
                    id=str(story_id),
                    title=title,
                    url=url,
                    pub_date=story.get("time", 0) * 1000 if story.get("time") else None,
                    extra={"info": f"{story.get('score', 0)} points"} if story.get("score") else None,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "Hacker News"),
                updated_time=int(time.time()),
                items=items,
            )

        except Exception as e:
            logger.error(f"获取 Hacker News 热门失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "Hacker News"),
                updated_time=int(time.time()),
                message=str(e),
            )


class ClsService(HotNewsService):
    """财联社"""

    @classmethod
    def _get_sign_params(cls) -> dict:
        """生成财联社签名参数"""
        import hashlib

        params = {
            "appName": "CailianpressWeb",
            "os": "web",
            "sv": "7.7.5",
        }
        # 排序参数
        sorted_params = sorted(params.items())
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        # SHA1 签名
        sha1 = hashlib.sha1(param_str.encode()).hexdigest()
        # MD5 签名
        sign = hashlib.md5(sha1.encode()).hexdigest()
        params["sign"] = sign
        return params

    @classmethod
    async def get_telegraph(cls) -> SourceResponse:
        """获取财联社电报"""
        source_id = "cls-telegraph"
        source_info = SOURCES.get(source_id, {})

        try:
            params = cls._get_sign_params()
            url = "https://www.cls.cn/nodeapi/updateTelegraphList"
            headers = {
                **cls.DEFAULT_HEADERS,
                "Referer": "https://www.cls.cn/telegraph",
            }

            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
            data = await cls._fetch_json(f"{url}?{param_str}", headers)

            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "财联社"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", {}).get("roll_data", []):
                # 跳过广告
                if item.get("is_ad"):
                    continue

                title = item.get("title") or item.get("brief", "")
                if not title:
                    continue

                # 清理HTML标签
                title = re.sub(r"<[^>]+>", "", title)

                items.append(NewsItem(
                    id=str(item.get("id", "")),
                    title=title[:100] if len(title) > 100 else title,
                    url=f"https://www.cls.cn/detail/{item.get('id')}",
                    mobile_url=item.get("shareurl", ""),
                    pub_date=item.get("ctime", 0) * 1000 if item.get("ctime") else None,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "财联社"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取财联社电报失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "财联社"),
                updated_time=int(time.time()),
                message=str(e),
            )

    @classmethod
    async def get_hot(cls) -> SourceResponse:
        """获取财联社热门"""
        source_id = "cls-hot"
        source_info = SOURCES.get(source_id, {})

        try:
            params = cls._get_sign_params()
            url = "https://www.cls.cn/v2/article/hot/list"
            headers = {
                **cls.DEFAULT_HEADERS,
                "Referer": "https://www.cls.cn/hot",
            }

            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
            data = await cls._fetch_json(f"{url}?{param_str}", headers)

            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "财联社"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", []):
                title = item.get("title") or item.get("brief", "")
                if not title:
                    continue

                title = re.sub(r"<[^>]+>", "", title)

                items.append(NewsItem(
                    id=str(item.get("id", "")),
                    title=title[:100] if len(title) > 100 else title,
                    url=f"https://www.cls.cn/detail/{item.get('id')}",
                    mobile_url=item.get("shareurl", ""),
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "财联社"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取财联社热门失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "财联社"),
                updated_time=int(time.time()),
                message=str(e),
            )


class GelonghuiService(HotNewsService):
    """格隆汇"""

    @classmethod
    async def get_events(cls) -> SourceResponse:
        """获取格隆汇事件"""
        source_id = "gelonghui"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://www.gelonghui.com/news/"
            html = await cls._fetch(url)

            if not html:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "格隆汇"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            soup = BeautifulSoup(html, "lxml")
            items = []

            for item in soup.select(".article-content")[:30]:
                link = item.select_one(".detail-right>a")
                if not link:
                    continue

                href = link.get("href", "")
                title_elem = link.select_one("h2")
                title = title_elem.get_text(strip=True) if title_elem else ""

                if not title or not href:
                    continue

                # 获取来源信息
                info_elem = item.select_one(".time > span:nth-child(1)")
                info = info_elem.get_text(strip=True) if info_elem else ""

                # 获取时间
                time_elem = item.select_one(".time > span:nth-child(3)")
                time_str = time_elem.get_text(strip=True) if time_elem else ""

                pub_date = None
                if time_str:
                    pub_date = cls._parse_relative_date(time_str)

                items.append(NewsItem(
                    id=href.split("/")[-1] if href else title,
                    title=title,
                    url=f"https://www.gelonghui.com{href}" if href.startswith("/") else href,
                    pub_date=pub_date,
                    extra={"info": info} if info else None,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "格隆汇"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取格隆汇事件失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "格隆汇"),
                updated_time=int(time.time()),
                message=str(e),
            )


class ToutiaoService(HotNewsService):
    """今日头条"""

    @classmethod
    async def get_hot(cls) -> SourceResponse:
        """获取今日头条热门"""
        source_id = "toutiao"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
            headers = {
                **cls.DEFAULT_HEADERS,
                "Referer": "https://www.toutiao.com/",
            }

            data = await cls._fetch_json(url, headers)

            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "今日头条"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", []):
                title = item.get("Title", "")
                cluster_id = item.get("ClusterIdStr", "") or str(item.get("ClusterId", ""))
                if not title or not cluster_id:
                    continue

                items.append(NewsItem(
                    id=cluster_id,
                    title=title,
                    url=f"https://www.toutiao.com/trending/{cluster_id}/",
                    extra={
                        "info": f"热度 {item.get('HotValue', 0)}" if item.get("HotValue") else None,
                        "icon": item.get("LabelUri", {}).get("url") if item.get("LabelUri") else None,
                    },
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "今日头条"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取今日头条热门失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "今日头条"),
                updated_time=int(time.time()),
                message=str(e),
            )


class DouyinService(HotNewsService):
    """抖音"""

    @classmethod
    async def get_hot(cls) -> SourceResponse:
        """获取抖音热门"""
        source_id = "douyin"
        source_info = SOURCES.get(source_id, {})

        try:
            # 先获取 cookie
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get("https://login.douyin.com/", headers=cls.DEFAULT_HEADERS)
                cookies = dict(resp.cookies)

            url = "https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1"
            headers = {
                **cls.DEFAULT_HEADERS,
                "Referer": "https://www.douyin.com/hot",
                "Cookie": "; ".join([f"{k}={v}" for k, v in cookies.items()]),
            }

            data = await cls._fetch_json(url, headers)

            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "抖音"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            word_list = data.get("data", {}).get("word_list", [])
            for item in word_list[:30]:
                title = item.get("word", "")
                sentence_id = item.get("sentence_id", "")
                if not title or not sentence_id:
                    continue

                items.append(NewsItem(
                    id=sentence_id,
                    title=title,
                    url=f"https://www.douyin.com/hot/{sentence_id}",
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "抖音"),
                updated_time=int(time.time()),
                items=items,
            )

        except Exception as e:
            logger.error(f"获取抖音热门失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "抖音"),
                updated_time=int(time.time()),
                message=str(e),
            )


class ThepaperService(HotNewsService):
    """澎湃新闻"""

    @classmethod
    async def get_hot(cls) -> SourceResponse:
        """获取澎湃新闻热榜"""
        source_id = "thepaper"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar"
            headers = {
                **cls.DEFAULT_HEADERS,
                "Referer": "https://www.thepaper.cn/",
            }

            data = await cls._fetch_json(url, headers)

            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "澎湃新闻"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            hot_list = data.get("data", {}).get("hotNews", [])
            for item in hot_list[:30]:
                title = item.get("name", "")
                if not title:
                    continue

                items.append(NewsItem(
                    id=str(item.get("contId", "")),
                    title=title,
                    url=f"https://www.thepaper.cn/newsDetail_forward_{item.get('contId')}",
                    extra={"info": item.get("tag", "")} if item.get("tag") else None,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "澎湃新闻"),
                updated_time=int(time.time()),
                items=items,
            )

        except Exception as e:
            logger.error(f"获取澎湃新闻热榜失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "澎湃新闻"),
                updated_time=int(time.time()),
                message=str(e),
            )


class IthomeService(HotNewsService):
    """IT之家"""

    @classmethod
    async def get_hot(cls) -> SourceResponse:
        """获取IT之家最新"""
        source_id = "ithome"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://www.ithome.com/"
            html = await cls._fetch(url)

            if not html:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "IT之家"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            soup = BeautifulSoup(html, "lxml")
            items = []

            for item in soup.select(".fl li")[:30]:
                link = item.select_one("a")
                if not link:
                    continue

                title = link.get_text(strip=True)
                url = link.get("href", "")

                if not title or not url:
                    continue

                items.append(NewsItem(
                    id=url.split("/")[-1] if url else title,
                    title=title,
                    url=url,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "IT之家"),
                updated_time=int(time.time()),
                items=items,
            )

        except Exception as e:
            logger.error(f"获取IT之家最新失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "IT之家"),
                updated_time=int(time.time()),
                message=str(e),
            )


class JuejinService(HotNewsService):
    """稀土掘金"""

    @classmethod
    async def get_hot(cls) -> SourceResponse:
        """获取稀土掘金热门"""
        source_id = "juejin"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed"
            headers = {
                **cls.DEFAULT_HEADERS,
                "Content-Type": "application/json",
                "Referer": "https://juejin.cn/",
            }
            json_data = {
                "id_type": 2,
                "sort_type": 200,
                "cate_id": "6809637773935378440",
                "cursor": "0",
                "limit": 30,
            }

            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(url, headers=headers, json=json_data)
                data = response.json()

            if not data or data.get("err_no") != 0:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "稀土掘金"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", [])[:30]:
                article_info = item.get("article_info", {})
                title = article_info.get("title", "")
                article_id = article_info.get("article_id", "")

                if not title or not article_id:
                    continue

                items.append(NewsItem(
                    id=article_id,
                    title=title,
                    url=f"https://juejin.cn/post/{article_id}",
                    extra={"info": f"👍 {item.get('article_info', {}).get('view_count', 0)}"} if item.get("article_info", {}).get("view_count") else None,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "稀土掘金"),
                updated_time=int(time.time()),
                items=items,
            )

        except Exception as e:
            logger.error(f"获取稀土掘金热门失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "稀土掘金"),
                updated_time=int(time.time()),
                message=str(e),
            )


class GithubTrendingService(HotNewsService):
    """GitHub Trending"""

    @classmethod
    async def get_trending(cls) -> SourceResponse:
        """获取 GitHub Trending"""
        source_id = "github-trending"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://github.com/trending"
            html = await cls._fetch(url)

            if not html:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "GitHub"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            soup = BeautifulSoup(html, "lxml")
            items = []

            for item in soup.select("article.Box-row")[:30]:
                repo_link = item.select_one("h2 a")
                if not repo_link:
                    continue

                repo_path = repo_link.get("href", "").strip()
                title = repo_path.replace("/", "").strip()

                desc_elem = item.select_one("p.col-9")
                desc = desc_elem.get_text(strip=True) if desc_elem else ""

                stars_elem = item.select_one("span.d-inline-block.float-sm-right")
                stars = stars_elem.get_text(strip=True) if stars_elem else ""

                items.append(NewsItem(
                    id=repo_path,
                    title=title,
                    url=f"https://github.com{repo_path}",
                    extra={
                        "hover": desc[:100] if desc else None,
                        "info": stars if stars else None,
                    },
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "GitHub"),
                updated_time=int(time.time()),
                items=items,
            )

        except Exception as e:
            logger.error(f"获取 GitHub Trending 失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "GitHub"),
                updated_time=int(time.time()),
                message=str(e),
            )


class V2exService(HotNewsService):
    """V2EX"""

    @classmethod
    async def get_latest(cls) -> SourceResponse:
        """获取 V2EX 最新分享"""
        source_id = "v2ex-share"
        source_info = SOURCES.get(source_id, {})

        try:
            # 获取多个板块的 feed
            boards = ["create", "ideas", "programmer", "share"]
            all_items = []

            async with httpx.AsyncClient(timeout=15) as client:
                for board in boards:
                    try:
                        url = f"https://www.v2ex.com/feed/{board}.json"
                        headers = {
                            **cls.DEFAULT_HEADERS,
                            "Referer": "https://www.v2ex.com/",
                        }
                        response = await client.get(url, headers=headers)
                        data = response.json()

                        for item in data.get("items", [])[:10]:
                            title = item.get("title", "")
                            item_url = item.get("url", "")
                            if not title or not item_url:
                                continue

                            # 解析时间
                            date_str = item.get("date_modified") or item.get("date_published", "")
                            pub_date = None
                            if date_str:
                                try:
                                    from datetime import datetime
                                    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                                    pub_date = int(dt.timestamp())
                                except:
                                    pass

                            all_items.append({
                                "id": item.get("id", ""),
                                "title": title,
                                "url": item_url,
                                "pub_date": pub_date,
                            })
                    except Exception as e:
                        logger.warning(f"获取 V2EX {board} 失败: {str(e)}")
                        continue

            # 按时间排序
            all_items.sort(key=lambda x: x.get("pub_date") or 0, reverse=True)

            items = [
                NewsItem(
                    id=str(item["id"]),
                    title=item["title"],
                    url=item["url"],
                    pub_date=item.get("pub_date"),
                )
                for item in all_items[:30]
            ]

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "V2EX"),
                updated_time=int(time.time()),
                items=items,
            )

        except Exception as e:
            logger.error(f"获取 V2EX 最新失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "V2EX"),
                updated_time=int(time.time()),
                message=str(e),
            )


class SspaiService(HotNewsService):
    """少数派"""

    @classmethod
    async def get_hot(cls) -> SourceResponse:
        """获取少数派热门"""
        source_id = "sspai"
        source_info = SOURCES.get(source_id, {})

        try:
            timestamp = int(time.time() * 1000)
            url = f"https://sspai.com/api/v1/article/tag/page/get?limit=30&offset=0&created_at={timestamp}&tag=%E7%83%AD%E9%97%A8%E6%96%87%E7%AB%A0&released=false"
            headers = {
                **cls.DEFAULT_HEADERS,
                "Referer": "https://sspai.com/",
            }

            data = await cls._fetch_json(url, headers)

            if not data:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "少数派"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", [])[:30]:
                title = item.get("title", "")
                article_id = item.get("id", "")
                if not title or not article_id:
                    continue

                items.append(NewsItem(
                    id=str(article_id),
                    title=title,
                    url=f"https://sspai.com/post/{article_id}",
                    extra={"info": item.get("author", {}).get("nickname", "")} if item.get("author") else None,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "少数派"),
                updated_time=int(time.time()),
                items=items,
            )

        except Exception as e:
            logger.error(f"获取少数派热门失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "少数派"),
                updated_time=int(time.time()),
                message=str(e),
            )


class FastbullService(HotNewsService):
    """法布财经"""

    @classmethod
    async def get_express(cls) -> SourceResponse:
        """获取法布财经快讯"""
        source_id = "fastbull-express"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://www.fastbull.com/cn/express-news"
            html = await cls._fetch(url)

            if not html:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "法布财经"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            soup = BeautifulSoup(html, "lxml")
            items = []

            for item in soup.select(".news-list")[:30]:
                title_elem = item.select_one(".title_name")
                if not title_elem:
                    continue

                href = title_elem.get("href", "")
                title_text = title_elem.get_text(strip=True)

                # 提取【】中的标题
                match = re.match(r"【(.+)】", title_text)
                title = match.group(1) if match else title_text

                # 获取时间
                date = item.get("data-date", "")

                if not title or not href:
                    continue

                items.append(NewsItem(
                    id=href.split("/")[-1] if href else title,
                    title=title if len(title) >= 4 else title_text,
                    url=f"https://www.fastbull.com{href}" if href.startswith("/") else href,
                    pub_date=int(date) if date.isdigit() else None,
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "法布财经"),
                updated_time=int(time.time()),
                items=items[:30],
            )

        except Exception as e:
            logger.error(f"获取法布财经快讯失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "法布财经"),
                updated_time=int(time.time()),
                message=str(e),
            )


class MktnewsService(HotNewsService):
    """MKTNews"""

    @classmethod
    async def get_flash(cls) -> SourceResponse:
        """获取 MKTNews 快讯"""
        source_id = "mktnews-flash"
        source_info = SOURCES.get(source_id, {})

        try:
            url = "https://api.mktnews.net/api/flash?type=0&limit=50"
            headers = {
                **cls.DEFAULT_HEADERS,
                "Referer": "https://mktnews.net/",
            }

            data = await cls._fetch_json(url, headers)

            if not data or data.get("status") != 0:
                return SourceResponse(
                    status="error",
                    source_id=source_id,
                    source_name=source_info.get("name", "MKTNews"),
                    updated_time=int(time.time()),
                    message="请求失败",
                )

            items = []
            for item in data.get("data", [])[:30]:
                content = item.get("data", {})
                title = content.get("title") or content.get("content", "")

                if not title:
                    continue

                # 提取【】中的标题
                match = re.match(r"^【([^】]*)】(.*)$", content.get("content", ""))
                if match and not content.get("title"):
                    title = match.group(1)

                items.append(NewsItem(
                    id=str(item.get("id", "")),
                    title=title[:100] if len(title) > 100 else title,
                    url=f"https://mktnews.net/flashDetail.html?id={item.get('id')}",
                    pub_date=int(item.get("time", 0)) if item.get("time") else None,
                    extra={
                        "hover": content.get("content", ""),
                        "info": "Important" if item.get("important") == 1 else None,
                    },
                ))

            return SourceResponse(
                status="success",
                source_id=source_id,
                source_name=source_info.get("name", "MKTNews"),
                updated_time=int(time.time()),
                items=items,
            )

        except Exception as e:
            logger.error(f"获取 MKTNews 快讯失败: {str(e)}")
            return SourceResponse(
                status="error",
                source_id=source_id,
                source_name=source_info.get("name", "MKTNews"),
                updated_time=int(time.time()),
                message=str(e),
            )


# 数据源服务映射
SOURCE_GETTERS: Dict[str, Callable] = {
    # 财经类
    "xueqiu": XueqiuService.get_hot_stock,
    "jin10": Jin10Service.get_flash,
    "wallstreetcn-quick": WallstreetcnService.get_quick,
    "wallstreetcn-news": WallstreetcnService.get_news,
    "wallstreetcn-hot": WallstreetcnService.get_hot,
    "gelonghui": GelonghuiService.get_events,
    "cls-telegraph": ClsService.get_telegraph,
    "cls-hot": ClsService.get_hot,
    "fastbull-express": FastbullService.get_express,
    "mktnews-flash": MktnewsService.get_flash,
    # 综合类
    "weibo": WeiboService.get_hot_search,
    "zhihu": ZhihuService.get_hot_list,
    "baidu": BaiduService.get_hot,
    "toutiao": ToutiaoService.get_hot,
    "douyin": DouyinService.get_hot,
    "thepaper": ThepaperService.get_hot,
    # 科技类
    "ithome": IthomeService.get_hot,
    "juejin": JuejinService.get_hot,
    "hackernews": HackerNewsService.get_top,
    "github-trending": GithubTrendingService.get_trending,
    "v2ex-share": V2exService.get_latest,
    "sspai": SspaiService.get_hot,
}


async def get_hot_news(source_id: str) -> SourceResponse:
    """获取指定数据源的热门新闻"""
    if source_id not in SOURCE_GETTERS:
        return SourceResponse(
            status="error",
            source_id=source_id,
            source_name="Unknown",
            updated_time=int(time.time()),
            message=f"不支持的数据源: {source_id}",
        )

    getter = SOURCE_GETTERS[source_id]
    return await getter()


async def get_hot_news_batch(source_ids: List[str]) -> Dict[str, SourceResponse]:
    """批量获取多个数据源的热门新闻"""
    results = {}
    for source_id in source_ids:
        if source_id in SOURCE_GETTERS:
            results[source_id] = await get_hot_news(source_id)
    return results


def get_all_sources() -> List[Dict[str, Any]]:
    """获取所有数据源列表"""
    return [
        {
            "id": source_id,
            "name": info.get("name", ""),
            "title": info.get("title", ""),
            "column": info.get("column", ""),
            "color": info.get("color", ""),
            "type": info.get("type", ""),
            "available": source_id in SOURCE_GETTERS,
        }
        for source_id, info in SOURCES.items()
    ]


def get_sources_by_column(column: str) -> List[Dict[str, Any]]:
    """按分类获取数据源

    支持的分类:
    - finance: 财经
    - china: 国内/综合
    - tech: 科技
    - world: 国际
    - hottest: 最热（所有 type=hottest 的数据源）
    - realtime: 实时（所有 type=realtime 的数据源）
    """
    # 特殊分类：hottest 和 realtime
    if column == "hottest":
        return [
            {
                "id": source_id,
                "name": info.get("name", ""),
                "title": info.get("title", ""),
                "color": info.get("color", ""),
                "type": info.get("type", ""),
                "column": info.get("column", ""),
                "available": source_id in SOURCE_GETTERS,
            }
            for source_id, info in SOURCES.items()
            if info.get("type") == "hottest"
        ]

    if column == "realtime":
        return [
            {
                "id": source_id,
                "name": info.get("name", ""),
                "title": info.get("title", ""),
                "color": info.get("color", ""),
                "type": info.get("type", ""),
                "column": info.get("column", ""),
                "available": source_id in SOURCE_GETTERS,
            }
            for source_id, info in SOURCES.items()
            if info.get("type") == "realtime"
        ]

    # 普通分类：按 column 筛选
    return [
        {
            "id": source_id,
            "name": info.get("name", ""),
            "title": info.get("title", ""),
            "color": info.get("color", ""),
            "type": info.get("type", ""),
            "column": info.get("column", ""),
            "available": source_id in SOURCE_GETTERS,
        }
        for source_id, info in SOURCES.items()
        if info.get("column") == column
    ]