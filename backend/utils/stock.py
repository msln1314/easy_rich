#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/1
# @File           : stock.py
# @IDE            : PyCharm
# @desc           : 股票工具类，包含股票相关的常用静态方法

from typing import Dict, Any, Optional, List
from datetime import datetime


class StockUtils:
    """股票工具类，提供股票相关的常用静态方法"""

    @staticmethod
    def get_market_prefix(stock_code: str) -> str:
        """
        获取股票市场前缀
        
        Args:
            stock_code: 股票代码，如 "600000" 或 "SZ000001"
            
        Returns:
            str: 市场前缀，如 "SH"、"SZ"、"BJ"
        """
        if not stock_code:
            return "SH"
        
        # 如果已经包含前缀，提取前缀
        if len(stock_code) >= 2:
            prefix = stock_code[:2].upper()
            if prefix in ["SH", "SZ", "BJ"]:
                return prefix
        
        # 根据代码判断市场
        if stock_code.startswith(("6", "9")):
            return "SH"
        elif stock_code.startswith(("0", "3", "2")):
            return "SZ"
        elif stock_code.startswith("8"):
            return "BJ"
        else:
            return "SH"  # 默认

    @staticmethod
    def get_full_code(stock_code: str) -> str:
        """
        获取完整的股票代码（带市场前缀）
        
        Args:
            stock_code: 股票代码，如 "600000" 或 "SZ000001"
            
        Returns:
            str: 完整的股票代码，如 "SH600000" 或 "SZ000001"
        """
        if not stock_code:
            return ""
        
        # 如果已经包含前缀，直接返回
        if len(stock_code) >= 2:
            prefix = stock_code[:2].upper()
            if prefix in ["SH", "SZ", "BJ"]:
                return stock_code
        
        # 根据代码添加前缀
        market_prefix = StockUtils.get_market_prefix(stock_code)
        
        # 确保股票代码是6位
        code = stock_code.zfill(6) if len(stock_code) == 6 else stock_code
        
        return f"{market_prefix}{code}"

    @staticmethod
    def get_stock_code(full_code: str) -> str:
        """
        从完整股票代码中提取股票代码
        
        Args:
            full_code: 完整的股票代码，如 "SH600000" 或 "SZ000001"
            
        Returns:
            str: 股票代码，如 "600000"
        """
        if not full_code:
            return ""
        
        # 如果包含前缀，提取股票代码
        if len(full_code) >= 2:
            prefix = full_code[:2].upper()
            if prefix in ["SH", "SZ", "BJ"]:
                return full_code[2:]
        
        # 如果没有前缀，直接返回
        return full_code

    @staticmethod
    def convert_to_gm_symbol(stock_code: str) -> str:
        """
        将股票代码转换为 GM 需要的格式
        
        Args:
            stock_code: 股票代码，如 "600000" 或 "SZ000001"
            
        Returns:
            str: GM 格式的股票代码，如 "SHSE.600000"
        """
        if not stock_code:
            return ""
        
        # 提取股票代码（去除可能的前缀）
        code = StockUtils.get_stock_code(stock_code)
        
        # 获取市场前缀
        prefix = StockUtils.get_market_prefix(stock_code)
        
        # 映射市场代码
        market_map = {
            "SH": "SHSE",
            "SZ": "SZSE",
            "BJ": "BJSE"
        }
        
        gm_market = market_map.get(prefix, "SHSE")
        return f"{gm_market}.{code}"

    @staticmethod
    def calc_change_percent(current: float, pre_close: float) -> float:
        """
        计算涨跌幅
        
        Args:
            current: 当前价格
            pre_close: 昨收价
            
        Returns:
            float: 涨跌幅（百分比），保留2位小数
        """
        if pre_close and pre_close != 0:
            return round((current - pre_close) / pre_close * 100, 2)
        return 0.0

    @staticmethod
    def calc_amplitude(high: float, low: float, pre_close: float) -> float:
        """
        计算振幅
        
        Args:
            high: 最高价
            low: 最低价
            pre_close: 昨收价
            
        Returns:
            float: 振幅（百分比），保留2位小数
        """
        if pre_close and pre_close != 0:
            return round((high - low) / pre_close * 100, 2)
        return 0.0

    @staticmethod
    def calc_amplitude_from_quote(quote: Dict[str, Any]) -> float:
        """
        从行情数据字典中计算振幅
        
        Args:
            quote: 行情数据字典，包含 high、low、pre_close 字段
            
        Returns:
            float: 振幅（百分比），保留2位小数
        """
        high = float(quote.get("high", 0))
        low = float(quote.get("low", 0))
        pre_close = float(quote.get("pre_close", 0))
        
        return StockUtils.calc_amplitude(high, low, pre_close)

    @staticmethod
    def format_price(price: Optional[float], decimals: int = 2) -> Optional[float]:
        """
        格式化价格，保留指定小数位数
        
        Args:
            price: 价格
            decimals: 小数位数，默认2位
            
        Returns:
            Optional[float]: 格式化后的价格
        """
        if price is None:
            return None
        return round(price, decimals)

    @staticmethod
    def format_percent(value: Optional[float], decimals: int = 2) -> Optional[float]:
        """
        格式化百分比，保留指定小数位数
        
        Args:
            value: 百分比值
            decimals: 小数位数，默认2位
            
        Returns:
            Optional[float]: 格式化后的百分比值
        """
        if value is None:
            return None
        return round(value, decimals)

    @staticmethod
    def format_volume(volume: Optional[float]) -> Optional[float]:
        """
        格式化成交量
        
        Args:
            volume: 成交量
            
        Returns:
            Optional[float]: 格式化后的成交量
        """
        if volume is None:
            return None
        return round(volume, 2)

    @staticmethod
    def format_amount(amount: Optional[float]) -> Optional[float]:
        """
        格式化成交额
        
        Args:
            amount: 成交额
            
        Returns:
            Optional[float]: 格式化后的成交额
        """
        if amount is None:
            return None
        return round(amount, 2)

    @staticmethod
    def format_market_cap(market_cap: Optional[float]) -> Optional[float]:
        """
        格式化市值（保留2位小数）
        
        Args:
            market_cap: 市值
            
        Returns:
            Optional[float]: 格式化后的市值
        """
        return StockUtils.format_price(market_cap, 2)

    