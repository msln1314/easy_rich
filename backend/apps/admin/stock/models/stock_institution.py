#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_institution.py
# @IDE            : PyCharm
# @desc           : 股票机构持仓模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Integer, Index


class StockInstitution(BaseModel):
    """机构持仓数据模型"""

    __tablename__ = "stock_institution"
    __table_args__ = (
        Index("idx_stock_code_date", "stock_code", "report_date"),
        Index("idx_stock_code", "stock_code"),
        Index("idx_report_date", "report_date"),
        Index("idx_institution_type", "institution_type"),
        {"comment": "机构持仓数据表"},
    )

    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="股票名称"
    )

    report_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="报告期"
    )
    institution_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="机构类型: 基金/社保/QFII/保险等"
    )

    institution_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="机构名称"
    )
    holding_shares: Mapped[float] = mapped_column(
        Float, nullable=False, comment="持有股份(股)"
    )
    holding_ratio: Mapped[float] = mapped_column(
        Float, nullable=False, comment="持股比例(%)"
    )

    change_shares: Mapped[float] = mapped_column(
        Float, nullable=False, comment="持股变化(股)"
    )
    change_ratio: Mapped[float] = mapped_column(
        Float, nullable=False, comment="持股变化比例(%)"
    )

    holding_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="持有市值(元)"
    )
    change_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="市值变化(元)"
    )

    quarter: Mapped[str | None] = mapped_column(
        String(10), nullable=True, comment="季度: Q1/Q2/Q3/Q4"
    )


class StockInstitutionSummary(BaseModel):
    """机构持仓汇总模型"""

    __tablename__ = "stock_institution_summary"
    __table_args__ = (
        Index("idx_stock_code", "stock_code"),
        Index("idx_report_date", "report_date"),
        {"comment": "机构持仓汇总表"},
    )

    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="股票名称"
    )

    report_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="报告期"
    )

    fund_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="基金持股家数"
    )
    fund_shares: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="基金持股总数(股)"
    )
    fund_ratio: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="基金持股比例(%)"
    )
    fund_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="基金持股市值(元)"
    )

    social_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="社保持股家数"
    )
    social_shares: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="社保持股总数(股)"
    )
    social_ratio: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="社保持股比例(%)"
    )

    qfii_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="QFII持股家数"
    )
    qfii_shares: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="QFII持股总数(股)"
    )
    qfii_ratio: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="QFII持股比例(%)"
    )

    insurance_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="保险持股家数"
    )
    insurance_shares: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="保险持股总数(股)"
    )
    insurance_ratio: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="保险持股比例(%)"
    )

    total_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="机构总家数"
    )
    total_shares: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="机构持股总数(股)"
    )
    total_ratio: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="机构持股比例(%)"
    )
