from datetime import date
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Text, Float, Integer, SmallInteger, Index
from db.db_base import BaseModel


class FundCompany(BaseModel):
    """基金公司模型"""

    __tablename__ = "fund_company"
    __table_args__ = (
        Index("idx_company_code", "company_code"),
        {"comment": "基金公司表"},
    )

    company_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="公司代码"
    )
    company_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="公司名称"
    )
    management_scale: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="管理规模(亿)"
    )
    fund_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="基金数量"
    )
    establish_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="成立日期"
    )
    company_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="公司类型"
    )


class FundInfo(BaseModel):
    """基金信息模型"""

    __tablename__ = "fund_info"
    __table_args__ = (
        Index("idx_fund_code", "fund_code"),
        Index("idx_fund_company", "company_code"),
        {"comment": "基金信息表"},
    )

    fund_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="基金代码"
    )
    fund_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="基金名称"
    )
    fund_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="基金类型"
    )
    company_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="基金公司代码"
    )
    company_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="基金公司名称"
    )
    establish_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="成立日期"
    )
    fund_scale: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="基金规模(亿)"
    )
    fund_manager: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="基金经理"
    )


class FundHolding(BaseModel):
    """基金持仓明细模型"""

    __tablename__ = "fund_holding"
    __table_args__ = (
        Index("idx_fh_fund_code", "fund_code"),
        Index("idx_fh_stock_code", "stock_code"),
        Index("idx_fh_report_date", "report_date"),
        Index("idx_fh_fund_stock", "fund_code", "stock_code", "report_date"),
        {"comment": "基金持仓明细表"},
    )

    fund_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="基金代码"
    )
    fund_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="基金名称"
    )
    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="股票名称"
    )
    report_date: Mapped[date] = mapped_column(Date, nullable=False, comment="报告日期")

    holding_shares: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="持仓股数(万股)"
    )
    holding_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="持仓市值(万)"
    )
    holding_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="占净值比(%)"
    )

    change_type: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="变动类型: new/increase/decrease/exit"
    )
    change_shares: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="变动股数(万股)"
    )
    change_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="变动市值(万)"
    )


class StockMainForceOverview(BaseModel):
    """个股主力概览模型"""

    __tablename__ = "stock_mainforce_overview"
    __table_args__ = (
        Index("idx_smf_stock_code", "stock_code"),
        Index("idx_smf_report_date", "report_date"),
        {"comment": "个股主力概览表"},
    )

    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="股票名称"
    )
    report_date: Mapped[date] = mapped_column(Date, nullable=False, comment="报告日期")

    # 持仓概况
    fund_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="持仓基金数"
    )
    holding_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="持仓市值(万)"
    )
    holding_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="占流通股比(%)"
    )
    change_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="较上期变动(万)"
    )

    # 集中度
    concentration: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="筹码集中度(%)"
    )
    top10_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="TOP10基金占比(%)"
    )
    top20_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="TOP20基金占比(%)"
    )

    # 资金流向
    net_inflow: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="净流入(万)"
    )
    increase_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="增持基金数"
    )
    decrease_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="减持基金数"
    )
    new_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="新进基金数"
    )
    exit_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="退出基金数"
    )


class MainForceAlert(BaseModel):
    """主力预警模型"""

    __tablename__ = "mainforce_alert"
    __table_args__ = (
        Index("idx_mfa_stock_code", "stock_code"),
        Index("idx_mfa_user_id", "user_id"),
        {"comment": "主力预警表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="股票名称"
    )

    alert_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="预警类型"
    )
    alert_level: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="预警级别: high/medium/low"
    )
    alert_content: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="预警内容"
    )

    fund_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="相关基金代码"
    )
    fund_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="相关基金名称"
    )

    is_read: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否已读")
    read_time: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="阅读时间"
    )
