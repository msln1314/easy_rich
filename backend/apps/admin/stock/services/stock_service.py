#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/10
# @File           : stock_service.py
# @IDE            : PyCharm
# @desc           : 股票服务层 - 封装数据获取逻辑，支持多数据源（AKShare、新浪、掘金量化）

from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
import akshare as ak
import pandas as pd
import requests
from core.logger import logger


# 主要指数代码映射
INDEX_CODES = {
    "sh000001": {"name": "上证指数", "code": "000001.SH", "gm_code": "SHSE.000001"},
    "sz399001": {"name": "深证成指", "code": "399001.SZ", "gm_code": "SZSE.399001"},
    "sz399006": {"name": "创业板指", "code": "399006.SZ", "gm_code": "SZSE.399006"},
    "sh000688": {"name": "科创50", "code": "000688.SH", "gm_code": "SHSE.000688"},
}

# 新浪指数接口配置
SINA_INDEX_URL = "http://hq.sinajs.cn/list=sh000001,sz399001,sz399006,sh000688"

# 新浪股票接口基础URL
SINA_STOCK_URL = "http://hq.sinajs.cn/list="


def _get_gm_service():
    """获取 GM 服务实例"""
    try:
        from apps.admin.stock.services.gm_service import gm_service
        return gm_service
    except ImportError:
        return None


class StockIndexService:
    """大盘指数服务类 - 支持多数据源"""

    @staticmethod
    def get_index_quote() -> List[Dict[str, Any]]:
        """
        获取主要指数实时行情

        Returns:
            指数行情列表
        """
        # 数据源优先级：AKShare > 新浪 > GM

        # 1. 尝试 AKShare 接口
        result = StockIndexService._try_akshare_index()
        if result:
            return result

        # 2. 备用：新浪接口
        result = StockIndexService._try_sina_index()
        if result:
            return result

        # 3. 备用：掘金量化
        result = StockIndexService._try_gm_index()
        if result:
            return result

        logger.warning("所有数据源均无法获取指数行情")
        return []

    @staticmethod
    def _try_akshare_index() -> Optional[List[Dict[str, Any]]]:
        """尝试使用 AKShare 获取指数行情"""
        try:
            df = ak.stock_zh_index_spot_em(symbol="沪深重要指数")
            if df is None or df.empty:
                return None

            # 主要指数代码
            main_codes = ["000001", "399001", "399006", "000688"]
            df_main = df[df["代码"].isin(main_codes)]

            items = []
            for _, row in df_main.iterrows():
                code = str(row["代码"])
                # 转换代码格式
                if code in ["000001", "000688"]:
                    std_code = f"{code}.SH"
                else:
                    std_code = f"{code}.SZ"

                items.append({
                    "index_code": std_code,
                    "index_name": str(row["名称"]),
                    "current_price": float(row["最新价"]) if pd.notna(row["最新价"]) else None,
                    "change_percent": float(row["涨跌幅"]) if pd.notna(row["涨跌幅"]) else None,
                    "change_amount": float(row["涨跌额"]) if pd.notna(row["涨跌额"]) else None,
                    "volume": float(row["成交量"]) / 100 if pd.notna(row["成交量"]) else None,
                    "amount": float(row["成交额"]) if pd.notna(row["成交额"]) else None,
                })

            logger.info(f"AKShare 获取到 {len(items)} 条指数数据")
            return items

        except Exception as e:
            logger.warning(f"AKShare 指数接口失败: {str(e)}")
            return None

    @staticmethod
    def _try_sina_index() -> Optional[List[Dict[str, Any]]]:
        """尝试使用新浪接口获取指数行情"""
        try:
            headers = {
                "Referer": "http://finance.sina.com.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(SINA_INDEX_URL, headers=headers, timeout=10)
            response.encoding = "gbk"

            if response.status_code != 200:
                return None

            items = []
            for line in response.text.strip().split('\n'):
                if not line or 'hq_str_' not in line:
                    continue

                try:
                    # 解析格式: var hq_str_sh000001="上证指数,3391.88,..."
                    code_part, data_part = line.split('="')
                    raw_code = code_part.replace('var hq_str_', '').upper()
                    data = data_part.rstrip('";').split(',')

                    if len(data) < 10:
                        continue

                    name = data[0]
                    open_price = float(data[1]) if data[1] else None
                    pre_close = float(data[2]) if data[2] else None
                    price = float(data[3]) if data[3] else None
                    high = float(data[4]) if data[4] else None
                    low = float(data[5]) if data[5] else None
                    volume = float(data[8]) if data[8] else None
                    amount = float(data[9]) if data[9] else None

                    change = round(price - pre_close, 2) if price and pre_close else None
                    change_percent = round((price - pre_close) / pre_close * 100, 2) if price and pre_close else None

                    # 转换代码格式
                    if raw_code.startswith('SH'):
                        std_code = raw_code.replace('SH', '') + '.SH'
                    else:
                        std_code = raw_code.replace('SZ', '') + '.SZ'

                    items.append({
                        "index_code": std_code,
                        "index_name": name,
                        "current_price": price,
                        "change_percent": change_percent,
                        "change_amount": change,
                        "volume": volume / 100 if volume else None,
                        "amount": amount,
                        "open_price": open_price,
                        "high_price": high,
                        "low_price": low,
                        "pre_close": pre_close,
                    })

                except Exception as e:
                    logger.warning(f"解析新浪指数数据失败: {e}")
                    continue

            logger.info(f"新浪接口获取到 {len(items)} 条指数数据")
            return items

        except Exception as e:
            logger.warning(f"新浪指数接口失败: {str(e)}")
            return None

    @staticmethod
    def _try_gm_index() -> Optional[List[Dict[str, Any]]]:
        """尝试使用掘金量化获取指数行情"""
        try:
            gm = _get_gm_service()
            if not gm or not gm.is_available():
                return None

            # 获取主要指数的 GM 代码列表
            gm_codes = [v["gm_code"] for v in INDEX_CODES.values()]

            # 使用 GM 的 current 方法获取实时行情
            quotes = gm.gm.current(symbols=gm_codes)

            if not quotes:
                return None

            items = []
            for quote in quotes:
                try:
                    gm_symbol = quote.get("symbol", "")
                    # 查找对应的标准代码
                    std_code = None
                    name = ""
                    for code, info in INDEX_CODES.items():
                        if info.get("gm_code") == gm_symbol:
                            std_code = info["code"]
                            name = info["name"]
                            break

                    if not std_code:
                        continue

                    price = float(quote.get("last", 0) or 0)
                    pre_close = float(quote.get("pre_close", 0) or 0)

                    items.append({
                        "index_code": std_code,
                        "index_name": name,
                        "current_price": price,
                        "change_percent": round((price - pre_close) / pre_close * 100, 2) if pre_close else None,
                        "change_amount": round(price - pre_close, 2) if price and pre_close else None,
                        "volume": float(quote.get("volume", 0) or 0),
                        "amount": float(quote.get("amount", 0) or 0),
                        "open_price": float(quote.get("open", 0) or 0),
                        "high_price": float(quote.get("high", 0) or 0),
                        "low_price": float(quote.get("low", 0) or 0),
                        "pre_close": pre_close,
                    })

                except Exception as e:
                    logger.warning(f"解析 GM 指数数据失败: {e}")
                    continue

            logger.info(f"GM 获取到 {len(items)} 条指数数据")
            return items

        except Exception as e:
            logger.warning(f"GM 指数接口失败: {str(e)}")
            return None

    @staticmethod
    def get_index_history(
        index_code: str,
        period: str = "daily",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        获取指数历史K线数据

        Args:
            index_code: 指数代码
            period: 周期
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            K线数据列表
        """
        # 尝试 AKShare
        result = StockIndexService._try_akshare_history(index_code, start_date, end_date)
        if result:
            return result

        # 尝试 GM
        result = StockIndexService._try_gm_history(index_code, start_date, end_date)
        if result:
            return result

        return []

    @staticmethod
    def _try_akshare_history(index_code: str, start_date: Optional[str], end_date: Optional[str]) -> Optional[List[Dict[str, Any]]]:
        """尝试使用 AKShare 获取历史数据"""
        try:
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            if not start_date:
                start_date = (datetime.now() - timedelta(days=300)).strftime("%Y%m%d")

            df = ak.stock_zh_index_daily(symbol=index_code)
            if df is None or df.empty:
                return None

            df["date"] = pd.to_datetime(df["date"])
            start_dt = datetime.strptime(start_date, "%Y%m%d")
            end_dt = datetime.strptime(end_date, "%Y%m%d")
            df = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]

            items = []
            for _, row in df.iterrows():
                items.append({
                    "date": row["date"].strftime("%Y-%m-%d"),
                    "open": float(row["open"]) if pd.notna(row["open"]) else None,
                    "high": float(row["high"]) if pd.notna(row["high"]) else None,
                    "low": float(row["low"]) if pd.notna(row["low"]) else None,
                    "close": float(row["close"]) if pd.notna(row["close"]) else None,
                    "volume": float(row["volume"]) / 100 if pd.notna(row["volume"]) else None,
                    "amount": float(row.get("amount", 0)) if pd.notna(row.get("amount", 0)) else None,
                })

            logger.info(f"AKShare 获取到 {len(items)} 条历史数据")
            return items

        except Exception as e:
            logger.warning(f"AKShare 历史接口失败: {str(e)}")
            return None

    @staticmethod
    def _try_gm_history(index_code: str, start_date: Optional[str], end_date: Optional[str]) -> Optional[List[Dict[str, Any]]]:
        """尝试使用 GM 获取历史数据"""
        try:
            gm = _get_gm_service()
            if not gm or not gm.is_available():
                return None

            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            if not start_date:
                start_date = (datetime.now() - timedelta(days=300)).strftime("%Y%m%d")

            # 转换代码格式
            gm_code = None
            for code, info in INDEX_CODES.items():
                if info["code"] == index_code or code == index_code:
                    gm_code = info["gm_code"]
                    break

            if not gm_code:
                return None

            # 格式化日期
            start_time = f"{start_date} 09:30:00"
            end_time = f"{end_date} 15:00:00"

            # 使用 GM 的 history 方法
            history_data = gm.gm.history(
                symbol=gm_code,
                frequency='1d',
                start_time=start_time,
                end_time=end_time,
                adjust=0
            )

            if not history_data:
                return None

            items = []
            for item in history_data:
                eob = item.get('eob', '')
                date_str = eob.strftime('%Y-%m-%d') if hasattr(eob, 'strftime') else str(eob)[:10]
                items.append({
                    "date": date_str,
                    "open": float(item.get('open', 0) or 0),
                    "high": float(item.get('high', 0) or 0),
                    "low": float(item.get('low', 0) or 0),
                    "close": float(item.get('close', 0) or 0),
                    "volume": float(item.get('volume', 0) or 0),
                })

            logger.info(f"GM 获取到 {len(items)} 条历史数据")
            return items

        except Exception as e:
            logger.warning(f"GM 历史接口失败: {str(e)}")
            return None


class StockQuoteService:
    """股票实时行情服务类 - 支持多数据源"""

    _stock_cache: Dict[str, Any] = {}
    _cache_time: Optional[datetime] = None

    @classmethod
    def get_stock_quote(cls, stock_code: str) -> Optional[Dict[str, Any]]:
        """
        获取单个股票实时行情

        Args:
            stock_code: 股票代码（如 000001 或 000001.SZ）

        Returns:
            股票行情数据
        """
        # 标准化股票代码
        std_code = cls._normalize_code(stock_code)

        # 尝试 AKShare
        result = cls._try_akshare_quote(std_code)
        if result:
            return result

        # 尝试新浪
        result = cls._try_sina_quote(std_code)
        if result:
            return result

        # 尝试 GM
        result = cls._try_gm_quote(std_code)
        if result:
            return result

        logger.warning(f"所有数据源均无法获取股票 {stock_code} 行情")
        return None

    @classmethod
    def get_stock_quotes(cls, stock_codes: List[str]) -> List[Dict[str, Any]]:
        """
        批量获取股票实时行情

        Args:
            stock_codes: 股票代码列表

        Returns:
            股票行情列表
        """
        if not stock_codes:
            return []

        # 标准化代码
        std_codes = [cls._normalize_code(code) for code in stock_codes]

        # 尝试 AKShare
        result = cls._try_akshare_quotes(std_codes)
        if result:
            return result

        # 尝试新浪
        result = cls._try_sina_quotes(std_codes)
        if result:
            return result

        # 尝试 GM
        result = cls._try_gm_quotes(std_codes)
        if result:
            return result

        logger.warning("所有数据源均无法获取股票行情")
        return []

    @staticmethod
    def _normalize_code(code: str) -> str:
        """标准化股票代码"""
        code = code.strip().upper()
        # 如果已经有后缀，直接返回
        if "." in code:
            return code
        # 根据代码前缀判断市场
        if code.startswith(("6", "5")):
            return f"{code}.SH"
        else:
            return f"{code}.SZ"

    @staticmethod
    def _code_to_sina(code: str) -> str:
        """标准代码转新浪代码"""
        if "." not in code:
            return code.lower()
        pure_code, market = code.split(".")
        if market == "SH":
            return f"sh{pure_code}"
        else:
            return f"sz{pure_code}"

    @staticmethod
    def _code_to_gm(code: str) -> str:
        """标准代码转 GM 代码"""
        if "." not in code:
            # 根据前缀判断
            if code.startswith(("6", "5")):
                return f"SHSE.{code}"
            else:
                return f"SZSE.{code}"
        pure_code, market = code.split(".")
        if market == "SH":
            return f"SHSE.{pure_code}"
        else:
            return f"SZSE.{pure_code}"

    @classmethod
    def _try_akshare_quote(cls, std_code: str) -> Optional[Dict[str, Any]]:
        """尝试使用 AKShare 获取单个股票行情"""
        try:
            df = ak.stock_zh_a_spot_em()
            if df is None or df.empty:
                return None

            pure_code = std_code.split(".")[0]
            row = df[df["代码"] == pure_code]

            if row.empty:
                return None

            row = row.iloc[0]
            pre_close = float(row["昨收"]) if pd.notna(row["昨收"]) else None
            price = float(row["最新价"]) if pd.notna(row["最新价"]) else None

            return {
                "stock_code": std_code,
                "stock_name": str(row["名称"]),
                "current_price": price,
                "open_price": float(row["今开"]) if pd.notna(row["今开"]) else None,
                "high_price": float(row["最高"]) if pd.notna(row["最高"]) else None,
                "low_price": float(row["最低"]) if pd.notna(row["最低"]) else None,
                "pre_close": pre_close,
                "change_percent": float(row["涨跌幅"]) if pd.notna(row["涨跌幅"]) else None,
                "change_amount": float(row["涨跌额"]) if pd.notna(row["涨跌额"]) else None,
                "volume": float(row["成交量"]) if pd.notna(row["成交量"]) else None,
                "amount": float(row["成交额"]) if pd.notna(row["成交额"]) else None,
                "turnover_rate": float(row["换手率"]) if pd.notna(row["换手率"]) else None,
                "pe_ratio": float(row["市盈率-动态"]) if pd.notna(row.get("市盈率-动态")) else None,
                "pb_ratio": float(row["市净率"]) if pd.notna(row.get("市净率")) else None,
                "total_market_cap": float(row["总市值"]) if pd.notna(row.get("总市值")) else None,
                "circulating_market_cap": float(row["流通市值"]) if pd.notna(row.get("流通市值")) else None,
                "update_time": datetime.now(),
                "data_source": "akshare",
            }

        except Exception as e:
            logger.warning(f"AKShare 获取股票行情失败: {str(e)}")
            return None

    @classmethod
    def _try_akshare_quotes(cls, std_codes: List[str]) -> Optional[List[Dict[str, Any]]]:
        """尝试使用 AKShare 批量获取股票行情"""
        try:
            df = ak.stock_zh_a_spot_em()
            if df is None or df.empty:
                return None

            pure_codes = [code.split(".")[0] for code in std_codes]
            df_filtered = df[df["代码"].isin(pure_codes)]

            items = []
            for _, row in df_filtered.iterrows():
                pure_code = str(row["代码"])
                # 恢复标准代码
                std_code = cls._normalize_code(pure_code)

                pre_close = float(row["昨收"]) if pd.notna(row["昨收"]) else None
                price = float(row["最新价"]) if pd.notna(row["最新价"]) else None

                items.append({
                    "stock_code": std_code,
                    "stock_name": str(row["名称"]),
                    "current_price": price,
                    "open_price": float(row["今开"]) if pd.notna(row["今开"]) else None,
                    "high_price": float(row["最高"]) if pd.notna(row["最高"]) else None,
                    "low_price": float(row["最低"]) if pd.notna(row["最低"]) else None,
                    "pre_close": pre_close,
                    "change_percent": float(row["涨跌幅"]) if pd.notna(row["涨跌幅"]) else None,
                    "change_amount": float(row["涨跌额"]) if pd.notna(row["涨跌额"]) else None,
                    "volume": float(row["成交量"]) if pd.notna(row["成交量"]) else None,
                    "amount": float(row["成交额"]) if pd.notna(row["成交额"]) else None,
                    "turnover_rate": float(row["换手率"]) if pd.notna(row["换手率"]) else None,
                    "update_time": datetime.now(),
                    "data_source": "akshare",
                })

            logger.info(f"AKShare 获取到 {len(items)} 条股票行情")
            return items

        except Exception as e:
            logger.warning(f"AKShare 批量获取股票行情失败: {str(e)}")
            return None

    @classmethod
    def _try_sina_quote(cls, std_code: str) -> Optional[Dict[str, Any]]:
        """尝试使用新浪接口获取单个股票行情"""
        try:
            sina_code = cls._code_to_sina(std_code)
            url = f"{SINA_STOCK_URL}{sina_code}"

            headers = {
                "Referer": "http://finance.sina.com.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "gbk"

            if response.status_code != 200:
                return None

            # 解析数据
            data_str = response.text.strip()
            if 'hq_str_' not in data_str:
                return None

            data_part = data_str.split('="')[1].rstrip('";')
            data = data_part.split(',')

            if len(data) < 32:
                return None

            name = data[0]
            open_price = float(data[1]) if data[1] else None
            pre_close = float(data[2]) if data[2] else None
            price = float(data[3]) if data[3] else None
            high = float(data[4]) if data[4] else None
            low = float(data[5]) if data[5] else None
            volume = float(data[8]) if data[8] else None
            amount = float(data[9]) if data[9] else None

            change = round(price - pre_close, 2) if price and pre_close else None
            change_percent = round((price - pre_close) / pre_close * 100, 2) if price and pre_close else None

            return {
                "stock_code": std_code,
                "stock_name": name,
                "current_price": price,
                "open_price": open_price,
                "high_price": high,
                "low_price": low,
                "pre_close": pre_close,
                "change_percent": change_percent,
                "change_amount": change,
                "volume": volume,
                "amount": amount,
                "update_time": datetime.now(),
                "data_source": "sina",
            }

        except Exception as e:
            logger.warning(f"新浪获取股票行情失败: {str(e)}")
            return None

    @classmethod
    def _try_sina_quotes(cls, std_codes: List[str]) -> Optional[List[Dict[str, Any]]]:
        """尝试使用新浪接口批量获取股票行情"""
        try:
            sina_codes = [cls._code_to_sina(code) for code in std_codes]
            url = f"{SINA_STOCK_URL}{','.join(sina_codes)}"

            headers = {
                "Referer": "http://finance.sina.com.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "gbk"

            if response.status_code != 200:
                return None

            items = []
            for line in response.text.strip().split('\n'):
                if not line or 'hq_str_' not in line:
                    continue

                try:
                    code_part, data_part = line.split('="')
                    sina_code = code_part.replace('var hq_str_', '').upper()
                    data = data_part.rstrip('";').split(',')

                    if len(data) < 32:
                        continue

                    # 转回标准代码
                    pure_code = sina_code[2:] if sina_code.startswith(('SH', 'SZ')) else sina_code
                    market = "SH" if sina_code.startswith('SH') else "SZ"
                    std_code = f"{pure_code}.{market}"

                    name = data[0]
                    open_price = float(data[1]) if data[1] else None
                    pre_close = float(data[2]) if data[2] else None
                    price = float(data[3]) if data[3] else None
                    high = float(data[4]) if data[4] else None
                    low = float(data[5]) if data[5] else None
                    volume = float(data[8]) if data[8] else None
                    amount = float(data[9]) if data[9] else None

                    change = round(price - pre_close, 2) if price and pre_close else None
                    change_percent = round((price - pre_close) / pre_close * 100, 2) if price and pre_close else None

                    items.append({
                        "stock_code": std_code,
                        "stock_name": name,
                        "current_price": price,
                        "open_price": open_price,
                        "high_price": high,
                        "low_price": low,
                        "pre_close": pre_close,
                        "change_percent": change_percent,
                        "change_amount": change,
                        "volume": volume,
                        "amount": amount,
                        "update_time": datetime.now(),
                        "data_source": "sina",
                    })

                except Exception as e:
                    logger.warning(f"解析新浪股票数据失败: {e}")
                    continue

            logger.info(f"新浪获取到 {len(items)} 条股票行情")
            return items

        except Exception as e:
            logger.warning(f"新浪批量获取股票行情失败: {str(e)}")
            return None

    @classmethod
    def _try_gm_quote(cls, std_code: str) -> Optional[Dict[str, Any]]:
        """尝试使用 GM 获取单个股票行情"""
        try:
            gm = _get_gm_service()
            if not gm or not gm.is_available():
                return None

            gm_code = cls._code_to_gm(std_code)
            logger.info(f"GM 代码转换: {std_code} -> {gm_code}")
            quotes = gm.gm.current(symbols=[gm_code])

            if not quotes:
                return None

            quote = quotes[0]
            price = float(quote.get("last", 0) or 0)
            pre_close = float(quote.get("pre_close", 0) or 0)

            return {
                "stock_code": std_code,
                "stock_name": quote.get("sec_name", ""),
                "current_price": price,
                "open_price": float(quote.get("open", 0) or 0),
                "high_price": float(quote.get("high", 0) or 0),
                "low_price": float(quote.get("low", 0) or 0),
                "pre_close": pre_close,
                "change_percent": round((price - pre_close) / pre_close * 100, 2) if pre_close else None,
                "change_amount": round(price - pre_close, 2) if price and pre_close else None,
                "volume": float(quote.get("volume", 0) or 0),
                "amount": float(quote.get("amount", 0) or 0),
                "update_time": datetime.now(),
                "data_source": "gm",
            }

        except Exception as e:
            logger.warning(f"GM 获取股票行情失败: {str(e)}")
            return None

    @classmethod
    def _try_gm_quotes(cls, std_codes: List[str]) -> Optional[List[Dict[str, Any]]]:
        """尝试使用 GM 批量获取股票行情"""
        try:
            gm = _get_gm_service()
            if not gm or not gm.is_available():
                return None

            gm_codes = [cls._code_to_gm(code) for code in std_codes]
            quotes = gm.gm.current(symbols=gm_codes)

            if not quotes:
                return None

            items = []
            for quote in quotes:
                try:
                    gm_symbol = quote.get("symbol", "")
                    # 转回标准代码
                    pure_code = gm_symbol.split(".")[1] if "." in gm_symbol else gm_symbol
                    market = "SH" if gm_symbol.startswith("SHSE") else "SZ"
                    std_code = f"{pure_code}.{market}"

                    price = float(quote.get("last", 0) or 0)
                    pre_close = float(quote.get("pre_close", 0) or 0)

                    items.append({
                        "stock_code": std_code,
                        "stock_name": quote.get("sec_name", ""),
                        "current_price": price,
                        "open_price": float(quote.get("open", 0) or 0),
                        "high_price": float(quote.get("high", 0) or 0),
                        "low_price": float(quote.get("low", 0) or 0),
                        "pre_close": pre_close,
                        "change_percent": round((price - pre_close) / pre_close * 100, 2) if pre_close else None,
                        "change_amount": round(price - pre_close, 2) if price and pre_close else None,
                        "volume": float(quote.get("volume", 0) or 0),
                        "amount": float(quote.get("amount", 0) or 0),
                        "update_time": datetime.now(),
                        "data_source": "gm",
                    })

                except Exception as e:
                    logger.warning(f"解析 GM 股票数据失败: {e}")
                    continue

            logger.info(f"GM 获取到 {len(items)} 条股票行情")
            return items

        except Exception as e:
            logger.warning(f"GM 批量获取股票行情失败: {str(e)}")
            return None

    @classmethod
    def get_stock_history(
        cls,
        stock_code: str,
        period: str = "daily",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        获取股票历史K线数据

        Args:
            stock_code: 股票代码
            period: 周期 (daily/weekly/monthly)
            start_date: 开始日期 YYYYMMDD
            end_date: 结束日期 YYYYMMDD

        Returns:
            K线数据列表
        """
        std_code = cls._normalize_code(stock_code)

        # 尝试 AKShare
        result = cls._try_akshare_history(std_code, period, start_date, end_date)
        if result:
            return result

        # 尝试 GM
        result = cls._try_gm_history(std_code, period, start_date, end_date)
        if result:
            return result

        return []

    @classmethod
    def _try_akshare_history(
        cls,
        std_code: str,
        period: str,
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> Optional[List[Dict[str, Any]]]:
        """尝试使用 AKShare 获取历史数据"""
        try:
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            if not start_date:
                start_date = (datetime.now() - timedelta(days=300)).strftime("%Y%m%d")

            pure_code = std_code.split(".")[0]

            df = ak.stock_zh_a_hist(
                symbol=pure_code,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust=""
            )

            if df is None or df.empty:
                return None

            items = []
            for _, row in df.iterrows():
                items.append({
                    "date": str(row["日期"]),
                    "open": float(row["开盘"]) if pd.notna(row.get("开盘")) else None,
                    "high": float(row["最高"]) if pd.notna(row.get("最高")) else None,
                    "low": float(row["最低"]) if pd.notna(row.get("最低")) else None,
                    "close": float(row["收盘"]) if pd.notna(row.get("收盘")) else None,
                    "volume": float(row["成交量"]) if pd.notna(row.get("成交量")) else None,
                    "amount": float(row["成交额"]) if pd.notna(row.get("成交额")) else None,
                    "change_percent": float(row["涨跌幅"]) if pd.notna(row.get("涨跌幅")) else None,
                    "change_amount": float(row["涨跌额"]) if pd.notna(row.get("涨跌额")) else None,
                    "turnover_rate": float(row["换手率"]) if pd.notna(row.get("换手率")) else None,
                })

            logger.info(f"AKShare 获取到 {len(items)} 条历史数据")
            return items

        except Exception as e:
            logger.warning(f"AKShare 获取历史数据失败: {str(e)}")
            return None

    @classmethod
    def _try_gm_history(
        cls,
        std_code: str,
        period: str,
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> Optional[List[Dict[str, Any]]]:
        """尝试使用 GM 获取历史数据"""
        try:
            gm = _get_gm_service()
            if not gm or not gm.is_available():
                return None

            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            if not start_date:
                start_date = (datetime.now() - timedelta(days=300)).strftime("%Y%m%d")

            gm_code = cls._code_to_gm(std_code)

            # 频率映射
            freq_map = {
                "daily": "1d",
                "weekly": "1w",
                "monthly": "1mon",
            }
            frequency = freq_map.get(period, "1d")

            # 格式化日期
            start_time = f"{start_date} 09:30:00"
            end_time = f"{end_date} 15:00:00"

            history_data = gm.gm.history(
                symbol=gm_code,
                frequency=frequency,
                start_time=start_time,
                end_time=end_time,
                adjust=0
            )

            if not history_data:
                return None

            items = []
            for item in history_data:
                eob = item.get('eob', '')
                date_str = eob.strftime('%Y-%m-%d') if hasattr(eob, 'strftime') else str(eob)[:10]
                close = float(item.get('close', 0) or 0)
                pre_close = float(item.get('pre_close', 0) or 0)

                items.append({
                    "date": date_str,
                    "open": float(item.get('open', 0) or 0),
                    "high": float(item.get('high', 0) or 0),
                    "low": float(item.get('low', 0) or 0),
                    "close": close,
                    "volume": float(item.get('volume', 0) or 0),
                    "amount": float(item.get('amount', 0) or 0),
                    "change_percent": round((close - pre_close) / pre_close * 100, 2) if pre_close else None,
                    "change_amount": round(close - pre_close, 2) if close and pre_close else None,
                })

            logger.info(f"GM 获取到 {len(items)} 条历史数据")
            return items

        except Exception as e:
            logger.warning(f"GM 获取历史数据失败: {str(e)}")
            return None


class MarketSummaryService:
    """市场汇总服务类 - 封装市场数据获取逻辑"""

    @staticmethod
    def get_market_summary() -> Dict[str, Any]:
        """
        获取市场汇总数据

        Returns:
            市场汇总数据
        """
        try:
            # 1. 获取主要指数
            index_items = StockIndexService.get_index_quote()

            # 2. 尝试获取市场涨跌统计
            market_stats = MarketSummaryService._get_market_stats()

            return {
                "indices": index_items,
                **market_stats,
                "trade_date": str(date.today()),
                "update_time": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"获取市场汇总失败: {str(e)}")
            return {}

    @staticmethod
    def _get_market_stats() -> Dict[str, Any]:
        """获取市场统计数据"""
        try:
            df_stock = ak.stock_zh_a_spot_em()
            if df_stock is not None and not df_stock.empty:
                total_stocks = len(df_stock)
                up_stocks = len(df_stock[df_stock["涨跌幅"] > 0])
                down_stocks = len(df_stock[df_stock["涨跌幅"] < 0])
                flat_stocks = len(df_stock[df_stock["涨跌幅"] == 0])
                total_amount = float(df_stock["成交额"].sum()) if "成交额" in df_stock.columns else 0
                total_volume = float(df_stock["成交量"].sum()) if "成交量" in df_stock.columns else 0
                limit_up_count = len(df_stock[df_stock["涨跌幅"] >= 9.9])
                limit_down_count = len(df_stock[df_stock["涨跌幅"] <= -9.9])

                return {
                    "total_stocks": total_stocks,
                    "up_stocks": up_stocks,
                    "down_stocks": down_stocks,
                    "flat_stocks": flat_stocks,
                    "total_amount": total_amount,
                    "total_volume": total_volume,
                    "limit_up_count": limit_up_count,
                    "limit_down_count": limit_down_count,
                }
        except Exception as e:
            logger.warning(f"获取市场统计失败: {str(e)}")

        # 返回默认值
        return {
            "total_stocks": 0,
            "up_stocks": 0,
            "down_stocks": 0,
            "flat_stocks": 0,
            "total_amount": 0,
            "total_volume": 0,
            "limit_up_count": 0,
            "limit_down_count": 0,
        }


class StockRankingService:
    """股票排行服务类 - 封装排行数据获取逻辑"""

    def __init__(self):
        """初始化，缓存股票数据"""
        self._stock_cache: Optional[List[Dict[str, Any]]] = None
        self._cache_time: Optional[datetime] = None

    def _get_stock_data(self) -> List[Dict[str, Any]]:
        """获取股票数据（带缓存）"""
        now = datetime.now()
        # 缓存 30 秒
        if self._stock_cache and self._cache_time:
            if (now - self._cache_time).seconds < 30:
                return self._stock_cache

        # 尝试 AKShare
        stocks = self._try_akshare_stocks()
        if stocks:
            self._stock_cache = stocks
            self._cache_time = now
            return stocks

        # 返回缓存数据
        return self._stock_cache or []

    def _try_akshare_stocks(self) -> Optional[List[Dict[str, Any]]]:
        """尝试使用 AKShare 获取股票数据"""
        try:
            df = ak.stock_zh_a_spot_em()
            if df is None or df.empty:
                return None

            # 过滤 ST 股票和退市股票
            df = df[~df["名称"].str.contains("ST|退", na=False)]

            records = df.to_dict("records")
            logger.info(f"AKShare 获取到 {len(records)} 条股票数据")
            return records

        except Exception as e:
            logger.warning(f"AKShare 股票接口失败: {str(e)}")
            return None

    def get_change_percent_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取涨跌幅排行"""
        stocks = self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("涨跌幅", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    def get_turnover_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取换手率排行"""
        stocks = self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("换手率", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    def get_volume_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取成交量排行"""
        stocks = self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("成交量", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    def get_amount_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取成交额排行"""
        stocks = self._get_stock_data()
        sorted_stocks = sorted(stocks, key=lambda x: x.get("成交额", 0) or 0, reverse=True)
        return self._format_ranking(sorted_stocks[:limit])

    def _format_ranking(self, stocks: List[Dict]) -> List[Dict[str, Any]]:
        """格式化排行数据"""
        items = []
        for idx, s in enumerate(stocks):
            code = str(s.get("代码", ""))
            items.append({
                "rank": idx + 1,
                "stock_code": code,
                "stock_name": s.get("名称", ""),
                "current_price": float(s["最新价"]) if pd.notna(s.get("最新价")) else None,
                "change_percent": float(s["涨跌幅"]) if pd.notna(s.get("涨跌幅")) else None,
                "volume": float(s["成交量"]) / 100 if pd.notna(s.get("成交量")) else None,
                "amount": float(s["成交额"]) if pd.notna(s.get("成交额")) else None,
                "turnover_rate": float(s["换手率"]) if pd.notna(s.get("换手率")) else None,
                "industry": s.get("所属行业", ""),
                "market": "SH" if code.startswith(("6", "5")) else "SZ",
            })
        return items


# 全局服务实例
stock_index_service = StockIndexService()
stock_quote_service = StockQuoteService()
market_summary_service = MarketSummaryService()
stock_ranking_service = StockRankingService()