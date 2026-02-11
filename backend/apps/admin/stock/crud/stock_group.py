#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/08
# @File           : stock_group.py
# @IDE            : PyCharm
# @desc           : 股票分组数据库 增删改查操作

from typing import Any
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from apps.admin.stock import models, schemas


class StockGroupDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(StockGroupDal, self).__init__()
        self.db = db
        self.model = models.StockGroup
        self.schema = schemas.StockGroupOut

    async def create_data(
            self,
            data: schemas.StockGroupCreate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建股票分组
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        """
        obj = self.model(**data.model_dump())
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.StockGroupUpdate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新股票分组
        :param data_id:
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        """
        obj = await self.get_data(data_id, v_options=v_options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
        """
        删除股票分组
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        return await super(StockGroupDal, self).delete_datas(ids, v_soft, **kwargs)

    async def get_by_user_id(self, user_id: int, v_include_children: bool = False) -> list:
        """
        根据用户ID获取分组列表
        :param user_id: 用户ID
        :param v_include_children: 是否包含子分组
        :return: 分组列表
        """
        sql = select(self.model).where(
            self.model.user_id == user_id,
            self.model.is_delete == False
        ).order_by(
            self.model.order.asc(),
            self.model.created_at.desc()
        )
        queryset = await self.db.scalars(sql)
        return [schemas.StockGroupOut.model_validate(i).model_dump() for i in queryset.all()]

    async def get_tree_by_user_id(self, user_id: int) -> list:
        """
        根据用户ID获取分组树
        :param user_id: 用户ID
        :return: 分组树
        """
        # 获取所有分组
        sql = select(self.model).where(
            self.model.user_id == user_id,
            self.model.is_delete == False
        ).order_by(
            self.model.order.asc(),
            self.model.created_at.desc()
        )
        queryset = await self.db.scalars(sql)
        all_groups = [schemas.StockGroupOut.model_validate(i).model_dump() for i in queryset.all()]

        # 构建树形结构
        def build_tree(groups, parent_id=None):
            tree = []
            for group in groups:
                if group['parent_id'] == parent_id:
                    children = build_tree(groups, group['id'])
                    if children:
                        group['children'] = children
                    tree.append(group)
            return tree

        return build_tree(all_groups)

    async def get_by_name(self, user_id: int, name: str) -> Any:
        """
        根据用户ID和分组名称获取分组
        :param user_id: 用户ID
        :param name: 分组名称
        :return: 分组对象
        """
        sql = select(self.model).where(
            self.model.user_id == user_id,
            self.model.name == name,
            self.model.is_delete == False
        )
        result = await self.db.execute(sql)
        return result.scalar_one_or_none()

    async def update_status(self, data_id: int, status: int) -> None:
        """
        更新分组状态
        :param data_id: 分组ID
        :param status: 状态
        """
        await self.db.execute(
            update(self.model)
            .where(self.model.id == data_id)
            .values(status=status)
        )
