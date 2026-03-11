# 先导入 akshare-proxy-patch 来修复网络问题
# try:
#     from app.utils.akshare_proxy_patch import install_patch
#     install_patch("127.0.0.1", "", 60)  # auth_token 为空时不使用代理
# except ImportError as e:
#     print(f"警告：无法导入 akshare 代理补丁: {e}")
#     pass

import akshare as ak
import pandas as pd
from datetime import datetime, date
from typing import List, Optional
from app.models.sentiment_models import MarginDetail, StockHotRank, StockHotUpRank, StockHotKeyword
from app.utils.akshare_wrapper import handle_akshare_exception
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)

class SentimentService:
    """市场情绪服务"""
    
    @cache_result()
    @handle_akshare_exception
    async def get_margin_details(self, trade_date: str) -> List[MarginDetail]:
        """
        获取融资融券明细数据（上海和深圳市场合并）
        
        Args:
            trade_date: 交易日期，格式为"YYYYMMDD"，如"20230922"
            
        Returns:
            List[MarginDetail]: 融资融券明细数据列表
        """
        logger.info(f"获取融资融券明细数据: {trade_date}")
        
        result = []
        
        # 获取上海市场数据
        try:
            sh_df = ak.stock_margin_detail_sse(date=trade_date)
            if not sh_df.empty:
                # 转换日期格式
                date_obj = datetime.strptime(trade_date, "%Y%m%d").date()
                
                # 处理上海市场数据
                for _, row in sh_df.iterrows():
                    detail = MarginDetail(
                        trade_date=date_obj,
                        stock_code=row["标的证券代码"],
                        stock_name=row["标的证券简称"],
                        market="上海",
                        financing_buy=int(row["融资买入额"]),
                        financing_balance=int(row["融资余额"]),
                        financing_repay=int(row["融资偿还额"]),
                        securities_sell=int(row["融券卖出量"]),
                        securities_balance=int(row["融券余量"]),
                        securities_repay=int(row["融券偿还量"]),
                        securities_balance_amount=None,  # 上海数据没有融券余额
                        margin_balance=None,  # 上海数据没有融资融券余额
                        update_time=datetime.now()
                    )
                    result.append(detail)
                logger.info(f"获取到上海市场融资融券明细数据: {len(result)}条")
            else:
                logger.warning(f"未获取到上海市场 {trade_date} 的融资融券明细数据")
        except Exception as e:
            logger.error(f"获取上海市场融资融券明细数据失败: {str(e)}")
        
        # 获取深圳市场数据
        try:
            sz_df = ak.stock_margin_detail_szse(date=trade_date)
            if not sz_df.empty:
                # 转换日期格式
                date_obj = datetime.strptime(trade_date, "%Y%m%d").date()
                
                # 处理深圳市场数据
                for _, row in sz_df.iterrows():
                    detail = MarginDetail(
                        trade_date=date_obj,
                        stock_code=row["证券代码"],
                        stock_name=row["证券简称"],
                        market="深圳",
                        financing_buy=int(row["融资买入额"]),
                        financing_balance=int(row["融资余额"]),
                        financing_repay=None,  # 深圳数据没有融资偿还额
                        securities_sell=int(row["融券卖出量"]),
                        securities_balance=int(row["融券余量"]),
                        securities_repay=None,  # 深圳数据没有融券偿还量
                        securities_balance_amount=int(row["融券余额"]),
                        margin_balance=int(row["融资融券余额"]),
                        update_time=datetime.now()
                    )
                    result.append(detail)
                logger.info(f"获取到深圳市场融资融券明细数据: {len(result) - len(sh_df)}条")
            else:
                logger.warning(f"未获取到深圳市场 {trade_date} 的融资融券明细数据")
        except Exception as e:
            logger.error(f"获取深圳市场融资融券明细数据失败: {str(e)}")
        
        return result
    
    @cache_result()
    @handle_akshare_exception
    async def get_stock_hot_rank(self) -> List[StockHotRank]:
        """
        获取股票热度排名数据
        
        Returns:
            List[StockHotRank]: 股票热度排名数据列表
        """
        logger.info("获取股票热度排名数据")
        
        # 调用AKShare接口获取股票热度排名数据
        df = ak.stock_hot_rank_em()
        
        if df.empty:
            logger.warning("未获取到股票热度排名数据")
            return []
        
        # 将DataFrame转换为StockHotRank对象列表
        result = []
        for _, row in df.iterrows():
            # 处理股票代码，确保格式一致
            stock_code = row["代码"]
            if stock_code.startswith(("SH", "SZ", "BJ")):
                stock_code = stock_code[2:]
            
            hot_rank = StockHotRank(
                rank=int(row["当前排名"]),
                stock_code=stock_code,
                stock_name=row["股票名称"],
                price=float(row["最新价"]),
                change=float(row["涨跌额"]),
                change_percent=float(row["涨跌幅"]),
                update_time=datetime.now()
            )
            result.append(hot_rank)
        
        return result
    
    @cache_result()
    @handle_akshare_exception
    async def get_stock_hot_up_rank(self) -> List[StockHotUpRank]:
        """
        获取股票飙升榜数据
        
        Returns:
            List[StockHotUpRank]: 股票飙升榜数据列表
        """
        # 方法实现保持不变
        logger.info("获取股票飙升榜数据")
        
        # 调用AKShare接口获取股票飙升榜数据
        df = ak.stock_hot_up_em()
        
        if df.empty:
            logger.warning("未获取到股票飙升榜数据")
            return []
        
        # 将DataFrame转换为StockHotUpRank对象列表
        result = []
        for _, row in df.iterrows():
            # 处理股票代码，确保格式一致
            stock_code = row["代码"]
            if stock_code.startswith(("SH", "SZ", "BJ")):
                stock_code = stock_code[2:]
            
            hot_up_rank = StockHotUpRank(
                rank_change=int(row["排名较昨日变动"]),
                rank=int(row["当前排名"]),
                stock_code=stock_code,
                stock_name=row["股票名称"],
                price=float(row["最新价"]),
                change=float(row["涨跌额"]),
                change_percent=float(row["涨跌幅"]),
                update_time=datetime.now()
            )
            result.append(hot_up_rank)
        
        return result
    
    @cache_result()
    @handle_akshare_exception
    async def get_stock_hot_keywords(self, symbol: str) -> List[StockHotKeyword]:
        """
        获取股票热门关键词数据
        
        Args:
            symbol: 股票代码，如"SZ000665"
            
        Returns:
            List[StockHotKeyword]: 股票热门关键词数据列表
        """
        logger.info(f"获取股票热门关键词数据: {symbol}")
        
        # 标准化股票代码（确保大写）
        if symbol.startswith(("sh", "sz", "bj")):
            market = symbol[:2].upper()
            code = symbol[2:]
            symbol = f"{market}{code}"
        
        # 调用AKShare接口获取股票热门关键词数据
        df = ak.stock_hot_keyword_em(symbol=symbol)
        
        if df.empty:
            logger.warning(f"未获取到股票 {symbol} 的热门关键词数据")
            return []
        
        # 将DataFrame转换为StockHotKeyword对象列表
        result = []
        for _, row in df.iterrows():
            # 转换时间格式
            time_obj = datetime.strptime(row["时间"], "%Y-%m-%d %H:%M:%S")
            
            # 处理股票代码，确保格式一致
            stock_code = row["股票代码"]
            if stock_code.startswith(("SH", "SZ", "BJ")):
                stock_code = stock_code[2:]
            
            keyword = StockHotKeyword(
                time=time_obj,
                stock_code=stock_code,
                concept_name=row["概念名称"],
                concept_code=row["概念代码"],
                heat=int(row["热度"]),
                update_time=datetime.now()
            )
            result.append(keyword)
        
        return result