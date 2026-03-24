#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/03/22
# @File           : experience_crud.py
# @IDE            : PyCharm
# @desc           : 心得经验数据库 增删改查操作

import json
from typing import Any, Optional, List
from sqlalchemy.orm.strategy_options import _AbstractLoad
from sqlalchemy import select, update
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from apps.admin.review import models, schemas


class ExperienceDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(ExperienceDal, self).__init__()
        self.db = db
        self.model = models.ExperienceNote
        self.schema = schemas.ExperienceOut

    async def create_data(
        self,
        data: schemas.ExperienceCreate,
        user_id: int,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        obj = self.model(
            user_id=user_id,
            title=data.title,
            content=data.content,
            category=data.category,
            tags=json.dumps(data.tags) if data.tags else None,
            related_stocks=json.dumps(data.related_stocks)
            if data.related_stocks
            else None,
            related_trades=json.dumps(data.related_trades)
            if data.related_trades
            else None,
            related_review_id=data.related_review_id,
            mood=data.mood,
            importance=data.importance,
        )
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
        self,
        data_id: int,
        data: schemas.ExperienceUpdate,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        obj = await self.get_data(data_id, v_options=v_options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            if value is not None:
                if key in ["tags", "related_stocks", "related_trades"]:
                    setattr(obj, key, json.dumps(value) if value else None)
                else:
                    setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def delete_datas(
        self, ids: list[int], v_soft: bool = False, **kwargs
    ) -> None:
        return await super(ExperienceDal, self).delete_datas(ids, v_soft, **kwargs)

    async def get_by_user_id(self, user_id: int, limit: int = 20) -> list:
        sql = select(self.model).where(self.model.user_id == user_id)
        sql = sql.order_by(self.model.created_at.desc()).limit(limit)
        queryset = await self.db.scalars(sql)
        return [self._format_output(i) for i in queryset.all()]

    async def get_by_category(self, user_id: int, category: str) -> list:
        sql = (
            select(self.model)
            .where(self.model.user_id == user_id, self.model.category == category)
            .order_by(self.model.created_at.desc())
        )
        queryset = await self.db.scalars(sql)
        return [self._format_output(i) for i in queryset.all()]

    async def get_by_tags(self, user_id: int, tags: List[str]) -> list:
        results = []
        sql = select(self.model).where(self.model.user_id == user_id)
        queryset = await self.db.scalars(sql)
        for item in queryset.all():
            if item.tags:
                item_tags = json.loads(item.tags)
                if any(tag in item_tags for tag in tags):
                    results.append(self._format_output(item))
        return results

    async def increment_view_count(self, note_id: int) -> None:
        await self.db.execute(
            update(self.model)
            .where(self.model.id == note_id)
            .values(view_count=self.model.view_count + 1)
        )

    async def search_content(self, user_id: int, keyword: str) -> list:
        sql = (
            select(self.model)
            .where(
                self.model.user_id == user_id, self.model.content.like(f"%{keyword}%")
            )
            .order_by(self.model.created_at.desc())
        )
        queryset = await self.db.scalars(sql)
        return [self._format_output(i) for i in queryset.all()]

    def _format_output(self, obj) -> dict:
        result = schemas.ExperienceOut.model_validate(obj).model_dump()
        if obj.tags:
            result["tags"] = json.loads(obj.tags)
        if obj.related_stocks:
            result["related_stocks"] = json.loads(obj.related_stocks)
        if obj.related_trades:
            result["related_trades"] = json.loads(obj.related_trades)
        return result
