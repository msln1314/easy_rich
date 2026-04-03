#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2026/4/4
# @File : report.py
# @IDE : PyCharm
# @desc : 回测报告模型

from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, Integer, Text, JSON, Float


class BacktestReport(BaseModel):
    """回测报告表"""
    __tablename__ = "backtest_report"
    __table_args__ = (
        {"comment": "回测报告表"},
    )

    strategy_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="关联策略ID")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="执行者ID")
    backtest_config: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="回测配置")
    metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="收益指标")
    risk_metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="风险指标")
    trades: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="交易记录明细")
    equity_curve: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="权益曲线数据点")
    benchmark_comparison: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="基准对比结果")
    report_file: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="报告文件路径")
    execution_time: Mapped[float | None] = mapped_column(Float, nullable=True, comment="回测耗时(秒)")
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="running",
        comment="状态: running/completed/failed"
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True, comment="错误信息")