# backend/qmt-service/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """QMT服务配置"""

    # 服务配置
    PROJECT_NAME: str = "QMT量化交易服务"
    API_V1_STR: str = "/api/v1"
    SERVICE_PORT: int = 8009
    SERVICE_HOST: str = "0.0.0.0"
    DEBUG: bool = False

    # CORS设置
    ORIGINS: list = ["*"]

    # QMT客户端配置
    QMT_CLIENT_PATH: str = ""  # QMT客户端路径，如: C:\迅投QMT交易端\userdata_mini
    QMT_ACCOUNT: str = ""      # QMT账号
    QMT_PASSWORD: str = ""     # QMT密码
    QMT_SESSION_ID: int = 123456  # 会话ID，任意整数

    # MySQL数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "1qaz2wsx"
    DB_NAME: str = "qmt_factor"

    # Redis配置（共享stock-service）
    REDIS_ENABLED: bool = True
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_PREFIX: str = "qmt:"

    # 日志配置
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()