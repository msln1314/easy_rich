# backend/qmt-service/app/core/qmt_client.py
"""
QMT客户端连接管理器

注意：xtquant SDK需要在Windows环境下运行，且需要先启动QMT客户端
"""
import logging
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class QMTClientManager:
    """QMT客户端连接管理器"""

    _trader = None
    _account = None
    _connected: bool = False
    _session_id: int = 0

    @classmethod
    async def initialize(cls) -> bool:
        """初始化QMT连接"""
        if cls._connected:
            logger.info("QMT已连接，跳过初始化")
            return True

        try:
            # 检查配置
            if not settings.QMT_CLIENT_PATH:
                logger.warning("QMT客户端路径未配置，使用模拟模式")
                return False

            if not settings.QMT_ACCOUNT or not settings.QMT_PASSWORD:
                logger.warning("QMT账号或密码未配置，使用模拟模式")
                return False

            # 尝试导入xtquant
            try:
                from xtquant.xttrader import XtQuantTrader, XtAccount
            except ImportError as e:
                logger.error(f"xtquant SDK未安装: {e}")
                logger.info("请运行: pip install xtquant")
                return False

            # 创建交易对象
            cls._session_id = settings.QMT_SESSION_ID
            cls._trader = XtQuantTrader(
                settings.QMT_CLIENT_PATH,
                cls._session_id
            )

            # 创建账号对象
            cls._account = XtAccount(
                settings.QMT_ACCOUNT,
                settings.QMT_PASSWORD
            )

            # 连接QMT
            cls._trader.connect()
            cls._connected = True

            logger.info(f"QMT连接成功，会话ID: {cls._session_id}")
            return True

        except Exception as e:
            logger.error(f"QMT连接失败: {e}")
            cls._connected = False
            return False

    @classmethod
    async def close(cls):
        """关闭QMT连接"""
        if cls._trader and cls._connected:
            try:
                cls._trader.disconnect()
                logger.info("QMT连接已关闭")
            except Exception as e:
                logger.error(f"关闭QMT连接失败: {e}")
            finally:
                cls._connected = False
                cls._trader = None
                cls._account = None

    @classmethod
    def get_trader(cls):
        """获取交易对象"""
        if not cls._connected:
            raise RuntimeError("QMT未连接，请先调用initialize()")
        return cls._trader

    @classmethod
    def get_account(cls):
        """获取账号对象"""
        if not cls._connected:
            raise RuntimeError("QMT未连接，请先调用initialize()")
        return cls._account

    @classmethod
    def is_connected(cls) -> bool:
        """检查连接状态"""
        return cls._connected

    @classmethod
    def get_status(cls) -> dict:
        """获取连接状态详情"""
        return {
            "connected": cls._connected,
            "session_id": cls._session_id,
            "account": settings.QMT_ACCOUNT if cls._connected else None,
            "client_path": settings.QMT_CLIENT_PATH if cls._connected else None,
        }