# backend/qmt-service/app/main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.qmt_client import QMTClientManager

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info(f"正在启动 {settings.PROJECT_NAME}...")

    # 初始化因子库（仅内存缓存，不使用数据库）
    from app.services.factor_service import factor_service
    await factor_service.init_factors()
    logger.info(f"因子库加载完成，共 {len(factor_service._factor_cache)} 个因子")

    # 连接QMT
    connected = await QMTClientManager.initialize()
    if connected:
        logger.info("QMT客户端连接成功")
    else:
        logger.warning("QMT客户端未连接，使用模拟模式")

    yield

    # 关闭时
    logger.info("正在关闭服务...")
    await QMTClientManager.close()
    logger.info("服务已关闭")


# API tags
tags_metadata = [
    {"name": "trade", "description": "交易执行接口"},
    {"name": "position", "description": "持仓管理接口"},
]

# 创建应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="QMT量化交易服务，提供交易执行、持仓管理等功能",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["root"])
async def root():
    """根路径"""
    return {
        "message": settings.PROJECT_NAME,
        "docs": "/docs",
        "qmt_status": "connected" if QMTClientManager.is_connected() else "mock"
    }


@app.get("/health", tags=["root"])
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "qmt": QMTClientManager.get_status()
    }