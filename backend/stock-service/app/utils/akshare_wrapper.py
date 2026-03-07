"""
AKShare接口封装工具模块

本模块提供了一系列工具函数和装饰器，用于封装和增强AKShare接口的调用。
主要功能包括：
1. 异常处理：统一捕获和处理AKShare接口调用过程中可能出现的异常
2. 结果转换：将AKShare返回的数据转换为标准格式
3. 缓存支持：为频繁调用的接口提供缓存功能，减少重复请求
4. 重试机制：对于可能因网络等原因失败的请求提供自动重试
"""

import functools
import logging
import time
from typing import Callable, Any, Optional, Dict, Union, List
import pandas as pd

logger = logging.getLogger(__name__)

def handle_akshare_exception(func: Callable) -> Callable:
    """
    处理AKShare接口异常的装饰器
    
    该装饰器会捕获AKShare接口调用过程中可能出现的所有异常，
    记录错误日志，并将异常转换为标准的ValueError异常抛出。
    
    Args:
        func (Callable): 需要处理异常的函数，通常是调用AKShare接口的函数
        
    Returns:
        Callable: 包装后的函数
        
    Raises:
        ValueError: 当原函数抛出任何异常时，将转换为ValueError并携带原异常信息
        
    Example:
        @handle_akshare_exception
        async def get_stock_info(stock_code: str):
            return ak.stock_individual_info_em(symbol=stock_code)
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"AKShare接口调用失败: {str(e)}")
            raise ValueError(f"数据获取失败: {str(e)}")
    return wrapper

def with_retry(max_retries: int = 3, retry_delay: float = 1.0) -> Callable:
    """
    为AKShare接口调用提供重试机制的装饰器
    
    当接口调用失败时，会自动重试指定次数，每次重试前等待指定的延迟时间。
    
    Args:
        max_retries (int, optional): 最大重试次数，默认为3次
        retry_delay (float, optional): 重试前的等待时间(秒)，默认为1秒
        
    Returns:
        Callable: 装饰器函数
        
    Example:
        @with_retry(max_retries=5, retry_delay=2.0)
        @handle_akshare_exception
        async def get_stock_quote(stock_code: str):
            return ak.stock_zh_a_spot_em()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait_time = retry_delay * (2 ** attempt)  # 指数退避策略
                        logger.warning(
                            f"AKShare接口调用失败，将在{wait_time:.2f}秒后进行第{attempt+1}次重试: {str(e)}"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"AKShare接口调用失败，已重试{max_retries}次: {str(e)}")
                        raise last_exception
            raise last_exception  # 这行代码理论上不会执行，但为了代码完整性添加
        return wrapper
    return decorator

def convert_to_dict_list(func: Callable) -> Callable:
    """
    将AKShare返回的DataFrame转换为字典列表的装饰器
    
    许多AKShare接口返回pandas DataFrame，该装饰器将其转换为字典列表，
    便于JSON序列化和API响应。
    
    Args:
        func (Callable): 返回pandas DataFrame的函数
        
    Returns:
        Callable: 包装后的函数，返回字典列表
        
    Example:
        @convert_to_dict_list
        @handle_akshare_exception
        async def get_stock_list():
            return ak.stock_zh_a_spot_em()
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> List[Dict]:
        result = await func(*args, **kwargs)
        if isinstance(result, pd.DataFrame):
            return result.to_dict(orient="records")
        return result
    return wrapper

def filter_dataframe(column: str, value: Any) -> Callable:
    """
    过滤AKShare返回的DataFrame的装饰器
    
    许多AKShare接口返回包含多条记录的DataFrame，该装饰器可以根据指定的列和值进行过滤，
    只返回符合条件的记录。
    
    Args:
        column (str): 用于过滤的列名
        value (Any): 用于过滤的值
        
    Returns:
        Callable: 装饰器函数
        
    Example:
        @filter_dataframe(column="代码", value="000001")
        @handle_akshare_exception
        async def get_specific_stock():
            return ak.stock_zh_a_spot_em()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> pd.DataFrame:
            df = await func(*args, **kwargs)
            if isinstance(df, pd.DataFrame) and column in df.columns:
                filtered_df = df[df[column] == value]
                if filtered_df.empty:
                    logger.warning(f"过滤后的DataFrame为空，列'{column}'中没有值'{value}'")
                return filtered_df
            return df
        return wrapper
    return decorator

# 可以根据需要继续添加更多实用工具函数...