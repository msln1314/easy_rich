#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/21
# @File           : stock_north_money.py
# @IDE            : PyCharm
# @desc           : 北向资金流向模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Index, UniqueConstraint


class StockNorthMoney(BaseModel):
    """
    北向资金流向表
    存储沪深股通资金流入流出数据
    每日更新，记录历史流向
    """

    __tablename__ = "stock_north_money"
    __table_args__ = (
        UniqueConstraint("trade_date", name="uk_north_money_trade_date"),
        Index("idx_trade_date", "trade_date"),
        Index("idx_created_at", "created_at"),
        {"comment": "北向资金流向表"},
    )

    # 交易日期
    trade_date: Mapped[date] = mapped_column(
        DateTime, nullable=False, comment="交易日期"
    )

    # 沪股通数据
    sh_buy_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="沪股通买入金额(元)"
    )
    sh_sell_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="沪股通卖出金额(元)"
    )
    sh_net_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="沪股通净买入金额(元)"
    )

    # 深股通数据
    sz_buy_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="深股通买入金额(元)"
    )
    sz_sell_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="深股通卖出金额(元)"
    )
    sz_net_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="深股通净买入金额(元)"
    )

    # 合计数据
    total_buy_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="合计买入金额(元)"
    )
    total_sell_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="合计卖出金额(元)"
    )
    total_net_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="合计净买入金额(元)"
    )

    # 时间信息
    data_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="数据时间（采集时间）"
    )

    # 数据来源
    data_from: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="stock_service", comment="数据来源"
    )


class StockNorthMoneyRealtime(BaseModel):
    """
    实时北向资金表
    存储当日实时北向资金数据
    交易时段实时更新
    """

    __tablename__ = "stock_north_money_realtime"
    __table_args__ = (
        Index("idx_data_date", "data_date"),
        Index("idx_data_time", "data_time"),
        {"comment": "实时北向资金表"},
    )

    # 数据日期
    data_date: Mapped[date] = mapped_column(
        DateTime, nullable=False, comment="数据日期"
    )

    # 沪股通数据
    sh_buy_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="沪股通买入金额(元)"
    )
    sh_sell_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="沪股通卖出金额(元)"
    )
    sh_net_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="沪股通净买入金额(元)"
    )

    # 深股通数据
    sz_buy_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="深股通买入金额(元)"
    )
    sz_sell_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="深股通卖出金额(元)"
    )
    sz_net_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="深股通净买入金额(元)"
    )

    # 合计数据
    total_buy_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="合计买入金额(元)"
    )
    total_sell_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="合计卖出金额(元)"
    )
    total_net_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="合计净买入金额(元)"
    )

    # 时间信息
    data_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="数据时间"
    )

    # 数据来源
    data_from: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="stock_service", comment="数据来源"
    )
