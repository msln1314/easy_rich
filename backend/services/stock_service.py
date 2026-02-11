"""
股票数据服务 - 从akshare获取数据然后返回
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional

import akshare as ak
import pandas as pd


class StockService:
    """股票数据服务"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 字段描述映射
        self.field_descriptions = {
            # 基本信息字段
            "code": "股票代码",
            "name": "股票名称",
            "industry": "所属行业",
            "list_date": "上市日期",
            "market": "交易市场",
            "data_source": "数据来源",
            "update_time": "更新时间",

            # 基础价格字段
            "current_price": "最新价格(元)",
            "open": "开盘价(元)",
            "high": "最高价(元)",
            "low": "最低价(元)",
            "pre_close": "昨收价(元)",

            # 涨跌数据字段
            "change_amount": "涨跌金额(元)",
            "change_percent": "涨跌幅度(%)",

            # 涨跌停字段
            "limit_up": "涨停价(元)",
            "limit_down": "跌停价(元)",

            # 成交数据字段
            "volume": "成交量(手)",
            "turnover": "成交金额(元)",
            "avg_price": "均价(元)",

            # 盘口数据字段
            "outer_disc": "外盘成交量(手)",
            "inner_disc": "内盘成交量(手)",

            # 比率数据字段
            "turnover_rate": "换手率(%)",
            "volume_ratio": "量比",

            # 买盘字段
            "buy_1": "买一价(元)",
            "buy_1_vol": "买一量(手)",
            "buy_2": "买二价(元)",
            "buy_2_vol": "买二量(手)",
            "buy_3": "买三价(元)",
            "buy_3_vol": "买三量(手)",
            "buy_4": "买四价(元)",
            "buy_4_vol": "买四量(手)",
            "buy_5": "买五价(元)",
            "buy_5_vol": "买五量(手)",

            # 卖盘字段
            "sell_1": "卖一价(元)",
            "sell_1_vol": "卖一量(手)",
            "sell_2": "卖二价(元)",
            "sell_2_vol": "卖二量(手)",
            "sell_3": "卖三价(元)",
            "sell_3_vol": "卖三量(手)",
            "sell_4": "卖四价(元)",
            "sell_4_vol": "卖四量(手)",
            "sell_5": "卖五价(元)",
            "sell_5_vol": "卖五量(手)",

            # 历史数据字段
            "date": "交易日期",
            "close": "收盘价(元)",
            "amount": "成交额(元)"
        }

    async def get_stock_info(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """获取股票基本信息"""
        code = stock_code.replace('sz.', '').replace('sh.', '')
        
        # 获取基本信息
        print(f"获取股票{code}基本信息")
        info_df = await asyncio.to_thread(ak.stock_individual_info_em, symbol=code)
        print(f"获取股票{code}基本信息: {info_df}")
        info_dict = {}
        for _, row in info_df.iterrows():
            info_dict[row['item']] = row['value']
        
        # 获取行情报价
        quote_df = await asyncio.to_thread(ak.stock_bid_ask_em, symbol=code)
        print(f"获取股票{code}行情报价: {quote_df}")
        quote_data = {}
		
        if not quote_df.empty:
            # 将DataFrame转换为字典，方便查找
            quote_dict = {row['item']: row['value'] for _, row in quote_df.iterrows()}
            quote_data = self._format_quote_data(quote_dict)
        
        # 组装数据
        result = {
            "code": stock_code,
            "name": info_dict.get('股票简称', ''),
            "industry": info_dict.get('行业', ''),
            "list_date": info_dict.get('上市时间', ''),
            "market": self._get_market(stock_code),
            "data_source": "akshare",
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 添加行情数据
        result.update(quote_data)
        
        return {
            "data": result,
            "field_descriptions": self.field_descriptions
        }

    async def get_historical_data(self, stock_code: str, start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
        """获取历史数据"""
        code = stock_code.replace('sz.', '').replace('sh.', '')
        start_ak = start_date.replace('-', '')
        end_ak = end_date.replace('-', '')
        
        df = await asyncio.to_thread(
            ak.stock_zh_a_hist,
            symbol=code,
            period="daily",
            start_date=start_ak,
            end_date=end_ak,
            adjust=""
        )
        
        data_list = [self._format_historical_row(row) for _, row in df.iterrows()]
        
        return {
            "stock_code": stock_code,
            "data_count": len(data_list),
            "data": data_list,
            "field_descriptions": self.field_descriptions
        }

    async def check_connection(self) -> bool:
        """检查连接"""
        await asyncio.to_thread(ak.tool_trade_date_hist_sina)
        return True
    
    def get_field_descriptions(self) -> Dict[str, str]:
        """获取字段描述"""
        return self.field_descriptions
    
    def _safe_convert(self, value, convert_type, default=None):
        """安全类型转换"""
        if value is None or pd.isna(value):
            return default
        try:
            return convert_type(value)
        except (ValueError, TypeError):
            return default
    
    def _format_quote_data(self, quote_dict: Dict[str, Any]) -> Dict[str, Any]:
        """格式化行情数据"""
        # 定义字段映射和转换规则
        # 参考 akshare.stock_bid_ask_em 返回的实际字段
        print(quote_dict)
        field_mapping = {
            # 基础价格数据
            "current_price": ("最新", float, None),
            "open": ("今开", float, None),
            "high": ("最高", float, None),
            "low": ("最低", float, None),
            "pre_close": ("昨收", float, None),

            # 涨跌数据
            "change_amount": ("涨跌", float, None),
            "change_percent": ("涨幅", float, None),

            # 成交数据
            "volume": ("总手", int, None),
            "turnover": ("金额", float, None),
            "avg_price": ("均价", float, None),

            # 比率数据
            "turnover_rate": ("换手", float, None),
            "volume_ratio": ("量比", float, None),

            # 涨跌停
            "limit_up": ("涨停", float, None),
            "limit_down": ("跌停", float, None),

            # 盘口数据
            "outer_disc": ("外盘", int, None),
            "inner_disc": ("内盘", int, None),

            # 买卖档位
            "buy_1": ("买一", float, None),
            "buy_1_vol": ("买一量", int, None),
            "buy_2": ("买二", float, None),
            "buy_2_vol": ("买二量", int, None),
            "buy_3": ("买三", float, None),
            "buy_3_vol": ("买三量", int, None),
            "buy_4": ("买四", float, None),
            "buy_4_vol": ("买四量", int, None),
            "buy_5": ("买五", float, None),
            "buy_5_vol": ("买五量", int, None),

            "sell_1": ("卖一", float, None),
            "sell_1_vol": ("卖一量", int, None),
            "sell_2": ("卖二", float, None),
            "sell_2_vol": ("卖二量", int, None),
            "sell_3": ("卖三", float, None),
            "sell_3_vol": ("卖三量", int, None),
            "sell_4": ("卖四", float, None),
            "sell_4_vol": ("卖四量", int, None),
            "sell_5": ("卖五", float, None),
            "sell_5_vol": ("卖五量", int, None)
        }

        result = {}
        for field_name, (source_key, convert_type, default) in field_mapping.items():
            raw_value = quote_dict.get(source_key)
            result[field_name] = self._safe_convert(raw_value, convert_type, default)

        return result
    
    def _format_historical_row(self, row) -> Dict[str, Any]:
        """格式化历史数据行"""
        return {
            "date": row['日期'].strftime('%Y-%m-%d') if pd.notna(row['日期']) else '',
            "open": self._safe_convert(row['开盘'], float, 0.0),
            "high": self._safe_convert(row['最高'], float, 0.0),
            "low": self._safe_convert(row['最低'], float, 0.0),
            "close": self._safe_convert(row['收盘'], float, 0.0),
            "volume": self._safe_convert(row['成交量'], int, 0),
            "amount": self._safe_convert(row['成交额'], float, 0.0),
"data_source": "akshare"
        }



    def _get_market(self, stock_code: str) -> str:
        """判断市场"""
        if stock_code.startswith('sz.'):
            return "sz"
        elif stock_code.startswith('sh.'):
            return "sh"
        elif stock_code.startswith('bj.'):
            return "bj"
        elif stock_code.startswith(('00', '30')):
            return "sz"
        elif stock_code.startswith(('60', '68')):
            return "sh"
        elif stock_code.startswith(('43', '83', '87', '88','920')):
            return "bj"
        
        return "unknow"