# backend/qmt-service/app/api/endpoints/trade_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models.trade_models import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    CancelOrderResponse,
    OrderStatus,
)
from app.services.trade_service import trade_service

router = APIRouter()


@router.post("/order", response_model=OrderResponse, summary="下单")
async def place_order(order: OrderCreate):
    """下单"""
    try:
        return await trade_service.place_order(order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/order/{order_id}", response_model=CancelOrderResponse, summary="撤单")
async def cancel_order(order_id: str):
    """撤单"""
    try:
        return await trade_service.cancel_order(order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders", response_model=OrderListResponse, summary="查询委托列表")
async def get_orders(
    status: Optional[OrderStatus] = Query(None, description="订单状态筛选"),
    date: Optional[str] = Query(None, description="日期筛选（YYYYMMDD）")
):
    """查询委托列表"""
    try:
        orders = await trade_service.get_orders(status, date)
        return OrderListResponse(orders=orders, total=len(orders))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders/{order_id}", response_model=OrderResponse, summary="查询委托详情")
async def get_order(order_id: str):
    """查询委托详情"""
    try:
        order = await trade_service.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="委托不存在")
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))