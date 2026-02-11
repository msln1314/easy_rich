#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/08
# @File           : sys_user_stock_group.py
# @IDE            : PyCharm
# @desc           : 用户股票分组关联数据库 增删改查操作

from typing import Any
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update, and_, func
from apps.admin.stock import models, schemas
from datetime import date

class SysUserStockGroupDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SysUserStockGroupDal, self).__init__()
        self.db = db
        self.model = models.SysUserStockGroup
        self.schema = schemas.SysUserStockGroupOut

    async def create_data(
            self,
            data: schemas.SysUserStockGroupCreate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建用户股票分组关联
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
            data: schemas.SysUserStockGroupUpdate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新用户股票分组关联
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
        删除用户股票分组关联
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        return await super(SysUserStockGroupDal, self).delete_datas(ids, v_soft, **kwargs)

    async def get_by_user_id(self, user_id: int, group_id: int | None = None) -> list:
        """
        根据用户ID获取关联列表
        :param user_id: 用户ID
        :param group_id: 分组ID（可选）
        :return: 关联列表
        """
        conditions = [
            self.model.user_id == user_id
        ]
        if group_id is not None:
            conditions.append(self.model.group_id == group_id)

        sql = select(self.model).where(and_(*conditions))
        queryset = await self.db.scalars(sql)
        return [schemas.SysUserStockGroupOut.model_validate(i).model_dump() for i in queryset.all()]

    async def get_my_stocks(self, user_id: int, group_id: int | None = None) -> list:
        """
        获取我的自选股列表
        :param user_id: 用户ID
        :param group_id: 分组ID（可选）
        :return: 自选股列表
        """
        from apps.admin.stock.models import StockBasicInfo, StockGroup, StockRealtime

        # 基础查询
        query = (
            select(
                self.model.id,
                StockBasicInfo.stock_code,
                StockBasicInfo.name.label('stock_name'),
                StockRealtime.current_price,
                StockRealtime.change_percent,
                StockRealtime.change_amount,
                StockRealtime.volume,
                StockRealtime.amount,
                StockRealtime.high_price,
                StockRealtime.low_price,
                StockRealtime.open_price,
                StockRealtime.previous_close,
                StockRealtime.pe_ratio,
                StockRealtime.pb_ratio,
                StockRealtime.total_market_cap,
                StockRealtime.circulating_market_cap,
                StockRealtime.turnover_rate,
                StockRealtime.volume_ratio,
                StockRealtime.ma5,
                StockRealtime.ma10,
                StockRealtime.ma20,
                StockRealtime.ma30,
                StockRealtime.rsi,
                StockRealtime.macd_diff,
                StockRealtime.macd_dea,
                StockRealtime.macd_bar,
                StockRealtime.limit_up,
                StockRealtime.limit_down,
                StockRealtime.is_limit_up,
                StockRealtime.is_limit_down,
                StockRealtime.is_trading,
                self.model.stock_id,
                self.model.group_id,
                StockGroup.name.label('group_name'),
                self.model.created_at
            )
            .select_from(self.model.__table__)
            .outerjoin(StockBasicInfo, self.model.stock_id == StockBasicInfo.id)
            .outerjoin(StockGroup, self.model.group_id == StockGroup.id)
            .outerjoin(StockRealtime, and_(
                StockRealtime.stock_code == StockBasicInfo.stock_code,
                StockRealtime.trade_date == date.today()
            ))
            .where(
                and_(
                    self.model.user_id == user_id
                )
            )
        )

        # 按分组筛选
        if group_id is not None:
            query = query.where(self.model.group_id == group_id)

        query = query.order_by(StockGroup.order.asc(), self.model.created_at.desc())

        result = await self.db.execute(query)
        rows = result.all()

        # 转换为字典列表
        stocks = []
        for row in rows:
            stock = {
                'id': row.id,
                'stock_id': row.stock_id,
                'stock_code': row.stock_code,
                'stock_name': row.stock_name,
                'current_price': float(row.current_price) if row.current_price else None,
                'change_percent': float(row.change_percent) if row.change_percent else None,
                'change_amount': float(row.change_amount) if row.change_amount else None,
                'volume': float(row.volume) if row.volume else None,
                'amount': float(row.amount) if row.amount else None,
                'high_price': float(row.high_price) if row.high_price else None,
                'low_price': float(row.low_price) if row.low_price else None,
                'open_price': float(row.open_price) if row.open_price else None,
                'previous_close': float(row.previous_close) if row.previous_close else None,
                'pe_ratio': float(row.pe_ratio) if row.pe_ratio else None,
                'pb_ratio': float(row.pb_ratio) if row.pb_ratio else None,
                'total_market_cap': float(row.total_market_cap) if row.total_market_cap else None,
                'circulating_market_cap': float(row.circulating_market_cap) if row.circulating_market_cap else None,
                'turnover_rate': float(row.turnover_rate) if row.turnover_rate else None,
                'volume_ratio': float(row.volume_ratio) if row.volume_ratio else None,
                'ma5': float(row.ma5) if row.ma5 else None,
                'ma10': float(row.ma10) if row.ma10 else None,
                'ma20': float(row.ma20) if row.ma20 else None,
                'ma30': float(row.ma30) if row.ma30 else None,
                'rsi': float(row.rsi) if row.rsi else None,
                'macd_diff': float(row.macd_diff) if row.macd_diff else None,
                'macd_dea': float(row.macd_dea) if row.macd_dea else None,
                'macd_bar': float(row.macd_bar) if row.macd_bar else None,
                'limit_up': float(row.limit_up) if row.limit_up else None,
                'limit_down': float(row.limit_down) if row.limit_down else None,
                'is_limit_up': row.is_limit_up,
                'is_limit_down': row.is_limit_down,
                'is_trading': row.is_trading,
                'group_id': row.group_id,
                'group_name': row.group_name,
                'created_at': row.created_at.isoformat() if row.created_at else None
            }
            stocks.append(stock)

        return stocks

    async def add_stocks_to_group(self, user_id: int, group_id: int, stock_ids:  list[int] ) -> None:
        """
        添加股票到分组
        :param user_id: 用户ID
        :param group_id: 分组ID
        :param stock_id: 股票ID
        """
        # 检查是否已存在,找出已经存在的股票列表

        existing = await self.db.scalars(
            select(self.model).where(
                and_(
                    self.model.user_id == user_id,
                    self.model.group_id == group_id,
                    self.model.stock_id.in_(stock_ids)
                )
            )
        )
        # 转换为字典列表
        existing_list = existing.all()
        print(existing_list)
        existing_stocks = [i.stock_id for i in existing_list if i is not None]


        # 过滤出需要添加的股票
        stocks_to_add = [stock_id for stock_id in stock_ids if stock_id not in existing_stocks]

        # 创建新的关联
        for stock_id in stocks_to_add:
            obj = self.model(user_id=user_id, group_id=group_id, stock_id=stock_id)
            self.db.add(obj)
        await self.flush()
      

    async def remove_stock_from_group(self, user_id: int, group_id: int | None = None, stock_id: int | None = None) -> None:
        """
        从分组中移除股票
        :param user_id: 用户ID
        :param group_id: 分组ID（可选）
        :param stock_id: 股票ID（可选）
        """
        conditions = [
            self.model.user_id == user_id
        ]

        if group_id is not None:
            conditions.append(self.model.group_id == group_id)
        if stock_id is not None:
            conditions.append(self.model.stock_id == stock_id)

        # 直接删除记录
        from sqlalchemy import delete
        await self.db.execute(
            delete(self.model).where(and_(*conditions))
        )

    async def move_stock_to_group(self, user_id: int, from_group_id: int, to_group_id: int, stock_id: int) -> None:
        """
        移动股票到其他分组
        :param user_id: 用户ID
        :param from_group_id: 原分组ID
        :param to_group_id: 目标分组ID
        :param stock_id: 股票ID
        """
        await self.db.execute(
            update(self.model)
            .where(
                and_(
                    self.model.user_id == user_id,
                    self.model.group_id == from_group_id,
                    self.model.stock_id == stock_id
                )
            )
            .values(group_id=to_group_id)
        )

    async def get_stock_count_by_group(self, user_id: int) -> list:
        """
        获取各分组的股票数量
        :param user_id: 用户ID
        :return: 分组股票数量列表
        """
        from apps.admin.stock.models import StockGroup

        query = (
            select(
                self.model.group_id,
                StockGroup.name,
                func.count(self.model.id).label('stock_count')
            )
            .select_from(self.model.__table__)
            .outerjoin(StockGroup, self.model.group_id == StockGroup.id)
            .where(
                self.model.user_id == user_id
            )
            .group_by(self.model.group_id, StockGroup.name)
        )

        result = await self.db.execute(query)
        rows = result.all()

        return [
            {
                'group_id': row.group_id,
                'group_name': row.name,
                'stock_count': row.stock_count
            }
            for row in rows
        ]
