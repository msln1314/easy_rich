import functools
import json
import redis
from typing import Any, Callable, Optional
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# 创建Redis连接
redis_client = None
if settings.REDIS_ENABLED:
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            socket_timeout=settings.REDIS_TIMEOUT
        )
        # 测试连接
        redis_client.ping()
        logger.info("Redis缓存已连接")
    except Exception as e:
        logger.warning(f"Redis连接失败，将禁用缓存: {str(e)}")
        redis_client = None

def cache_result(expire: int = None):
    """
    缓存函数结果的装饰器
    
    Args:
        expire: 缓存过期时间(秒)，默认使用配置中的REDIS_CACHE_EXPIRATION
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # 如果Redis未启用或连接失败，直接执行函数
            if not settings.REDIS_ENABLED or redis_client is None:
                return await func(*args, **kwargs)
            
            # 生成缓存键
            cache_key = _generate_cache_key(func.__name__, args, kwargs)
            
            # 尝试从缓存获取
            try:
                cached_data = redis_client.get(cache_key)
                if cached_data:
                    logger.debug(f"从缓存获取数据: {cache_key}")
                    return json.loads(cached_data)
            except Exception as e:
                logger.warning(f"从缓存获取数据失败: {str(e)}")
            
            # 执行原函数
            result = await func(*args, **kwargs)
            
            # 存入缓存
            try:
                expiration = expire or settings.REDIS_CACHE_EXPIRATION
                redis_client.setex(
                    cache_key,
                    expiration,
                    json.dumps(result, ensure_ascii=False)
                )
                logger.debug(f"数据已存入缓存: {cache_key}, 过期时间: {expiration}秒")
            except Exception as e:
                logger.warning(f"存入缓存失败: {str(e)}")
            
            return result
        return wrapper
    return decorator

def _generate_cache_key(func_name: str, args: tuple, kwargs: dict) -> str:
    """生成缓存键"""
    # 将参数转换为字符串
    args_str = '_'.join([str(arg) for arg in args])
    kwargs_str = '_'.join([f"{k}:{v}" for k, v in sorted(kwargs.items())])
    
    # 组合缓存键
    key_parts = [settings.REDIS_PREFIX, func_name]
    if args_str:
        key_parts.append(args_str)
    if kwargs_str:
        key_parts.append(kwargs_str)
    
    return ':'.join(key_parts)

def clear_cache(pattern: str = None):
    """
    清除缓存
    
    Args:
        pattern: 缓存键模式，如果为None则清除所有以REDIS_PREFIX开头的缓存
    """
    if not settings.REDIS_ENABLED or redis_client is None:
        return
    
    try:
        if pattern is None:
            pattern = f"{settings.REDIS_PREFIX}*"
        
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
            logger.info(f"已清除{len(keys)}个缓存项: {pattern}")
    except Exception as e:
        logger.error(f"清除缓存失败: {str(e)}")