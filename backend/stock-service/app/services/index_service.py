# 先导入 akshare-proxy-patch 来修复网络问题
# try:
#     import akshare_proxy_patch
#     akshare_proxy_patch.install_patch("101.201.173.125", "", 60)
# except ImportError:
#     pass

import akshare as ak
import pandas as pd  # 添加 pandas 导入
from datetime import datetime
from typing import List, Optional
from app.models.index_models import IndexQuote
from app.utils.akshare_wrapper import handle_akshare_exception
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)

class IndexService:
    @cache_result()
    @handle_akshare_exception
    async def get_index_quotes(self, symbol: str = "沪深重要指数") -> List[IndexQuote]:
        """
        获取指数实时行情数据
        
        Args:
            symbol: 指数类型，可选值：
                   "沪深重要指数", "上证系列指数", "深证系列指数", "指数成份", "中证系列指数"
                   
        Returns:
            List[IndexQuote]: 指数实时行情数据列表
        """
        logger.info(f"获取指数实时行情: {symbol}")
        
        # 验证参数
        valid_symbols = ["沪深重要指数", "上证系列指数", "深证系列指数", "指数成份", "中证系列指数"]
        if symbol not in valid_symbols:
            logger.error(f"不支持的指数类型: {symbol}")
            raise ValueError(f"不支持的指数类型: {symbol}，支持的类型为: {', '.join(valid_symbols)}")
        
        # 调用AKShare接口获取指数实时行情
        df = ak.stock_zh_index_spot_em(symbol=symbol)
        
        if df.empty:
            logger.warning(f"未找到指数类型 {symbol} 的实时行情数据")
            return []
        
        # 将DataFrame转换为IndexQuote对象列表
        result = []
        for _, row in df.iterrows():
            # 处理可能的NaN值
            high = float(row["最高"]) if not pd.isna(row["最高"]) else None
            low = float(row["最低"]) if not pd.isna(row["最低"]) else None
            open_price = float(row["今开"]) if not pd.isna(row["今开"]) else None
            pre_close = float(row["昨收"]) if not pd.isna(row["昨收"]) else None
            volume_ratio = float(row["量比"]) if not pd.isna(row["量比"]) else None
            
            quote = IndexQuote(
                code=row["代码"],
                name=row["名称"],
                price=float(row["最新价"]),
                change=float(row["涨跌额"]),
                change_percent=float(row["涨跌幅"]),
                volume=float(row["成交量"]) if not pd.isna(row["成交量"]) else None,
                amount=float(row["成交额"]) if not pd.isna(row["成交额"]) else None,
                amplitude=float(row["振幅"]) if not pd.isna(row["振幅"]) else None,
                high=high,
                low=low,
                open=open_price,
                pre_close=pre_close,
                volume_ratio=volume_ratio,
                update_time=datetime.now()
            )
            result.append(quote)
        
        return result
    
    @cache_result()
    @handle_akshare_exception
    async def get_index_quote(self, index_code: str) -> Optional[IndexQuote]:
        """
        获取单个指数的实时行情数据
        
        Args:
            index_code: 指数代码，如"000001"（上证指数）
            
        Returns:
            Optional[IndexQuote]: 指数实时行情数据，如果未找到则返回None
        """
        logger.info(f"获取单个指数实时行情: {index_code}")
        
        # 尝试从不同的指数类型中查找
        index_types = ["沪深重要指数", "上证系列指数", "深证系列指数", "指数成份", "中证系列指数"]
        
        for index_type in index_types:
            try:
                # 获取该类型下的所有指数
                all_indices = await self.get_index_quotes(index_type)
                
                # 查找匹配的指数
                for index in all_indices:
                    if index.code == index_code:
                        return index
            except Exception as e:
                logger.warning(f"从 {index_type} 中查找指数 {index_code} 失败: {str(e)}")
                continue
        
        logger.warning(f"未找到指数代码 {index_code} 的实时行情数据")
        return None