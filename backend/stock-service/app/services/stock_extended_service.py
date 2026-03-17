# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : stock_extended_service.py
# @IDE            : PyCharm
# @desc           : 股票扩展服务 - 龙虎榜、资金流、财务数据等

import akshare as ak
import pandas as pd
import math
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict, field

from app.core.logging import get_logger
from app.utils.cache import cache_result
from app.utils.akshare_wrapper import handle_akshare_exception, with_retry
from app.core.data_source_manager import DataSource, data_source_manager

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
class LongHuBangItem:
    """龙虎榜数据项"""

    trade_date: str
    stock_code: str
    stock_name: str
    close_price: Optional[float]
    change_percent: Optional[float]
    turnover_rate: Optional[float]
    total_amount: Optional[float]
    net_buy_amount: Optional[float]
    net_buy_ratio: Optional[float]
    reason: str
    buy_details: List[Dict] = field(default_factory=list)
    sell_details: List[Dict] = field(default_factory=list)
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class FundFlowItem:
    """个股资金流向"""

    stock_code: str
    stock_name: str
    close_price: Optional[float]
    change_percent: Optional[float]
    main_net_inflow: Optional[float]
    main_net_inflow_ratio: Optional[float]
    retail_net_inflow: Optional[float]
    retail_net_inflow_ratio: Optional[float]
    super_net_inflow: Optional[float]
    big_net_inflow: Optional[float]
    medium_net_inflow: Optional[float]
    small_net_inflow: Optional[float]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class FinancialIndicator:
    """财务指标"""

    stock_code: str
    stock_name: str
    report_date: str
    roe: Optional[float]
    roa: Optional[float]
    gross_margin: Optional[float]
    net_margin: Optional[float]
    debt_ratio: Optional[float]
    current_ratio: Optional[float]
    quick_ratio: Optional[float]
    eps: Optional[float]
    bvps: Optional[float]
    pe: Optional[float]
    pb: Optional[float]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class DividendItem:
    """分红数据"""

    stock_code: str
    stock_name: str
    report_year: str
    dividend_date: Optional[str]
    ex_dividend_date: Optional[str]
    dividend_amount: Optional[float]
    dividend_ratio: Optional[float]
    dividend_type: Optional[str]
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class BlockTradeItem:
    """大宗交易"""

    trade_date: str
    stock_code: str
    stock_name: str
    trade_price: Optional[float]
    trade_amount: Optional[float]
    trade_volume: Optional[float]
    buyer_name: Optional[str]
    seller_name: Optional[str]
    premium_rate: Optional[float]
    update_time: datetime = field(default_factory=datetime.now)


# ========== 服务类 ==========


class StockExtendedService:
    """股票扩展数据服务"""

    # ========== 龙虎榜数据 ==========

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_lhb_list(
        self,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[LongHuBangItem]:
        """
        获取龙虎榜数据

        Args:
            trade_date: 交易日期 YYYYMMDD
            start_date: 开始日期
            end_date: 结束日期
        """
        logger.info(f"获取龙虎榜数据: {trade_date or start_date} - {end_date}")

        if not trade_date:
            trade_date = datetime.now().strftime("%Y%m%d")

        try:
            df = ak.stock_lhb_detail_em(start_date=trade_date, end_date=trade_date)

            if df.empty:
                logger.warning(f"未获取到龙虎榜数据: {trade_date}")
                return []

            result = []
            for _, row in df.iterrows():
                item = LongHuBangItem(
                    trade_date=str(row.get("交易日", "")),
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    close_price=safe_float(row.get("收盘价")),
                    change_percent=safe_float(row.get("涨跌幅")),
                    turnover_rate=safe_float(row.get("换手率")),
                    total_amount=safe_float(row.get("总成交额")),
                    net_buy_amount=safe_float(row.get("龙虎榜净买额")),
                    net_buy_ratio=safe_float(row.get("龙虎榜净买额占比")),
                    reason=str(row.get("上榜原因", "")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.error(f"获取龙虎榜数据失败: {e}")
            raise

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_lhb_by_stock(
        self, stock_code: str, days: int = 30
    ) -> List[LongHuBangItem]:
        """获取个股龙虎榜历史"""
        logger.info(f"获取个股龙虎榜: {stock_code}, 近{days}天")

        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")

        try:
            df = ak.stock_lhb_detail_em(start_date=start_date, end_date=end_date)

            if df.empty:
                return []

            df = df[df["代码"] == stock_code]

            result = []
            for _, row in df.iterrows():
                item = LongHuBangItem(
                    trade_date=str(row.get("交易日", "")),
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    close_price=safe_float(row.get("收盘价")),
                    change_percent=safe_float(row.get("涨跌幅")),
                    turnover_rate=safe_float(row.get("换手率")),
                    total_amount=safe_float(row.get("总成交额")),
                    net_buy_amount=safe_float(row.get("龙虎榜净买额")),
                    net_buy_ratio=safe_float(row.get("龙虎榜净买额占比")),
                    reason=str(row.get("上榜原因", "")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.error(f"获取个股龙虎榜失败: {e}")
            raise

    # ========== 资金流向 ==========

    @cache_result(expire=60)
    @handle_akshare_exception
    async def get_individual_fund_flow(self, stock_code: str) -> Optional[FundFlowItem]:
        """获取个股资金流向"""
        logger.info(f"获取个股资金流向: {stock_code}")

        try:
            df = ak.stock_individual_fund_flow(
                stock=stock_code, market="sh" if stock_code.startswith("6") else "sz"
            )

            if df.empty:
                return None

            row = df.iloc[0]

            return FundFlowItem(
                stock_code=stock_code,
                stock_name=str(row.get("名称", "")),
                close_price=safe_float(row.get("收盘价")),
                change_percent=safe_float(row.get("涨跌幅")),
                main_net_inflow=safe_float(row.get("主力净流入")),
                main_net_inflow_ratio=safe_float(row.get("主力净占比")),
                retail_net_inflow=safe_float(row.get("散户净流入")),
                retail_net_inflow_ratio=safe_float(row.get("散户净占比")),
                super_net_inflow=safe_float(row.get("超大单净流入")),
                big_net_inflow=safe_float(row.get("大单净流入")),
                medium_net_inflow=safe_float(row.get("中单净流入")),
                small_net_inflow=safe_float(row.get("小单净流入")),
            )

        except Exception as e:
            logger.warning(f"AKShare获取资金流向失败: {e}")
            return None

    @cache_result(expire=60)
    @handle_akshare_exception
    async def get_fund_flow_rank(self, indicator: str = "今日") -> List[FundFlowItem]:
        """
        获取资金流向排名

        Args:
            indicator: 今日/3日/5日/10日
        """
        logger.info(f"获取资金流向排名: {indicator}")

        try:
            df = ak.stock_sector_fund_flow_rank(
                indicator=indicator, sector_type="行业资金流"
            )

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = FundFlowItem(
                    stock_code=str(row.get("代码", "")),
                    stock_name=str(row.get("名称", "")),
                    close_price=safe_float(row.get("最新价")),
                    change_percent=safe_float(row.get("涨跌幅")),
                    main_net_inflow=safe_float(row.get("主力净流入")),
                    main_net_inflow_ratio=safe_float(row.get("主力净占比")),
                    retail_net_inflow=None,
                    retail_net_inflow_ratio=None,
                    super_net_inflow=safe_float(row.get("超大单净流入")),
                    big_net_inflow=safe_float(row.get("大单净流入")),
                    medium_net_inflow=safe_float(row.get("中单净流入")),
                    small_net_inflow=safe_float(row.get("小单净流入")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.error(f"获取资金流向排名失败: {e}")
            raise

    # ========== 财务数据 ==========

    @cache_result(expire=3600)
    @handle_akshare_exception
    async def get_financial_indicators(
        self, stock_code: str
    ) -> List[FinancialIndicator]:
        """获取个股财务指标"""
        logger.info(f"获取财务指标: {stock_code}")

        try:
            df = ak.stock_financial_analysis_indicator(symbol=stock_code)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = FinancialIndicator(
                    stock_code=stock_code,
                    stock_name=str(row.get("简称", "")),
                    report_date=str(row.get("日期", "")),
                    roe=safe_float(row.get("净资产收益率")),
                    roa=safe_float(row.get("总资产净利率")),
                    gross_margin=safe_float(row.get("销售毛利率")),
                    net_margin=safe_float(row.get("销售净利率")),
                    debt_ratio=safe_float(row.get("资产负债率")),
                    current_ratio=safe_float(row.get("流动比率")),
                    quick_ratio=safe_float(row.get("速动比率")),
                    eps=safe_float(row.get("每股收益")),
                    bvps=safe_float(row.get("每股净资产")),
                    pe=safe_float(row.get("市盈率")),
                    pb=safe_float(row.get("市净率")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.error(f"获取财务指标失败: {e}")
            raise

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_dividend_history(self, stock_code: str) -> List[DividendItem]:
        """获取分红历史"""
        logger.info(f"获取分红历史: {stock_code}")

        try:
            df = ak.stock_dividend_cninfo(symbol=stock_code)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = DividendItem(
                    stock_code=stock_code,
                    stock_name=str(row.get("证券简称", "")),
                    report_year=str(row.get("分红年度", "")),
                    dividend_date=str(row.get("分红实施公告日", ""))
                    if pd.notna(row.get("分红实施公告日"))
                    else None,
                    ex_dividend_date=str(row.get("A股股权登记日", ""))
                    if pd.notna(row.get("A股股权登记日"))
                    else None,
                    dividend_amount=safe_float(row.get("每股股利(税前)")),
                    dividend_ratio=safe_float(row.get("股利支付率")),
                    dividend_type=str(row.get("股利类型", ""))
                    if pd.notna(row.get("股利类型"))
                    else None,
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取分红历史失败: {e}")
            return []

    # ========== 大宗交易 ==========

    @cache_result(expire=300)
    @handle_akshare_exception
    async def get_block_trade(
        self, trade_date: Optional[str] = None
    ) -> List[BlockTradeItem]:
        """获取大宗交易数据"""
        if not trade_date:
            trade_date = datetime.now().strftime("%Y%m%d")

        logger.info(f"获取大宗交易: {trade_date}")

        try:
            df = ak.stock_dzjy_mrmx(
                symbol="A股", start_date=trade_date, end_date=trade_date
            )

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                item = BlockTradeItem(
                    trade_date=str(row.get("交易日期", "")),
                    stock_code=str(row.get("证券代码", "")),
                    stock_name=str(row.get("证券简称", "")),
                    trade_price=safe_float(row.get("成交价")),
                    trade_amount=safe_float(row.get("成交金额")),
                    trade_volume=safe_float(row.get("成交量")),
                    buyer_name=str(row.get("买方营业部", ""))
                    if pd.notna(row.get("买方营业部"))
                    else None,
                    seller_name=str(row.get("卖方营业部", ""))
                    if pd.notna(row.get("卖方营业部"))
                    else None,
                    premium_rate=safe_float(row.get("溢价率")),
                )
                result.append(item)

            return result

        except Exception as e:
            logger.warning(f"获取大宗交易失败: {e}")
            return []

    # ========== 股东数据 ==========

    @cache_result(expire=86400)
    @handle_akshare_exception
    async def get_shareholder_number(self, stock_code: str) -> List[Dict[str, Any]]:
        """获取股东人数变化"""
        logger.info(f"获取股东人数: {stock_code}")

        try:
            df = ak.stock_zh_a_gdhs(symbol=stock_code)

            if df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "stock_code": stock_code,
                        "report_date": str(row.get("股东户数统计截止日", "")),
                        "shareholder_num": safe_float(row.get("股东户数")),
                        "change_percent": safe_float(row.get("股东户数较上期变化")),
                        "avg_shareholder_holding": safe_float(row.get("户均持股数量")),
                        "avg_shareholder_amount": safe_float(row.get("户均持股金额")),
                    }
                )

            return result

        except Exception as e:
            logger.warning(f"获取股东人数失败: {e}")
            return []


stock_extended_service = StockExtendedService()
