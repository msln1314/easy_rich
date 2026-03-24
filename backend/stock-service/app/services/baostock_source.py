# -*- coding: utf-8 -*-
# @version        : 2.0
# @Create Time    : 2026/3/24
# @File           : baostock_source.py
# @IDE            : PyCharm
# @desc           : 证券宝数据源 - 免费开源证券数据平台（完整版）

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import pandas as pd

from app.core.logging import get_logger

logger = get_logger(__name__)

try:
    import baostock as bs

    BAOSTOCK_AVAILABLE = True
except ImportError:
    BAOSTOCK_AVAILABLE = False
    logger.warning("baostock 未安装，证券宝数据源不可用")


@dataclass
class BaostockKline:
    stock_code: str
    trade_date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: float
    turnover: Optional[float]
    change_percent: Optional[float]
    change_amount: Optional[float]
    amplitude: Optional[float]
    source: str = "baostock"


@dataclass
class StockBasic:
    """股票基本信息"""
    code: str
    name: str
    industry: str
    list_date: str
    type: str  # 1-股票 2-指数 3-其他
    status: str  # 1-正常 2-暂停 3-退市


@dataclass
class StockIndustry:
    """股票行业分类"""
    code: str
    name: str
    industry: str
    industry_classification: str  # 证监会行业分类


@dataclass
class FinancialIndicator:
    """财务指标"""
    code: str
    pub_date: str
    stat_date: str
    roe: Optional[float]  # 净资产收益率
    roe_dt: Optional[float]  # 净资产收益率-扣非
    roa: Optional[float]  # 总资产净利率
    eps: Optional[float]  # 每股收益
    bvps: Optional[float]  # 每股净资产
    cfps: Optional[float]  # 每股现金流
    net_profit: Optional[float]  # 净利润
    net_profit_yoy: Optional[float]  # 净利润同比增长
    revenue: Optional[float]  # 营业收入
    revenue_yoy: Optional[float]  # 营收同比增长
    gross_margin: Optional[float]  # 毛利率
    net_margin: Optional[float]  # 净利率
    debt_ratio: Optional[float]  # 资产负债率
    current_ratio: Optional[float]  # 流动比率
    quick_ratio: Optional[float]  # 速动比率


@dataclass
class Dividend:
    """分红送股"""
    code: str
    pub_date: str
    div_year: str
    ann_date: str
    record_date: str
    ex_date: str
    pay_date: str
    dividend: Optional[float]  # 每股分红
    transfer: Optional[float]  # 每股转增
    bonus: Optional[float]  # 每股送股


@dataclass
class AdjustFactor:
    """复权因子"""
    code: str
    date: str
    fore_adjust: float  # 前复权因子
    back_adjust: float  # 后复权因子


class BaostockSource:
    """证券宝数据源 - 免费、稳定的历史K线数据"""

    _instance = None
    _logged_in = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def is_available(self) -> bool:
        """检查证券宝是否可用"""
        return BAOSTOCK_AVAILABLE

    def _login(self) -> bool:
        """登录证券宝"""
        if not BAOSTOCK_AVAILABLE:
            return False

        if self._logged_in:
            return True

        try:
            lg = bs.login()
            if lg.error_code == "0":
                self._logged_in = True
                logger.info("证券宝登录成功")
                return True
            else:
                logger.warning(f"证券宝登录失败: {lg.error_msg}")
                return False
        except Exception as e:
            logger.error(f"证券宝登录异常: {e}")
            return False

    def _logout(self):
        """登出证券宝"""
        if self._logged_in:
            try:
                bs.logout()
                self._logged_in = False
            except:
                pass

    def _get_baostock_code(self, stock_code: str) -> str:
        """转换为证券宝代码格式 (如: sh.600000, sz.000001)"""
        code = stock_code.lower()

        if code.startswith(("sh", "sz", "bj")):
            return code

        if code.startswith("6"):
            return f"sh.{code}"
        elif code.startswith(("0", "3")):
            return f"sz.{code}"
        elif code.startswith("8"):
            return f"bj.{code}"
        else:
            return f"sz.{code}"

    def _calc_amplitude(self, high: float, low: float, pre_close: float) -> Optional[float]:
        """计算振幅"""
        if pre_close and pre_close != 0:
            return round((high - low) / pre_close * 100, 2)
        return None

    # ==================== K线数据 ====================

    def get_history_kline(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        period: str = "d",
        adjust: str = "2",
    ) -> List[BaostockKline]:
        """
        获取历史K线数据

        Args:
            stock_code: 股票代码，如 "000001"
            start_date: 开始日期，格式 YYYY-MM-DD 或 YYYYMMDD
            end_date: 结束日期，格式 YYYY-MM-DD 或 YYYYMMDD
            period: 周期，d=日k线, w=周, m=月, 5/15/30/60=分钟
            adjust: 复权类型，1-后复权, 2-前复权, 3-不复权

        Returns:
            List[BaostockKline]: K线数据列表
        """
        if not self._login():
            return []

        try:
            bs_code = self._get_baostock_code(stock_code)

            if len(start_date) == 8:
                start_date = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}"
            if len(end_date) == 8:
                end_date = f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:8]}"

            fields = "date,code,open,high,low,close,volume,amount,turn,pctChg"

            rs = bs.query_history_k_data_plus(
                bs_code,
                fields,
                start_date=start_date,
                end_date=end_date,
                frequency=period,
                adjustflag=adjust,
            )

            if rs.error_code != "0":
                logger.warning(f"证券宝查询失败: {rs.error_msg}")
                return []

            data_list = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if not row or len(row) < 10:
                    continue

                try:
                    trade_date = row[0]
                    open_price = float(row[2]) if row[2] else None
                    high_price = float(row[3]) if row[3] else None
                    low_price = float(row[4]) if row[4] else None
                    close_price = float(row[5]) if row[5] else None
                    volume = float(row[6]) if row[6] else None
                    amount = float(row[7]) if row[7] else None
                    turnover = float(row[8]) if row[8] else None
                    change_percent = float(row[9]) if row[9] else None

                    if open_price and close_price:
                        change_amount = round(close_price - open_price, 2) if change_percent else None
                        amplitude = self._calc_amplitude(high_price, low_price, open_price)

                        kline = BaostockKline(
                            stock_code=stock_code,
                            trade_date=trade_date,
                            open=open_price,
                            high=high_price,
                            low=low_price,
                            close=close_price,
                            volume=volume,
                            amount=amount,
                            turnover=turnover,
                            change_percent=change_percent,
                            change_amount=change_amount,
                            amplitude=amplitude,
                        )
                        data_list.append(kline)

                except (ValueError, TypeError) as e:
                    logger.warning(f"解析K线数据失败: {e}")
                    continue

            logger.info(f"证券宝获取 {stock_code} K线数据 {len(data_list)} 条")
            return data_list

        except Exception as e:
            logger.error(f"证券宝获取K线数据异常: {e}")
            return []

    async def get_history_kline_async(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        period: str = "d",
        adjust: str = "2",
    ) -> List[BaostockKline]:
        """异步获取历史K线数据"""
        return await asyncio.to_thread(
            self.get_history_kline,
            stock_code,
            start_date,
            end_date,
            period,
            adjust,
        )

    # ==================== 股票列表 ====================

    def get_all_stocks(self, date: str = None) -> List[StockBasic]:
        """
        获取全部股票列表

        Args:
            date: 查询日期，格式 YYYY-MM-DD，默认当前日期

        Returns:
            List[StockBasic]: 股票列表
        """
        if not self._login():
            return []

        try:
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")

            rs = bs.query_all_stock(day=date)

            if rs.error_code != "0":
                logger.warning(f"获取股票列表失败: {rs.error_msg}")
                return []

            stocks = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if not row or len(row) < 5:
                    continue

                try:
                    stock = StockBasic(
                        code=row[0],
                        name=row[1] or "",
                        industry=row[2] or "",
                        list_date=row[3] or "",
                        type=row[4] or "1",
                        status=row[5] if len(row) > 5 else "1",
                    )
                    stocks.append(stock)
                except Exception:
                    continue

            logger.info(f"获取股票列表 {len(stocks)} 只")
            return stocks

        except Exception as e:
            logger.error(f"获取股票列表异常: {e}")
            return []

    def get_stock_list_by_industry(self, industry: str) -> List[str]:
        """
        根据行业获取股票列表

        Args:
            industry: 行业名称

        Returns:
            List[str]: 股票代码列表
        """
        if not self._login():
            return []

        try:
            rs = bs.query_stock_by_industry(industry)

            if rs.error_code != "0":
                return []

            codes = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row:
                    codes.append(row[0])

            return codes

        except Exception as e:
            logger.error(f"根据行业获取股票列表异常: {e}")
            return []

    # ==================== 行业分类 ====================

    def get_industry_classification(self, code: str = None) -> List[StockIndustry]:
        """
        获取行业分类数据

        Args:
            code: 股票代码，为空则获取所有

        Returns:
            List[StockIndustry]: 行业分类列表
        """
        if not self._login():
            return []

        try:
            rs = bs.query_stock_industry(code=code)

            if rs.error_code != "0":
                return []

            industries = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if not row:
                    continue

                industry = StockIndustry(
                    code=row[0] if len(row) > 0 else "",
                    name=row[1] if len(row) > 1 else "",
                    industry=row[2] if len(row) > 2 else "",
                    industry_classification=row[3] if len(row) > 3 else "",
                )
                industries.append(industry)

            return industries

        except Exception as e:
            logger.error(f"获取行业分类异常: {e}")
            return []

    def get_all_industries(self) -> List[Dict[str, str]]:
        """获取所有行业列表"""
        if not self._login():
            return []

        try:
            rs = bs.query_stock_industry()

            if rs.error_code != "0":
                return []

            industries = {}
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row and len(row) > 2:
                    industry_name = row[2]
                    if industry_name not in industries:
                        industries[industry_name] = {
                            "name": industry_name,
                            "classification": row[3] if len(row) > 3 else "",
                        }

            return list(industries.values())

        except Exception as e:
            logger.error(f"获取行业列表异常: {e}")
            return []

    # ==================== 财务数据 ====================

    def get_financial_indicator(
        self,
        stock_code: str,
        start_date: str = None,
        end_date: str = None,
        year: str = None,
        quarter: int = None,
    ) -> List[FinancialIndicator]:
        """
        获取财务指标数据

        Args:
            stock_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            year: 年份 (与quarter配合使用)
            quarter: 季度 1-4

        Returns:
            List[FinancialIndicator]: 财务指标列表
        """
        if not self._login():
            return []

        try:
            bs_code = self._get_baostock_code(stock_code)

            if year and quarter:
                rs = bs.query_financial_indicator(
                    code=bs_code, year=year, quarter=quarter
                )
            else:
                rs = bs.query_financial_indicator(
                    code=bs_code,
                    start_date=start_date or "",
                    end_date=end_date or "",
                )

            if rs.error_code != "0":
                logger.warning(f"获取财务指标失败: {rs.error_msg}")
                return []

            indicators = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if not row:
                    continue

                try:
                    indicator = FinancialIndicator(
                        code=row[0] if len(row) > 0 else "",
                        pub_date=row[1] if len(row) > 1 else "",
                        stat_date=row[2] if len(row) > 2 else "",
                        roe=self._safe_float(row[3]) if len(row) > 3 else None,
                        roe_dt=self._safe_float(row[4]) if len(row) > 4 else None,
                        roa=self._safe_float(row[5]) if len(row) > 5 else None,
                        eps=self._safe_float(row[6]) if len(row) > 6 else None,
                        bvps=self._safe_float(row[7]) if len(row) > 7 else None,
                        cfps=self._safe_float(row[8]) if len(row) > 8 else None,
                        net_profit=self._safe_float(row[9]) if len(row) > 9 else None,
                        net_profit_yoy=self._safe_float(row[10]) if len(row) > 10 else None,
                        revenue=self._safe_float(row[11]) if len(row) > 11 else None,
                        revenue_yoy=self._safe_float(row[12]) if len(row) > 12 else None,
                        gross_margin=self._safe_float(row[13]) if len(row) > 13 else None,
                        net_margin=self._safe_float(row[14]) if len(row) > 14 else None,
                        debt_ratio=self._safe_float(row[15]) if len(row) > 15 else None,
                        current_ratio=self._safe_float(row[16]) if len(row) > 16 else None,
                        quick_ratio=self._safe_float(row[17]) if len(row) > 17 else None,
                    )
                    indicators.append(indicator)
                except Exception:
                    continue

            logger.info(f"获取 {stock_code} 财务指标 {len(indicators)} 条")
            return indicators

        except Exception as e:
            logger.error(f"获取财务指标异常: {e}")
            return []

    # ==================== 分红送股 ====================

    def get_dividend(
        self,
        stock_code: str,
        year: str = None,
        year_type: str = "report",
    ) -> List[Dividend]:
        """
        获取分红送股数据

        Args:
            stock_code: 股票代码
            year: 年份
            year_type: 年份类型 report-公告年 oper-实施年

        Returns:
            List[Dividend]: 分红数据列表
        """
        if not self._login():
            return []

        try:
            bs_code = self._get_baostock_code(stock_code)

            rs = bs.query_dividend_data(
                code=bs_code, year=year, yearType=year_type
            )

            if rs.error_code != "0":
                logger.warning(f"获取分红数据失败: {rs.error_msg}")
                return []

            dividends = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if not row:
                    continue

                try:
                    dividend = Dividend(
                        code=row[0] if len(row) > 0 else "",
                        pub_date=row[1] if len(row) > 1 else "",
                        div_year=row[2] if len(row) > 2 else "",
                        ann_date=row[3] if len(row) > 3 else "",
                        record_date=row[4] if len(row) > 4 else "",
                        ex_date=row[5] if len(row) > 5 else "",
                        pay_date=row[6] if len(row) > 6 else "",
                        dividend=self._safe_float(row[7]) if len(row) > 7 else None,
                        transfer=self._safe_float(row[8]) if len(row) > 8 else None,
                        bonus=self._safe_float(row[9]) if len(row) > 9 else None,
                    )
                    dividends.append(dividend)
                except Exception:
                    continue

            return dividends

        except Exception as e:
            logger.error(f"获取分红数据异常: {e}")
            return []

    # ==================== 复权因子 ====================

    def get_adjust_factor(
        self,
        stock_code: str,
        start_date: str = None,
        end_date: str = None,
    ) -> List[AdjustFactor]:
        """
        获取复权因子

        Args:
            stock_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[AdjustFactor]: 复权因子列表
        """
        if not self._login():
            return []

        try:
            bs_code = self._get_baostock_code(stock_code)

            rs = bs.query_adjust_factor(
                code=bs_code,
                start_date=start_date or "1990-01-01",
                end_date=end_date or datetime.now().strftime("%Y-%m-%d"),
            )

            if rs.error_code != "0":
                logger.warning(f"获取复权因子失败: {rs.error_msg}")
                return []

            factors = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if not row:
                    continue

                try:
                    factor = AdjustFactor(
                        code=row[0] if len(row) > 0 else "",
                        date=row[1] if len(row) > 1 else "",
                        fore_adjust=self._safe_float(row[2]) if len(row) > 2 else 1.0,
                        back_adjust=self._safe_float(row[3]) if len(row) > 3 else 1.0,
                    )
                    factors.append(factor)
                except Exception:
                    continue

            return factors

        except Exception as e:
            logger.error(f"获取复权因子异常: {e}")
            return []

    # ==================== 指数数据 ====================

    def get_index_kline(
        self,
        index_code: str,
        start_date: str,
        end_date: str,
        period: str = "d",
    ) -> List[Dict[str, Any]]:
        """
        获取指数K线数据

        Args:
            index_code: 指数代码，如 sh.000001
            start_date: 开始日期
            end_date: 结束日期
            period: 周期 d/w/m

        Returns:
            List[Dict]: K线数据列表
        """
        if not self._login():
            return []

        try:
            fields = "date,code,open,high,low,close,volume,amount"

            rs = bs.query_history_k_data_plus(
                index_code,
                fields,
                start_date=start_date,
                end_date=end_date,
                frequency=period,
            )

            if rs.error_code != "0":
                return []

            klines = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row and len(row) >= 8:
                    klines.append({
                        "date": row[0],
                        "code": row[1],
                        "open": self._safe_float(row[2]),
                        "high": self._safe_float(row[3]),
                        "low": self._safe_float(row[4]),
                        "close": self._safe_float(row[5]),
                        "volume": self._safe_float(row[6]),
                        "amount": self._safe_float(row[7]),
                    })

            return klines

        except Exception as e:
            logger.error(f"获取指数K线异常: {e}")
            return []

    def get_index_stocks(self, index_code: str, date: str = None) -> List[str]:
        """
        获取指数成份股

        Args:
            index_code: 指数代码
            date: 查询日期

        Returns:
            List[str]: 成份股代码列表
        """
        if not self._login():
            return []

        try:
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")

            rs = bs.query_hs300_stocks(date=date)

            if rs.error_code != "0":
                return []

            stocks = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row:
                    stocks.append(row[1])  # 股票代码

            return stocks

        except Exception as e:
            logger.error(f"获取指数成份股异常: {e}")
            return []

    # ==================== 交易日历 ====================

    def get_trade_dates(self, start_date: str, end_date: str) -> List[str]:
        """
        获取交易日历

        Args:
            start_date: 开始日期，格式 YYYY-MM-DD
            end_date: 结束日期，格式 YYYY-MM-DD

        Returns:
            List[str]: 交易日列表
        """
        if not self._login():
            return []

        try:
            rs = bs.query_trade_dates(start_date=start_date, end_date=end_date)

            if rs.error_code != "0":
                return []

            trade_dates = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row and row[1] == "1":
                    trade_dates.append(row[0])

            return trade_dates

        except Exception as e:
            logger.error(f"获取交易日历异常: {e}")
            return []

    def is_trade_date(self, date: str) -> bool:
        """判断是否为交易日"""
        trade_dates = self.get_trade_dates(date, date)
        return len(trade_dates) > 0

    # ==================== 停复牌信息 ====================

    def get_suspend_info(
        self,
        stock_code: str = None,
        start_date: str = None,
        end_date: str = None,
    ) -> List[Dict[str, Any]]:
        """
        获取停复牌信息

        Args:
            stock_code: 股票代码，为空则获取所有
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[Dict]: 停复牌信息列表
        """
        if not self._login():
            return []

        try:
            bs_code = self._get_baostock_code(stock_code) if stock_code else ""

            rs = bs.query_suspend(
                code=bs_code,
                start_date=start_date or "",
                end_date=end_date or "",
            )

            if rs.error_code != "0":
                return []

            suspends = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row:
                    suspends.append({
                        "code": row[0] if len(row) > 0 else "",
                        "suspend_date": row[1] if len(row) > 1 else "",
                        "resume_date": row[2] if len(row) > 2 else "",
                        "reason": row[3] if len(row) > 3 else "",
                    })

            return suspends

        except Exception as e:
            logger.error(f"获取停复牌信息异常: {e}")
            return []

    # ==================== 业绩预告/快报 ====================

    def get_performance_forecast(
        self,
        stock_code: str = None,
        year: int = None,
        quarter: int = None,
    ) -> List[Dict[str, Any]]:
        """
        获取业绩预告

        Args:
            stock_code: 股票代码
            year: 年份
            quarter: 季度

        Returns:
            List[Dict]: 业绩预告列表
        """
        if not self._login():
            return []

        try:
            bs_code = self._get_baostock_code(stock_code) if stock_code else ""

            rs = bs.query_performance_forecast(
                code=bs_code,
                year=year or "",
                quarter=quarter or "",
            )

            if rs.error_code != "0":
                return []

            forecasts = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row:
                    forecasts.append({
                        "code": row[0] if len(row) > 0 else "",
                        "year": row[1] if len(row) > 1 else "",
                        "quarter": row[2] if len(row) > 2 else "",
                        "forecast_type": row[3] if len(row) > 3 else "",
                        "net_profit_min": self._safe_float(row[4]) if len(row) > 4 else None,
                        "net_profit_max": self._safe_float(row[5]) if len(row) > 5 else None,
                        "change_min": self._safe_float(row[6]) if len(row) > 6 else None,
                        "change_max": self._safe_float(row[7]) if len(row) > 7 else None,
                        "pub_date": row[8] if len(row) > 8 else "",
                    })

            return forecasts

        except Exception as e:
            logger.error(f"获取业绩预告异常: {e}")
            return []

    def get_performance_express(
        self,
        stock_code: str = None,
        year: int = None,
        quarter: int = None,
    ) -> List[Dict[str, Any]]:
        """
        获取业绩快报

        Args:
            stock_code: 股票代码
            year: 年份
            quarter: 季度

        Returns:
            List[Dict]: 业绩快报列表
        """
        if not self._login():
            return []

        try:
            bs_code = self._get_baostock_code(stock_code) if stock_code else ""

            rs = bs.query_performance_express(
                code=bs_code,
                year=year or "",
                quarter=quarter or "",
            )

            if rs.error_code != "0":
                return []

            expresses = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row:
                    expresses.append({
                        "code": row[0] if len(row) > 0 else "",
                        "year": row[1] if len(row) > 1 else "",
                        "quarter": row[2] if len(row) > 2 else "",
                        "revenue": self._safe_float(row[3]) if len(row) > 3 else None,
                        "net_profit": self._safe_float(row[4]) if len(row) > 4 else None,
                        "eps": self._safe_float(row[5]) if len(row) > 5 else None,
                        "roe": self._safe_float(row[6]) if len(row) > 6 else None,
                        "pub_date": row[7] if len(row) > 7 else "",
                    })

            return expresses

        except Exception as e:
            logger.error(f"获取业绩快报异常: {e}")
            return []

    # ==================== 增减持 ====================

    def get_stock_hold_changes(
        self,
        stock_code: str = None,
        start_date: str = None,
        end_date: str = None,
    ) -> List[Dict[str, Any]]:
        """
        获取增减持数据

        Args:
            stock_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[Dict]: 增减持列表
        """
        if not self._login():
            return []

        try:
            bs_code = self._get_baostock_code(stock_code) if stock_code else ""

            rs = bs.query_stock_hold_changes(
                code=bs_code,
                start_date=start_date or "",
                end_date=end_date or "",
            )

            if rs.error_code != "0":
                return []

            changes = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row:
                    changes.append({
                        "code": row[0] if len(row) > 0 else "",
                        "holder_name": row[1] if len(row) > 1 else "",
                        "holder_type": row[2] if len(row) > 2 else "",
                        "change_type": row[3] if len(row) > 3 else "",
                        "change_shares": self._safe_float(row[4]) if len(row) > 4 else None,
                        "change_ratio": self._safe_float(row[5]) if len(row) > 5 else None,
                        "change_date": row[6] if len(row) > 6 else "",
                    })

            return changes

        except Exception as e:
            logger.error(f"获取增减持数据异常: {e}")
            return []

    # ==================== 估值指标 ====================

    def get_stock_valuation(
        self,
        stock_code: str,
        start_date: str = None,
        end_date: str = None,
    ) -> List[Dict[str, Any]]:
        """
        获取估值指标 (PE/PB等)

        Args:
            stock_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[Dict]: 估值数据列表
        """
        if not self._login():
            return []

        try:
            bs_code = self._get_baostock_code(stock_code)

            rs = bs.query_history_k_data_plus(
                bs_code,
                "date,code,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                start_date=start_date or "",
                end_date=end_date or "",
                frequency="d",
            )

            if rs.error_code != "0":
                return []

            valuations = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row and len(row) >= 6:
                    valuations.append({
                        "date": row[0],
                        "code": row[1],
                        "pe_ttm": self._safe_float(row[2]),
                        "pb_mrq": self._safe_float(row[3]),
                        "ps_ttm": self._safe_float(row[4]),
                        "pcf_ttm": self._safe_float(row[5]),
                    })

            return valuations

        except Exception as e:
            logger.error(f"获取估值指标异常: {e}")
            return []

    # ==================== 宏观数据 ====================

    def get_macro_economy(self, indicator: str = None) -> List[Dict[str, Any]]:
        """
        获取宏观经济数据

        Args:
            indicator: 指标代码，为空则获取所有

        Returns:
            List[Dict]: 宏观数据列表
        """
        if not self._login():
            return []

        try:
            rs = bs.query_macro_economy(indicator=indicator or "")

            if rs.error_code != "0":
                return []

            data = []
            while (rs.error_code == "0") & rs.next():
                row = rs.get_row_data()
                if row:
                    data.append({
                        "indicator": row[0] if len(row) > 0 else "",
                        "indicator_name": row[1] if len(row) > 1 else "",
                        "date": row[2] if len(row) > 2 else "",
                        "value": self._safe_float(row[3]) if len(row) > 3 else None,
                    })

            return data

        except Exception as e:
            logger.error(f"获取宏观数据异常: {e}")
            return []

    # ==================== 工具方法 ====================

    def _safe_float(self, value) -> Optional[float]:
        """安全转换为浮点数"""
        if value is None or value == "" or value == "--":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None


baostock_source = BaostockSource()