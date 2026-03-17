# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : watchlist_service.py
# @IDE            : PyCharm
# @desc           : 自选股管理服务 - 添加、删除、分组管理

import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field, asdict
import aiofiles
import asyncio

from app.core.logging import get_logger
from app.core.config import settings

logger = get_logger(__name__)

WATCHLIST_FILE = "data/watchlist.json"


@dataclass
class WatchlistItem:
    stock_code: str
    stock_name: str
    add_time: str
    group: str = "default"
    notes: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class WatchlistGroup:
    name: str
    created_time: str
    stocks: List[str] = field(default_factory=list)


class WatchlistService:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(WATCHLIST_FILE):
            self._save_data({"groups": {}, "stocks": {}})

    def _load_data(self) -> Dict[str, Any]:
        try:
            with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"groups": {}, "stocks": {}}

    def _save_data(self, data: Dict[str, Any]):
        with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    async def add_stock(
        self,
        stock_code: str,
        stock_name: str,
        group: str = "default",
        notes: str = "",
        tags: List[str] = None,
    ) -> WatchlistItem:
        async with self._lock:
            data = self._load_data()

            item = WatchlistItem(
                stock_code=stock_code,
                stock_name=stock_name,
                add_time=datetime.now().isoformat(),
                group=group,
                notes=notes,
                tags=tags or [],
            )

            data["stocks"][stock_code] = asdict(item)

            if group not in data["groups"]:
                data["groups"][group] = {
                    "name": group,
                    "created_time": datetime.now().isoformat(),
                    "stocks": [],
                }

            if stock_code not in data["groups"][group]["stocks"]:
                data["groups"][group]["stocks"].append(stock_code)

            self._save_data(data)
            logger.info(f"添加自选股: {stock_code} {stock_name}")
            return item

    async def remove_stock(self, stock_code: str) -> bool:
        async with self._lock:
            data = self._load_data()

            if stock_code not in data["stocks"]:
                return False

            group = data["stocks"][stock_code].get("group", "default")
            del data["stocks"][stock_code]

            if group in data["groups"]:
                if stock_code in data["groups"][group]["stocks"]:
                    data["groups"][group]["stocks"].remove(stock_code)

            self._save_data(data)
            logger.info(f"删除自选股: {stock_code}")
            return True

    async def get_all_stocks(self) -> List[WatchlistItem]:
        data = self._load_data()
        return [WatchlistItem(**item) for item in data["stocks"].values()]

    async def get_stocks_by_group(self, group: str) -> List[WatchlistItem]:
        data = self._load_data()

        if group not in data["groups"]:
            return []

        stocks = []
        for code in data["groups"][group].get("stocks", []):
            if code in data["stocks"]:
                stocks.append(WatchlistItem(**data["stocks"][code]))

        return stocks

    async def get_all_groups(self) -> List[WatchlistGroup]:
        data = self._load_data()
        return [WatchlistGroup(**g) for g in data["groups"].values()]

    async def create_group(self, name: str) -> WatchlistGroup:
        async with self._lock:
            data = self._load_data()

            if name in data["groups"]:
                raise ValueError(f"分组已存在: {name}")

            group = WatchlistGroup(
                name=name, created_time=datetime.now().isoformat(), stocks=[]
            )

            data["groups"][name] = asdict(group)
            self._save_data(data)
            logger.info(f"创建分组: {name}")
            return group

    async def delete_group(self, name: str) -> bool:
        if name == "default":
            raise ValueError("不能删除默认分组")

        async with self._lock:
            data = self._load_data()

            if name not in data["groups"]:
                return False

            for code in data["groups"][name].get("stocks", []):
                if code in data["stocks"]:
                    data["stocks"][code]["group"] = "default"
                    if "default" in data["groups"]:
                        data["groups"]["default"]["stocks"].append(code)

            del data["groups"][name]
            self._save_data(data)
            logger.info(f"删除分组: {name}")
            return True

    async def move_stock(self, stock_code: str, new_group: str) -> bool:
        async with self._lock:
            data = self._load_data()

            if stock_code not in data["stocks"]:
                return False

            old_group = data["stocks"][stock_code].get("group", "default")

            if old_group in data["groups"]:
                if stock_code in data["groups"][old_group]["stocks"]:
                    data["groups"][old_group]["stocks"].remove(stock_code)

            if new_group not in data["groups"]:
                data["groups"][new_group] = {
                    "name": new_group,
                    "created_time": datetime.now().isoformat(),
                    "stocks": [],
                }

            data["stocks"][stock_code]["group"] = new_group
            data["groups"][new_group]["stocks"].append(stock_code)

            self._save_data(data)
            logger.info(f"移动股票 {stock_code} 到分组 {new_group}")
            return True

    async def update_notes(self, stock_code: str, notes: str) -> bool:
        async with self._lock:
            data = self._load_data()

            if stock_code not in data["stocks"]:
                return False

            data["stocks"][stock_code]["notes"] = notes
            self._save_data(data)
            return True

    async def add_tag(self, stock_code: str, tag: str) -> bool:
        async with self._lock:
            data = self._load_data()

            if stock_code not in data["stocks"]:
                return False

            if tag not in data["stocks"][stock_code]["tags"]:
                data["stocks"][stock_code]["tags"].append(tag)
                self._save_data(data)

            return True

    async def remove_tag(self, stock_code: str, tag: str) -> bool:
        async with self._lock:
            data = self._load_data()

            if stock_code not in data["stocks"]:
                return False

            if tag in data["stocks"][stock_code]["tags"]:
                data["stocks"][stock_code]["tags"].remove(tag)
                self._save_data(data)

            return True

    async def search_by_tag(self, tag: str) -> List[WatchlistItem]:
        data = self._load_data()
        result = []

        for item in data["stocks"].values():
            if tag in item.get("tags", []):
                result.append(WatchlistItem(**item))

        return result


watchlist_service = WatchlistService()
