#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/03/22
# @File           : rule_crud.py
# @IDE            : PyCharm
# @desc           : 雷区基线规则数据库 增删改查操作

import json
from datetime import datetime, timedelta
from typing import Any, Optional, List
from sqlalchemy.orm.strategy_options import _AbstractLoad
from sqlalchemy import select, update
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from apps.admin.review import models, schemas


class RuleDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(RuleDal, self).__init__()
        self.db = db
        self.model = models.RiskRule
        self.schema = schemas.RuleOut

    async def out_dict(self, obj, v_options=None, v_return_obj=False, v_schema=None):
        result = await super().out_dict(obj, v_options, v_return_obj, v_schema)
        if isinstance(result, dict) and obj.check_timing:
            result["check_timing"] = json.loads(obj.check_timing)
        if isinstance(result, dict) and obj.check_condition:
            result["check_condition"] = json.loads(obj.check_condition)
        return result

    async def create_data(
        self,
        data: schemas.RuleCreate,
        user_id: int,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        obj = self.model(
            user_id=user_id,
            rule_type=data.rule_type,
            category=data.category,
            name=data.name,
            description=data.description,
            severity=data.severity,
            check_timing=json.dumps(data.check_timing) if data.check_timing else None,
            check_condition=json.dumps(data.check_condition)
            if data.check_condition
            else None,
            is_active=data.is_active,
        )
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
        self,
        data_id: int,
        data: schemas.RuleUpdate,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        obj = await self.get_data(data_id, v_options=v_options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            if value is not None:
                if key in ["check_timing", "check_condition"]:
                    setattr(obj, key, json.dumps(value) if value else None)
                else:
                    setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def delete_datas(
        self, ids: list[int], v_soft: bool = False, **kwargs
    ) -> None:
        return await super(RuleDal, self).delete_datas(ids, v_soft, **kwargs)

    async def get_active_rules(
        self, user_id: Optional[int] = None, rule_type: Optional[str] = None
    ) -> list:
        sql = select(self.model).where(self.model.is_active == 1)
        if user_id:
            sql = sql.where(self.model.user_id == user_id)
        if rule_type:
            sql = sql.where(self.model.rule_type == rule_type)
        queryset = await self.db.scalars(sql)
        return [self._format_output(i) for i in queryset.all()]

    async def get_by_type(self, user_id: int, rule_type: str) -> list:
        sql = (
            select(self.model)
            .where(self.model.user_id == user_id, self.model.rule_type == rule_type)
            .order_by(self.model.created_at.desc())
        )
        queryset = await self.db.scalars(sql)
        return [self._format_output(i) for i in queryset.all()]

    async def update_active_status(self, rule_id: int, is_active: int) -> None:
        await self.db.execute(
            update(self.model)
            .where(self.model.id == rule_id)
            .values(is_active=is_active)
        )

    def _format_output(self, obj) -> dict:
        result = schemas.RuleOut.model_validate(obj).model_dump()
        if obj.check_timing:
            result["check_timing"] = json.loads(obj.check_timing)
        if obj.check_condition:
            result["check_condition"] = json.loads(obj.check_condition)
        return result


class ViolationDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(ViolationDal, self).__init__()
        self.db = db
        self.model = models.RuleViolation
        self.schema = schemas.ViolationOut

    async def create_violation(
        self,
        user_id: int,
        rule_id: int,
        violation_time: datetime,
        violation_context: Optional[dict] = None,
        related_stock_code: Optional[str] = None,
        related_trade_id: Optional[int] = None,
        user_note: Optional[str] = None,
    ) -> dict:
        obj = self.model(
            user_id=user_id,
            rule_id=rule_id,
            violation_time=violation_time,
            violation_context=json.dumps(violation_context)
            if violation_context
            else None,
            related_stock_code=related_stock_code,
            related_trade_id=related_trade_id,
            user_note=user_note,
        )
        await self.flush(obj)
        return schemas.ViolationOut.model_validate(obj).model_dump()

    async def get_by_rule_id(self, rule_id: int, limit: int = 50) -> list:
        sql = select(self.model).where(self.model.rule_id == rule_id)
        sql = sql.order_by(self.model.violation_time.desc()).limit(limit)
        queryset = await self.db.scalars(sql)
        return [self._format_output(i) for i in queryset.all()]

    async def get_by_user_id(self, user_id: int, limit: int = 50) -> list:
        sql = select(self.model).where(self.model.user_id == user_id)
        sql = sql.order_by(self.model.violation_time.desc()).limit(limit)
        queryset = await self.db.scalars(sql)
        return [self._format_output(i) for i in queryset.all()]

    async def get_recent_violations(self, user_id: int, days: int = 7) -> list:
        start_time = datetime.now() - timedelta(days=days)
        sql = (
            select(self.model)
            .where(
                self.model.user_id == user_id, self.model.violation_time >= start_time
            )
            .order_by(self.model.violation_time.desc())
        )
        queryset = await self.db.scalars(sql)
        return [self._format_output(i) for i in queryset.all()]

    def _format_output(self, obj) -> dict:
        result = schemas.ViolationOut.model_validate(obj).model_dump()
        if obj.violation_context:
            result["violation_context"] = json.loads(obj.violation_context)
        return result
