import os
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings


def load_akshare_patch():
    from app.core.config import settings
    from app.utils.akshare_proxy_patch import (
        install_patch_default,
        install_patch_with_pool,
        install_patch_with_redis_pool,
        install_patch_auto,
        fetch_eastmoney_cookie,
        is_patch_disabled,
    )

    patch_mode = settings.AKSHARE_PATCH_MODE
    auth_token = settings.AKSHARE_AUTH_TOKEN
    proxy_pool_url = settings.AKSHARE_PROXY_POOL_URL

    print(f"[Stock Service] AKShare 补丁模式: {patch_mode}")

    if patch_mode == "direct":
        print("[Stock Service] AKShare 补丁：直连模式")
        install_patch_auto(timeout=30, min_interval=0.2)
        return

    # Try cloud auth first (for auto and cloud modes)
    if patch_mode in ("cloud", "auto"):
        # Check if cloud auth is disabled in Redis
        if is_patch_disabled():
            print("[Stock Service] 云端授权已被禁用 (积分用完)，跳过云端授权")
        else:
            try:
                print("[Stock Service] 尝试云端授权...")
                install_patch_default(
                    auth_token=auth_token, timeout=10, min_interval=0.2
                )
                print("[Stock Service] 云端授权成功")
                return
            except Exception as e:
                error_msg = str(e)
                if "积分" in error_msg or "用完" in error_msg:
                    print(f"[Stock Service] 云端积分用完: {error_msg[:50]}")
                else:
                    print(f"[Stock Service] 云端授权失败: {error_msg[:50]}")

            if patch_mode == "cloud":
                print("[Stock Service] 切换直连模式")
                install_patch_auto(timeout=30, min_interval=0.2)
                return

    # Try proxy pool with Redis caching
    if patch_mode in ("proxy_pool", "auto"):
        print(f"[Stock Service] 初始化代理池...")
        try:
            from app.services.proxy_pool_manager import (
                get_proxy_pool_manager,
                init_proxy_pool,
            )

            manager = get_proxy_pool_manager()
            status = manager.get_pool_status()

            if status["available"] < status["min_proxies"]:
                print(
                    f"[Stock Service] 代理池代理不足({status['available']}<{status['min_proxies']})，正在获取..."
                )
                count = init_proxy_pool(validate=False)
                if count == 0:
                    print("[Stock Service] 无法获取代理，使用直连模式")
                    install_patch_auto(timeout=30, min_interval=0.2)
                    return
            else:
                print(f"[Stock Service] 代理池已有 {status['available']} 个可用代理")

            # Install patch with Redis-backed proxy pool
            install_patch_with_redis_pool(timeout=30, min_interval=0.2)
            print("[Stock Service] Redis代理池模式已启用")
            return

        except Exception as e:
            print(f"[Stock Service] 代理池初始化失败: {e}")

    # Fallback to direct mode
    print("[Stock Service] 使用直连模式")
    install_patch_auto(timeout=30, min_interval=0.2)


# Load patch before creating app
load_akshare_patch()

# API tags
tags_metadata = [
    {"name": "stock", "description": "股票相关接口"},
    {"name": "index", "description": "大盘指数接口"},
    {"name": "sector", "description": "板块相关接口"},
    {"name": "sentiment", "description": "市场情绪接口"},
    {"name": "technical", "description": "技术分析接口"},
    {"name": "news", "description": "新闻资讯接口"},
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="基于 AKShare 数据的股票分析服务",
    version="2.3.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata,
    openapi_version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["root"])
async def root():
    return {"message": "股票分析服务 API", "docs": "/docs"}


@app.get("/health", tags=["root"])
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}


@app.get("/proxy-pool/status", tags=["root"])
async def proxy_pool_status():
    """Get proxy pool status"""
    try:
        from app.services.proxy_pool_manager import get_proxy_pool_manager

        manager = get_proxy_pool_manager()
        return manager.get_pool_status()
    except Exception as e:
        return {"error": str(e)}


@app.post("/proxy-pool/refresh", tags=["root"])
async def refresh_proxy_pool(validate: bool = False):
    """Refresh proxy pool"""
    try:
        from app.services.proxy_pool_manager import init_proxy_pool

        count = init_proxy_pool(validate=validate)
        return {"refreshed": count}
    except Exception as e:
        return {"error": str(e)}
