# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : macro_service.py
# @IDE            : PyCharm
# @desc           : 宏观经济服务 - GDP、CPI、利率等宏观数据

import akshare as ak
import pandas as pd
import math
from datetime import datetime
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


@dataclass
class MacroIndicator:
    """宏观经济指标"""

    indicator_name: str
    value: Optional[float]
    unit: Optional[str]
    period: Optional[str]
    update_time: datetime = field(default_factory=datetime.now)


class MacroService:
    """宏观经济数据服务"""

    # ========== GDP数据 ==========

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_gdp(self) -> List[Dict[str, Any]]:
        """获取GDP数据"""
        logger.info("获取GDP数据")

        try:
            df = ak.macro_china_gdp()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "quarter": str(row.get("季度", "")),
                        "gdp": safe_float(row.get("国内生产总值-绝对值")),
                        "gdp_yoy": safe_float(row.get("国内生产总值-同比增长")),
                        "primary_industry": safe_float(row.get("第一产业-绝对值")),
                        "secondary_industry": safe_float(row.get("第二产业-绝对值")),
                        "tertiary_industry": safe_float(row.get("第三产业-绝对值")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取GDP数据失败: {e}")
            return []

    # ========== CPI数据 ==========

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_cpi(self) -> List[Dict[str, Any]]:
        """获取CPI数据"""
        logger.info("获取CPI数据")

        try:
            df = ak.macro_china_cpi_yearly()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "month": str(row.get("月份", "")),
                        "cpi_yoy": safe_float(row.get("全国当月同比")),
                        "cpi_mom": safe_float(row.get("全国环比")),
                        "cpi_accumulated": safe_float(row.get("全国累计同比")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取CPI数据失败: {e}")
            return []

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_cpi_monthly(self) -> List[Dict[str, Any]]:
        """获取月度CPI数据"""
        logger.info("获取月度CPI数据")

        try:
            df = ak.macro_china_cpi_monthly()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "month": str(row.get("月份", "")),
                        "cpi_yoy": safe_float(row.get("全国同比")),
                        "cpi_mom": safe_float(row.get("全国环比")),
                        "urban_yoy": safe_float(row.get("城市同比")),
                        "rural_yoy": safe_float(row.get("农村同比")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取月度CPI数据失败: {e}")
            return []

    # ========== PPI数据 ==========

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_ppi(self) -> List[Dict[str, Any]]:
        """获取PPI数据"""
        logger.info("获取PPI数据")

        try:
            df = ak.macro_china_ppi_yearly()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "month": str(row.get("月份", "")),
                        "ppi_yoy": safe_float(row.get("当月同比")),
                        "ppi_accumulated": safe_float(row.get("累计同比")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取PPI数据失败: {e}")
            return []

    # ========== 货币供应量 ==========

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_money_supply(self) -> List[Dict[str, Any]]:
        """获取货币供应量数据"""
        logger.info("获取货币供应量数据")

        try:
            df = ak.macro_china_m2_yearly()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "month": str(row.get("月份", "")),
                        "m2": safe_float(row.get("货币和准货币(M2)")),
                        "m2_yoy": safe_float(row.get("货币和准货币(M2)同比增长")),
                        "m1": safe_float(row.get("货币(M1)")),
                        "m1_yoy": safe_float(row.get("货币(M1)同比增长")),
                        "m0": safe_float(row.get("流通中现金(M0)")),
                        "m0_yoy": safe_float(row.get("流通中现金(M0)同比增长")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取货币供应量失败: {e}")
            return []

    # ========== 社会融资规模 ==========

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_social_financing(self) -> List[Dict[str, Any]]:
        """获取社会融资规模数据"""
        logger.info("获取社会融资规模数据")

        try:
            df = ak.macro_china_shrzgm()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "month": str(row.get("月份", "")),
                        "total": safe_float(row.get("社会融资规模增量")),
                        "rmb_loans": safe_float(row.get("其中:人民币贷款")),
                        "entrust_loans": safe_float(row.get("其中:委托贷款")),
                        "trust_loans": safe_float(row.get("其中:信托贷款")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取社会融资规模失败: {e}")
            return []

    # ========== PMI数据 ==========

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_pmi(self) -> List[Dict[str, Any]]:
        """获取PMI数据"""
        logger.info("获取PMI数据")

        try:
            df = ak.macro_china_pmi_yearly()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "month": str(row.get("月份", "")),
                        "manufacturing_pmi": safe_float(row.get("制造业-指数")),
                        "manufacturing_new_order": safe_float(row.get("制造业-新订单")),
                        "non_manufacturing_pmi": safe_float(row.get("非制造业-指数")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取PMI数据失败: {e}")
            return []

    # ========== 利率数据 ==========

    @cache_result(expire=3600)
    @handle_akshare_exception
    async def get_interest_rate(self) -> Dict[str, Any]:
        """获取利率数据"""
        logger.info("获取利率数据")

        try:
            df = ak.rate_interbank(
                market="上海银行间同业拆放利率", symbol="Shibor人民币", indicator="隔夜"
            )

            result = {
                "shibor_overnight": None,
                "shibor_1week": None,
                "shibor_1month": None,
                "lpr_1year": None,
                "lpr_5year": None,
            }

            if not df.empty:
                row = df.iloc[-1]
                result["shibor_overnight"] = safe_float(row.get("利率"))

            try:
                df_1w = ak.rate_interbank(
                    market="上海银行间同业拆放利率",
                    symbol="Shibor人民币",
                    indicator="1周",
                )
                if not df_1w.empty:
                    result["shibor_1week"] = safe_float(df_1w.iloc[-1].get("利率"))
            except:
                pass

            try:
                df_lpr = ak.macro_china_lpr()
                if not df_lpr.empty:
                    row = df_lpr.iloc[-1]
                    result["lpr_1year"] = safe_float(row.get("LPR1Y"))
                    result["lpr_5year"] = safe_float(row.get("LPR5Y"))
            except:
                pass

            return result

        except Exception as e:
            logger.warning(f"获取利率数据失败: {e}")
            return {}

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_lpr_history(self) -> List[Dict[str, Any]]:
        """获取LPR历史数据"""
        logger.info("获取LPR历史数据")

        try:
            df = ak.macro_china_lpr()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "date": str(row.get("日期", "")),
                        "lpr_1year": safe_float(row.get("LPR1Y")),
                        "lpr_5year": safe_float(row.get("LPR5Y")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取LPR历史数据失败: {e}")
            return []

    # ========== 汇率数据 ==========

    @cache_result(expire=3600)
    @handle_akshare_exception
    async def get_exchange_rate(self) -> Dict[str, Any]:
        """获取汇率数据"""
        logger.info("获取汇率数据")

        try:
            df = ak.currency_boc_safe()

            if df.empty:
                return {}

            result = {}
            for _, row in df.iterrows():
                currency = str(row.get("货币名称", ""))
                if "美元" in currency:
                    result["usd_cny"] = safe_float(row.get("中行折算价"))
                elif "欧元" in currency:
                    result["eur_cny"] = safe_float(row.get("中行折算价"))
                elif "日元" in currency:
                    result["jpy_cny"] = safe_float(row.get("中行折算价"))
                elif "英镑" in currency:
                    result["gbp_cny"] = safe_float(row.get("中行折算价"))

            return result

        except Exception as e:
            logger.warning(f"获取汇率数据失败: {e}")
            return {}

    # ========== 外汇储备 ==========

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_fx_reserves(self) -> List[Dict[str, Any]]:
        """获取外汇储备数据"""
        logger.info("获取外汇储备数据")

        try:
            df = ak.macro_china_fx_reserves()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "month": str(row.get("月份", "")),
                        "fx_reserves": safe_float(row.get("外汇储备(亿美元)")),
                        "gold_reserves": safe_float(row.get("黄金储备(盎司)")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取外汇储备失败: {e}")
            return []

    # ========== 贸易数据 ==========

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_trade_data(self) -> List[Dict[str, Any]]:
        """获取进出口贸易数据"""
        logger.info("获取进出口贸易数据")

        try:
            df = ak.macro_china_trade_data()

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "month": str(row.get("月份", "")),
                        "export": safe_float(row.get("出口金额-美元")),
                        "import": safe_float(row.get("进口金额-美元")),
                        "trade_balance": safe_float(row.get("贸易顺差")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取贸易数据失败: {e}")
            return []

    # ========== 综合指标 ==========

    async def get_macro_overview(self) -> Dict[str, Any]:
        """获取宏观经济概览"""
        logger.info("获取宏观经济概览")

        gdp = await self.get_gdp()
        cpi = await self.get_cpi()
        ppi = await self.get_ppi()
        pmi = await self.get_pmi()
        interest_rate = await self.get_interest_rate()
        exchange_rate = await self.get_exchange_rate()

        return {
            "gdp": gdp[:4] if gdp else [],
            "cpi": cpi[:12] if cpi else [],
            "ppi": ppi[:12] if ppi else [],
            "pmi": pmi[:12] if pmi else [],
            "interest_rate": interest_rate,
            "exchange_rate": exchange_rate,
            "update_time": datetime.now().isoformat(),
        }


macro_service = MacroService()
