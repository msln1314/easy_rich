from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class FundCompanyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_code: str
    company_name: str
    management_scale: Optional[float] = None
    fund_count: Optional[int] = None
    establish_date: Optional[date] = None
    company_type: Optional[str] = None
    created_at: DatetimeStr


class FundInfoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fund_code: str
    fund_name: str
    fund_type: Optional[str] = None
    company_code: Optional[str] = None
    company_name: Optional[str] = None
    establish_date: Optional[date] = None
    fund_scale: Optional[float] = None
    fund_manager: Optional[str] = None
    created_at: DatetimeStr


class FundHoldingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fund_code: str
    fund_name: Optional[str] = None
    stock_code: str
    stock_name: Optional[str] = None
    report_date: date
    holding_shares: Optional[float] = None
    holding_value: Optional[float] = None
    holding_ratio: Optional[float] = None
    change_type: Optional[str] = None
    change_shares: Optional[float] = None
    change_value: Optional[float] = None
    created_at: DatetimeStr


class MainForceOverviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    stock_code: str
    stock_name: Optional[str] = None
    report_date: date
    fund_count: Optional[int] = None
    holding_value: Optional[float] = None
    holding_ratio: Optional[float] = None
    change_value: Optional[float] = None
    concentration: Optional[float] = None
    top10_ratio: Optional[float] = None
    top20_ratio: Optional[float] = None
    net_inflow: Optional[float] = None
    increase_count: Optional[int] = None
    decrease_count: Optional[int] = None
    new_count: Optional[int] = None
    exit_count: Optional[int] = None
    created_at: DatetimeStr


class MainForceFundItem(BaseModel):
    fund_code: str
    fund_name: Optional[str] = None
    fund_company: Optional[str] = None
    holding_value: Optional[float] = None
    holding_ratio: Optional[float] = None
    holding_shares: Optional[float] = None
    change_type: Optional[str] = None
    change_value: Optional[float] = None
    change_ratio: Optional[float] = None
    report_date: Optional[date] = None


class MainForceTrendItem(BaseModel):
    report_date: date
    fund_count: Optional[int] = None
    holding_value: Optional[float] = None
    net_inflow: Optional[float] = None
    concentration: Optional[float] = None


class MainForceAlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    stock_code: str
    stock_name: Optional[str] = None
    alert_type: str
    alert_level: Optional[str] = None
    alert_content: Optional[str] = None
    fund_code: Optional[str] = None
    fund_name: Optional[str] = None
    is_read: int
    read_time: Optional[date] = None
    created_at: DatetimeStr


class MainForceAlertCreate(BaseModel):
    stock_code: str
    stock_name: Optional[str] = None
    alert_type: str
    alert_level: Optional[str] = None
    alert_content: Optional[str] = None
    fund_code: Optional[str] = None
    fund_name: Optional[str] = None


class CompanyHoldingItem(BaseModel):
    stock_code: str
    stock_name: Optional[str] = None
    holding_value: Optional[float] = None
    holding_ratio: Optional[float] = None
    fund_count: Optional[int] = None
    change_value: Optional[float] = None
    report_date: Optional[date] = None
