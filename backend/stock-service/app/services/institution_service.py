# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : institution_service.py
# @IDE            : PyCharm
# @desc           : 机构数据服务 - 机构调研、基金持仓等

import akshare as ak
import pandas as pd
import math
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from app.core.logging import get_logger
from app.utils.cache import cache_result
from app.utils.akshare_wrapper import handle_akshare_exception

logger = get_logger(__name__)


def safe_float(value, default=None):
    if value is None or pd.isna(value):
        return default
    try:
        float_value = float(value)
        if math.isnan(float_value) or math.isinf(float_value):
            return default
        return float_value
    except (ValueError, TypeError):
        return default


# ========== 数据模型 ==========


@dataclass
class InstitutionResearch:
    """机构调研"""

    stock_code: str
    stock_name: str
    research_date: str
    institution_type: Optional[str]
    institution_name: Optional[str]
    researcher_num: Optional[int]
    reception_place: Optional[str]
    reception_person: Optional[str]
    activity_type: Optional[str]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class FundHolding:
    """基金持股"""

    stock_code: str
    stock_name: str
    fund_code: Optional[str]
    fund_name: Optional[str]
    holding_share: Optional[float]
    holding_amount: Optional[float]
    holding_ratio: Optional[float]
    report_date: Optional[str]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class NorthHolding:
    """北向资金持股"""

    stock_code: str
    stock_name: str
    holding_share: Optional[float]
    holding_ratio: Optional[float]
    change_share: Optional[float]
    change_ratio: Optional[float]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class MainForceHolding:
    """主力持仓"""

    stock_code: str
    stock_name: str
    holder_type: Optional[str]
    holder_name: Optional[str]
    holding_share: Optional[float]
    holding_ratio: Optional[float]
    change_share: Optional[float]
    report_date: Optional[str]
    update_time: datetime = field(default_factory=datetime.now)


# ========== 服务类 ==========


class InstitutionService:
    """机构数据服务"""

    # ========== 机构调研 ==========

    @cache_result(expire=3600)
    @handle_akshare_exception
    async def get_research_list(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> List[InstitutionResearch]:
        """获取机构调研列表"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y%m%d")

        logger.info(f"获取机构调研列表: {start_date} - {end_date}")

        try:
            df = ak.stock_jgdy_tj_em(start_date=start_date, end_date=end_date)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = InstitutionResearch(
                    stock_code=str(row.get("股票代码", "")),
                    stock_name=str(row.get("股票简称", "")),
                    research_date=str(row.get("调研日期", "")),
                    institution_type=str(row.get("机构类型", ""))
                    if pd.notna(row.get("机构类型"))
                    else None,
                    institution_name=str(row.get("机构名称", ""))
                    if pd.notna(row.get("机构名称"))
                    else None,
                    researcher_num=safe_float(row.get("调研人数")),
                    reception_place=str(row.get("接待地点", ""))
                    if pd.notna(row.get("接待地点"))
                    else None,
                    reception_person=str(row.get("接待人员", ""))
                    if pd.notna(row.get("接待人员"))
                    else None,
                    activity_type=str(row.get("活动类型", ""))
                    if pd.notna(row.get("活动类型"))
                    else None,
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取机构调研列表失败: {e}")
            return []

    @cache_result(expire=3600)
    @handle_akshare_exception
    async def get_research_by_stock(self, stock_code: str) -> List[InstitutionResearch]:
        """获取个股机构调研历史"""
        logger.info(f"获取个股机构调研: {stock_code}")

        try:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            end_date = datetime.now().strftime("%Y%m%d")

            df = ak.stock_jgdy_tj_em(start_date=start_date, end_date=end_date)

            if df.empty:
                return []

            df = df[df["股票代码"] == stock_code]

            result = []
            for _, row in df.iterrows():
                item = InstitutionResearch(
                    stock_code=str(row.get("股票代码", "")),
                    stock_name=str(row.get("股票简称", "")),
                    research_date=str(row.get("调研日期", "")),
                    institution_type=str(row.get("机构类型", ""))
                    if pd.notna(row.get("机构类型"))
                    else None,
                    institution_name=str(row.get("机构名称", ""))
                    if pd.notna(row.get("机构名称"))
                    else None,
                    researcher_num=safe_float(row.get("调研人数")),
                    reception_place=str(row.get("接待地点", ""))
                    if pd.notna(row.get("接待地点"))
                    else None,
                    reception_person=str(row.get("接待人员", ""))
                    if pd.notna(row.get("接待人员"))
                    else None,
                    activity_type=str(row.get("活动类型", ""))
                    if pd.notna(row.get("活动类型"))
                    else None,
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取个股机构调研失败: {e}")
            return []

    # ========== 基金持股 ==========

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_fund_holding(self, stock_code: str) -> List[FundHolding]:
        """获取个股基金持股"""
        logger.info(f"获取基金持股: {stock_code}")

        try:
            df = ak.stock_fund_stock_em(symbol=stock_code)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = FundHolding(
                    stock_code=stock_code,
                    stock_name=str(row.get("股票名称", "")),
                    fund_code=str(row.get("基金代码", ""))
                    if pd.notna(row.get("基金代码"))
                    else None,
                    fund_name=str(row.get("基金简称", ""))
                    if pd.notna(row.get("基金简称"))
                    else None,
                    holding_share=safe_float(row.get("持股数")),
                    holding_amount=safe_float(row.get("持股市值")),
                    holding_ratio=safe_float(row.get("占流通股比例")),
                    report_date=str(row.get("报告期", ""))
                    if pd.notna(row.get("报告期"))
                    else None,
                )
                result.append(item)

            return result[:50]

        except Exception as e:
            logger.warning(f"获取基金持股失败: {e}")
            return []

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_fund_holding_rank(self, top: int = 50) -> List[FundHolding]:
        """获取基金持股排名"""
        logger.info(f"获取基金持股排名: top {top}")

        try:
            df = ak.stock_fund_flow_individual(symbol="即时")

            if df.empty:
                return []

            result = []
            for idx, row in df.head(top).iterrows():
                item = FundHolding(
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    fund_code=None,
                    fund_name=None,
                    holding_share=None,
                    holding_amount=None,
                    holding_ratio=None,
                    report_date=None,
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取基金持股排名失败: {e}")
            return []

    # ========== 北向资金持股 ==========

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_north_holding(self, top: int = 50) -> List[NorthHolding]:
        """获取北向资金持股"""
        logger.info(f"获取北向资金持股: top {top}")

        try:
            df = ak.stock_hsgt_hold_stock_em(market="北向", indicator="今日排名")

            if df.empty:
                return []

            result = []
            for _, row in df.head(top).iterrows():
                item = NorthHolding(
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    holding_share=safe_float(row.get("持股数量")),
                    holding_ratio=safe_float(row.get("持股占A股百分比")),
                    change_share=safe_float(row.get("持股市值变化")),
                    change_ratio=safe_float(row.get("持股数量变化")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取北向资金持股失败: {e}")
            return []

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_north_holding_by_stock(
        self, stock_code: str
    ) -> Optional[NorthHolding]:
        """获取个股北向资金持股"""
        logger.info(f"获取个股北向资金持股: {stock_code}")

        try:
            df = ak.stock_hsgt_hold_stock_em(market="北向", indicator="今日排名")

            if df.empty:
                return None

            df = df[df["代码"] == stock_code]

            if df.empty:
                return None

            row = df.iloc[0]

            return NorthHolding(
                stock_code=stock_code,
                stock_name=str(row.get("名称", "")),
                holding_share=safe_float(row.get("持股数量")),
                holding_ratio=safe_float(row.get("持股占A股百分比")),
                change_share=safe_float(row.get("持股市值变化")),
                change_ratio=safe_float(row.get("持股数量变化")),
            )

        except Exception as e:
            logger.warning(f"获取个股北向资金持股失败: {e}")
            return None

    # ========== 主力持仓 ==========

    @cache_result(expire=3600)
    @handle_akshare_exception
    async def get_main_force_holding(self, stock_code: str) -> List[MainForceHolding]:
        """获取个股主力持仓"""
        logger.info(f"获取主力持仓: {stock_code}")

        try:
            df = ak.stock_zh_a_gdhs(symbol=stock_code)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = MainForceHolding(
                    stock_code=stock_code,
                    stock_name=str(row.get("股东户数统计截止日", "")),
                    holder_type="股东",
                    holder_name=None,
                    holding_share=safe_float(row.get("户均持股数量")),
                    holding_ratio=None,
                    change_share=safe_float(row.get("股东户数较上期变化")),
                    report_date=str(row.get("股东户数统计截止日", "")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取主力持仓失败: {e}")
            return []


institution_service = InstitutionService()
