# backend/qmt-service/app/services/trade_service.py
"""
交易执行服务

提供下单、撤单、查询委托等功能
"""
import logging
from datetime import datetime
from typing import Optional, List
import uuid

from app.core.qmt_client import QMTClientManager
from app.models.trade_models import (
    OrderCreate,
    OrderResponse,
    OrderDirection,
    OrderType,
    OrderStatus,
    CancelOrderResponse,
)

logger = logging.getLogger(__name__)


class TradeService:
    """交易执行服务"""

    # 订单类型映射
    ORDER_TYPE_MAP = {
        OrderType.LIMIT: 23,    # 限价单
        OrderType.MARKET: 24,   # 市价单
    }

    # 方向映射
    DIRECTION_MAP = {
        OrderDirection.BUY: 23,    # 买入
        OrderDirection.SELL: 24,   # 卖出
    }

    # 状态映射（QMT状态 -> 系统状态）
    STATUS_MAP = {
        48: OrderStatus.PENDING,    # 未报
        49: OrderStatus.PENDING,    # 待报
        50: OrderStatus.PENDING,    # 已报
        51: OrderStatus.PARTIAL,    # 部成
        52: OrderStatus.FILLED,     # 全成
        53: OrderStatus.CANCELLED,  # 已撤
        54: OrderStatus.CANCELLED,  # 已撤
        55: OrderStatus.REJECTED,   # 废单
    }

    async def place_order(self, order: OrderCreate) -> OrderResponse:
        """下单"""
        if not QMTClientManager.is_connected():
            # 模拟模式
            return self._mock_place_order(order)

        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()

            # 下单
            order_id = trader.order_stock(
                account,
                order.stock_code,
                self.ORDER_TYPE_MAP[order.order_type],
                self.DIRECTION_MAP[order.direction],
                order.quantity,
                order.price or 0  # 市价单价格为0
            )

            if order_id <= 0:
                raise Exception("下单失败，返回无效订单ID")

            now = datetime.now()
            return OrderResponse(
                order_id=str(order_id),
                stock_code=order.stock_code,
                stock_name="",  # 需要额外查询
                direction=order.direction,
                price=order.price or 0,
                quantity=order.quantity,
                order_type=order.order_type,
                status=OrderStatus.PENDING,
                filled_quantity=0,
                filled_price=0,
                created_time=now,
                updated_time=now,
                message="下单成功"
            )

        except Exception as e:
            logger.error(f"下单失败: {e}")
            raise

    def _mock_place_order(self, order: OrderCreate) -> OrderResponse:
        """模拟下单（QMT未连接时使用）"""
        now = datetime.now()
        mock_order_id = str(uuid.uuid4())[:8]

        logger.info(f"[模拟模式] 下单: {order.stock_code} {order.direction.value} {order.quantity}@{order.price}")

        return OrderResponse(
            order_id=mock_order_id,
            stock_code=order.stock_code,
            stock_name=f"模拟股票_{order.stock_code}",
            direction=order.direction,
            price=order.price or 10.0,
            quantity=order.quantity,
            order_type=order.order_type,
            status=OrderStatus.PENDING,
            filled_quantity=0,
            filled_price=0,
            created_time=now,
            updated_time=now,
            message="[模拟]下单成功"
        )

    async def cancel_order(self, order_id: str) -> CancelOrderResponse:
        """撤单"""
        if not QMTClientManager.is_connected():
            return CancelOrderResponse(
                order_id=order_id,
                success=True,
                message="[模拟]撤单成功"
            )

        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()

            result = trader.cancel_order(account, int(order_id))

            return CancelOrderResponse(
                order_id=order_id,
                success=result > 0,
                message="撤单成功" if result > 0 else "撤单失败"
            )

        except Exception as e:
            logger.error(f"撤单失败: {e}")
            return CancelOrderResponse(
                order_id=order_id,
                success=False,
                message=f"撤单失败: {str(e)}"
            )

    async def get_orders(
        self,
        status: Optional[OrderStatus] = None,
        date: Optional[str] = None
    ) -> List[OrderResponse]:
        """查询委托列表"""
        if not QMTClientManager.is_connected():
            return self._mock_get_orders()

        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()

            orders = trader.query_stock_orders(account)

            result = []
            for o in orders:
                order_response = self._convert_order(o)
                if status and order_response.status != status:
                    continue
                result.append(order_response)

            return result

        except Exception as e:
            logger.error(f"查询委托列表失败: {e}")
            return []

    def _mock_get_orders(self) -> List[OrderResponse]:
        """模拟查询委托列表"""
        now = datetime.now()
        return [
            OrderResponse(
                order_id="mock001",
                stock_code="000001",
                stock_name="平安银行",
                direction=OrderDirection.BUY,
                price=12.5,
                quantity=1000,
                order_type=OrderType.LIMIT,
                status=OrderStatus.PENDING,
                filled_quantity=0,
                filled_price=0,
                created_time=now,
                updated_time=now,
                message="[模拟]待成交"
            )
        ]

    async def get_order(self, order_id: str) -> Optional[OrderResponse]:
        """查询单个委托"""
        if not QMTClientManager.is_connected():
            orders = self._mock_get_orders()
            for o in orders:
                if o.order_id == order_id:
                    return o
            return None

        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()

            order = trader.query_stock_order(account, int(order_id))
            if order:
                return self._convert_order(order)
            return None

        except Exception as e:
            logger.error(f"查询委托失败: {e}")
            return None

    def _convert_order(self, qmt_order) -> OrderResponse:
        """转换QMT订单对象"""
        now = datetime.now()
        return OrderResponse(
            order_id=str(qmt_order.order_id),
            stock_code=qmt_order.stock_code,
            stock_name=qmt_order.stock_name or "",
            direction=OrderDirection.BUY if qmt_order.order_type == 23 else OrderDirection.SELL,
            price=qmt_order.price,
            quantity=qmt_order.order_volume,
            order_type=OrderType.LIMIT,
            status=self.STATUS_MAP.get(qmt_order.order_status, OrderStatus.PENDING),
            filled_quantity=qmt_order.traded_volume or 0,
            filled_price=qmt_order.traded_price or 0,
            created_time=now,
            updated_time=now,
        )


# 单例
trade_service = TradeService()