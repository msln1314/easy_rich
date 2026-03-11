# 先导入 akshare-proxy-patch 来修复网络问题 (已禁用)
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
from app.models.technical_models import ChipDistribution
from app.utils.akshare_wrapper import handle_akshare_exception
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)

class TechnicalService:
    """技术指标服务"""
    
    # ... 保留现有的方法 ...
    
    @cache_result()
    @handle_akshare_exception
    async def get_chip_distribution(self, symbol: str, adjust: str = "") -> List[ChipDistribution]:
        """
        获取股票筹码分布数据
        
        Args:
            symbol: 股票代码，如"000001"
            adjust: 复权类型，可选值为"qfq"(前复权)、"hfq"(后复权)、""(不复权)，默认为不复权
            
        Returns:
            List[ChipDistribution]: 筹码分布数据列表
        """
        logger.info(f"获取股票筹码分布数据: {symbol}, 复权类型: {adjust}")
        
        # 标准化股票代码（去掉市场前缀）
        if symbol.startswith(("sh", "sz", "bj")):
            symbol = symbol[2:]
        
        try:
            # 调用AKShare接口获取筹码分布数据
            df = ak.stock_cyq_em(symbol=symbol, adjust=adjust)
            
            if df.empty:
                logger.warning(f"未获取到股票 {symbol} 的筹码分布数据")
                return []
            
            # 将DataFrame转换为ChipDistribution对象列表
            result = []
            for _, row in df.iterrows():
                # 确保日期是字符串类型
                if isinstance(row["日期"], (datetime, pd.Timestamp, pd.DatetimeIndex, date)):
                    trade_date_str = row["日期"].strftime("%Y-%m-%d")
                else:
                    trade_date_str = str(row["日期"])
                
                chip = ChipDistribution(
                    trade_date=trade_date_str,  # 使用转换后的字符串
                    stock_code=symbol,
                    profit_ratio=float(row["获利比例"]),
                    avg_cost=float(row["平均成本"]),
                    cost_90_low=float(row["90成本-低"]),
                    cost_90_high=float(row["90成本-高"]),
                    concentration_90=float(row["90集中度"]),
                    cost_70_low=float(row["70成本-低"]),
                    cost_70_high=float(row["70成本-高"]),
                    concentration_70=float(row["70集中度"]),
                    update_time=datetime.now()
                )
                result.append(chip)
            
            return result
        except Exception as e:
            logger.error(f"获取股票筹码分布数据失败: {str(e)}")
            raise ValueError(f"获取股票筹码分布数据失败: {str(e)}")