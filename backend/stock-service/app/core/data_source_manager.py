# -*- coding: utf-8 -*-
# @version        : 1.1
# @Create Time    : 2026/3/16
# @File           : data_source_manager.py
# @IDE            : PyCharm
# @desc           : 数据源管理器 - 统一管理多数据源优先级和降级策略

"""
数据源优先级管理器

优先级顺序（成功率从高到低）：
1. AKShare - 主数据源，覆盖最全
2. 腾讯财经 - 成功率高，响应快，实时行情首选备用
3. pytdx - 通达信接口，实时行情备用
4. 新浪财经 - HTTP接口，行情备用
5. GM (掘金量化) - 需要Token
6. Tushare Pro - 需要Token

使用方式：
    from app.core.data_source_manager import DataSourceManager, DataSource

    manager = DataSourceManager()

    # 执行数据获取，自动降级
    result = await manager.execute_with_fallback(
        data_type="stock_quote",
        sources=[
            (DataSource.AKSHARE, lambda: ak.stock_zh_a_spot_em()),
            (DataSource.TENCENT, lambda: tencent_source.get_quote(code)),
            (DataSource.PYTDX, lambda: pytdx_source.get_stock_quote(code)),
        ]
    )
"""

import asyncio
import functools
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class DataSource(str, Enum):
    """数据源枚举"""

    AKSHARE = "akshare"
    TENCENT = "tencent"  # 腾讯财经 - 成功率高
    PYTDX = "pytdx"
    SINA = "sina"
    GM = "gm"  # 掘金量化
    TUSHARE = "tushare"
    EASTMONEY = "eastmoney"

    def __str__(self):
        return self.value


@dataclass
class DataSourceResult:
    """数据源返回结果"""

    success: bool
    data: Any = None
    source: Optional[DataSource] = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DataSourceConfig:
    """数据源配置"""

    enabled: bool = True
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    priority: int = 0  # 数字越小优先级越高

    # 特定配置
    token: Optional[str] = None  # GM/Tushare需要
    host: Optional[str] = None  # pytdx需要
    port: Optional[int] = None  # pytdx需要


class DataSourceManager:
    """
    数据源管理器

    统一管理多数据源的优先级、降级策略和错误处理
    """

    # 默认数据源配置 - 腾讯财经优先级提高
    DEFAULT_CONFIGS: Dict[DataSource, DataSourceConfig] = {
        DataSource.AKSHARE: DataSourceConfig(enabled=True, priority=1, timeout=60.0),
        DataSource.TENCENT: DataSourceConfig(
            enabled=True, priority=2, timeout=5.0
        ),  # 腾讯财经，成功率高
        DataSource.PYTDX: DataSourceConfig(enabled=True, priority=3, timeout=10.0),
        DataSource.SINA: DataSourceConfig(enabled=True, priority=4, timeout=10.0),
        DataSource.GM: DataSourceConfig(enabled=True, priority=5, timeout=30.0),
        DataSource.TUSHARE: DataSourceConfig(enabled=True, priority=6, timeout=60.0),
    }

    # 数据类型到推荐数据源的映射 - 腾讯财经加入
    DATA_TYPE_SOURCES: Dict[str, List[DataSource]] = {
        # 股票行情 - 腾讯财经优先
        "stock_quote": [
            DataSource.AKSHARE,
            DataSource.TENCENT,  # 腾讯财经，成功率高
            DataSource.PYTDX,
            DataSource.SINA,
            DataSource.GM,
        ],
        "stock_history": [DataSource.AKSHARE, DataSource.PYTDX, DataSource.GM],
        "stock_list": [DataSource.AKSHARE, DataSource.TENCENT, DataSource.PYTDX],
        # 指数数据 - 腾讯财经优先
        "index_quote": [
            DataSource.AKSHARE,
            DataSource.TENCENT,  # 腾讯财经
            DataSource.SINA,
            DataSource.PYTDX,
        ],
        "index_history": [DataSource.AKSHARE, DataSource.GM],
        # 板块数据
        "concept_board": [DataSource.AKSHARE, DataSource.TUSHARE],
        "industry_board": [DataSource.AKSHARE, DataSource.TUSHARE],
        "board_constituents": [DataSource.AKSHARE, DataSource.GM],
        # 市场数据
        "market_summary": [DataSource.AKSHARE, DataSource.PYTDX],
        "zt_pool": [DataSource.AKSHARE, DataSource.PYTDX],
        "fund_flow": [DataSource.AKSHARE],
        # 财务数据
        "financial": [DataSource.AKSHARE, DataSource.TUSHARE],
        "margin": [DataSource.AKSHARE],
        # 新闻资讯
        "news": [DataSource.AKSHARE],
        # 龙虎榜
        "lhb": [DataSource.AKSHARE],
        # 机构数据
        "institution_research": [DataSource.AKSHARE],
        "fund_holding": [DataSource.AKSHARE],
    }

    def __init__(self, configs: Optional[Dict[DataSource, DataSourceConfig]] = None):
        """
        初始化数据源管理器

        Args:
            configs: 自定义数据源配置，会覆盖默认配置
        """
        self.configs = {**self.DEFAULT_CONFIGS, **(configs or {})}
        self._source_status: Dict[DataSource, Dict[str, Any]] = {
            source: {
                "available": True,
                "last_success": None,
                "last_failure": None,
                "failure_count": 0,
            }
            for source in DataSource
        }

    def get_config(self, source: DataSource) -> DataSourceConfig:
        """获取数据源配置"""
        return self.configs.get(source, DataSourceConfig())

    def is_source_available(self, source: DataSource) -> bool:
        """检查数据源是否可用"""
        config = self.get_config(source)
        if not config.enabled:
            return False

        status = self._source_status.get(source, {})

        # 如果连续失败超过阈值，暂时标记为不可用
        if status.get("failure_count", 0) >= 5:
            # 检查上次失败时间，超过5分钟则重试
            last_failure = status.get("last_failure")
            if last_failure:
                elapsed = (datetime.now() - last_failure).total_seconds()
                if elapsed < 300:  # 5分钟内不重试
                    return False
                else:
                    # 重置失败计数
                    status["failure_count"] = 0

        return status.get("available", True)

    def mark_success(self, source: DataSource):
        """标记数据源成功"""
        self._source_status[source]["last_success"] = datetime.now()
        self._source_status[source]["failure_count"] = 0

    def mark_failure(self, source: DataSource, error: str):
        """标记数据源失败"""
        self._source_status[source]["last_failure"] = datetime.now()
        self._source_status[source]["failure_count"] += 1
        logger.warning(f"数据源 {source} 失败: {error}")

    async def execute_with_fallback(
        self,
        sources: List[Tuple[DataSource, Callable]],
        data_type: Optional[str] = None,
    ) -> DataSourceResult:
        """
        按优先级执行数据获取，失败时自动降级

        Args:
            sources: 数据源列表，格式为 [(数据源, 获取函数), ...]
            data_type: 数据类型，用于日志记录

        Returns:
            DataSourceResult: 包含数据和来源的结果对象
        """
        last_error = None

        for source, fetch_func in sources:
            # 检查数据源是否可用
            if not self.is_source_available(source):
                logger.debug(f"数据源 {source} 不可用，跳过")
                continue

            config = self.get_config(source)
            start_time = datetime.now()

            try:
                # 执行获取函数
                if asyncio.iscoroutinefunction(fetch_func):
                    data = await asyncio.wait_for(fetch_func(), timeout=config.timeout)
                else:
                    # 同步函数在执行器中运行
                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, fetch_func)

                # 检查返回数据是否有效
                if data is None:
                    raise ValueError("返回数据为空")

                if hasattr(data, "empty") and data.empty:
                    raise ValueError("返回数据为空DataFrame")

                latency = (datetime.now() - start_time).total_seconds() * 1000
                self.mark_success(source)

                logger.info(
                    f"数据源 {source} 获取 {data_type or '数据'} 成功, "
                    f"耗时: {latency:.2f}ms"
                )

                return DataSourceResult(
                    success=True, data=data, source=source, latency_ms=latency
                )

            except asyncio.TimeoutError:
                error = f"数据源 {source} 超时 ({config.timeout}s)"
                logger.warning(error)
                last_error = error
                self.mark_failure(source, error)

            except Exception as e:
                error = f"数据源 {source} 失败: {str(e)}"
                logger.warning(error)
                last_error = error
                self.mark_failure(source, str(e))

        # 所有数据源都失败
        error_msg = f"所有数据源均无法获取 {data_type or '数据'}"
        if last_error:
            error_msg += f", 最后错误: {last_error}"

        logger.error(error_msg)

        return DataSourceResult(success=False, error=error_msg)

    def get_recommended_sources(self, data_type: str) -> List[DataSource]:
        """
        获取指定数据类型的推荐数据源列表

        Args:
            data_type: 数据类型

        Returns:
            List[DataSource]: 推荐的数据源列表（按优先级排序）
        """
        return self.DATA_TYPE_SOURCES.get(data_type, [DataSource.AKSHARE])

    def get_source_status(self) -> Dict[DataSource, Dict[str, Any]]:
        """获取所有数据源状态"""
        return self._source_status.copy()


# 装饰器：自动降级
def with_fallback(data_type: str, sources: Optional[List[DataSource]] = None):
    """
    装饰器：为函数添加自动降级功能

    使用示例:
        @with_fallback("stock_quote", [DataSource.AKSHARE, DataSource.PYTDX])
        async def get_stock_quote(code: str):
            return ak.stock_zh_a_spot_em()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            manager = DataSourceManager()

            # 如果没有指定数据源，使用默认推荐
            source_list = sources or manager.get_recommended_sources(data_type)

            # 构建数据源调用列表
            fetch_funcs = []
            for source in source_list:
                # 这里需要根据实际的数据源实现来构建调用函数
                fetch_funcs.append((source, lambda: func(*args, **kwargs)))

            result = await manager.execute_with_fallback(fetch_funcs, data_type)

            if result.success:
                return result.data
            else:
                raise ValueError(result.error)

        return wrapper

    return decorator


# 创建全局实例
data_source_manager = DataSourceManager()
