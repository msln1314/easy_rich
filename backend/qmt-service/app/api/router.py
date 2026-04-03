# backend/qmt-service/app/api/router.py
from fastapi import APIRouter

from app.api.endpoints import trade_routes, position_routes

api_router = APIRouter()

api_router.include_router(trade_routes.router, prefix="/trade", tags=["trade"])
api_router.include_router(position_routes.router, prefix="/position", tags=["position"])