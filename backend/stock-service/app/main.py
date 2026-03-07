from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router  # 使用router.py中的api_router
from app.core.config import settings
from app.mcp.router import mcp_router  # 修改导入路径

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="股票分析服务API，基于AKShare数据",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)
# 包含MCP路由
app.include_router(mcp_router)

@app.get("/")
async def root():
    return {"message": "欢迎使用股票分析服务API"}