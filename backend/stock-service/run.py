import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # 允许所有网络接口访问
        port=8008,
        reload=True,
        log_level=settings.LOG_LEVEL.lower(),
        # SSE 优化配置
        proxy_headers=True,  # 支持代理头
        forwarded_allow_ips="*",  # 允许所有转发 IP
        timeout_keep_alive=300,  # 增加保持连接时间到5分钟
        # CORS 配置
        headers=[
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Headers", "*"),
            ("Access-Control-Allow-Methods", "*"),
            ("Access-Control-Allow-Credentials", "true"),
            ("Access-Control-Expose-Headers", "*"),
        ],
        # 其他优化配置
        limit_concurrency=1000,  # 增加并发连接数
        limit_max_requests=10000,  # 增加最大请求数
        backlog=2048,  # 增加待处理连接队列大小
    )