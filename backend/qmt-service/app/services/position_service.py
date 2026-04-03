# backend/qmt-service/app/services/position_service.py
"""
持仓管理服务

提供持仓查询、资金余额、成交记录等功能
"""
import logging
from datetime import datetime
from typing import List, Optional

from app.core.qmt_client import QMTClientManager
from app.models.position_models import (
    Position,
    PositionListResponse,
    Balance,
    Trade,
    TradeListResponse,
)

logger = logging.getLogger(__name__)


class PositionService:
    """持仓管理服务"""

    async def get_positions(self) -> PositionListResponse:
        """查询持仓列表"""
        if not QMTClientManager.is_connected():
            return self._mock_get_positions()

        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()

            positions = trader.query_stock_positions(account)

            result = []
            total_market_value = 0.0
            total_profit = 0.0

            for p in positions:
                position = self._convert_position(p)
                result.append(position)
                total_market_value += position.market_value
                total_profit += position.profit

            return PositionListResponse(
                positions=result,
                total_market_value=total_market_value,
                total_profit=total_profit,
                count=len(result)
            )

        except Exception as e:
            logger.error(f"查询持仓失败: {e}")
            return PositionListResponse(
                positions=[],
                total_market_value=0,
                total_profit=0,
                count=0
            )

    def _mock_get_positions(self) -> PositionListResponse:
        """模拟查询持仓"""
        now = datetime.now()
        positions = [
            Position(
                stock_code="000001",
                stock_name="平安银行",
                quantity=1000,
                available=1000,
                cost_price=12.0,
                current_price=12.5,
                profit=500.0,
                profit_rate=4.17,
                market_value=12500.0,
                updated_time=now
            ),
            Position(
                stock_code="600519",
                stock_name="贵州茅台",
                quantity=100,
                available=100,
                cost_price=1800.0,
                current_price=1850.0,
                profit=5000.0,
                profit_rate=2.78,
                market_value=185000.0,
                updated_time=now
            )
        ]

        total_mv = sum(p.market_value for p in positions)
        total_profit = sum(p.profit for p in positions)

        return PositionListResponse(
            positions=positions,
            total_market_value=total_mv,
            total_profit=total_profit,
            count=len(positions)
        )

    async def get_balance(self) -> Balance:
        """查询资金余额"""
        if not QMTClientManager.is_connected():
            return self._mock_get_balance()

        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()

            asset = trader.query_stock_asset(account)

            return Balance(
                total_asset=asset.total_asset,
                available_cash=asset.cash,
                market_value=asset.market_value,
                frozen_cash=asset.frozen_cash if hasattr(asset, 'frozen_cash') else 0,
                profit_today=0,
                profit_total=0,
                updated_time=datetime.now()
            )

        except Exception as e:
            logger.error(f"查询资金余额失败: {e}")
            return self._mock_get_balance()

    def _mock_get_balance(self) -> Balance:
        """模拟查询资金余额"""
        return Balance(
            total_asset=500000.0,
            available_cash=300000.0,
            market_value=197500.0,
            frozen_cash=2500.0,
            profit_today=5500.0,
            profit_total=15000.0,
            updated_time=datetime.now()
        )

    async def get_trades(
        self,
        date: Optional[str] = None,
        stock_code: Optional[str] = None
    ) -> TradeListResponse:
        """查询成交记录"""
        if not QMTClientManager.is_connected():
            return self._mock_get_trades()

        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()

            trades = trader.query_stock_trades(account)

            result = []
            for t in trades:
                trade = self._convert_trade(t)
                if stock_code and trade.stock_code != stock_code:
                    continue
                result.append(trade)

            return TradeListResponse(
                trades=result,
                total=len(result)
            )

        except Exception as e:
            logger.error(f"查询成交记录失败: {e}")
            return TradeListResponse(trades=[], total=0)

    def _mock_get_trades(self) -> TradeListResponse:
        """模拟查询成交记录"""
        now = datetime.now()
        trades = [
            Trade(
                trade_id="t001",
                order_id="mock001",
                stock_code="000001",
                stock_name="平安银行",
                direction="buy",
                price=12.0,
                quantity=1000,
                trade_time=now,
                commission=5.0
            )
        ]

        return TradeListResponse(trades=trades, total=len(trades))

    async def get_today_trades(self) -> TradeListResponse:
        """查询今日成交"""
        today = datetime.now().strftime("%Y%m%d")
        return await self.get_trades(date=today)

    def _convert_position(self, qmt_position) -> Position:
        """转换QMT持仓对象"""
        now = datetime.now()
        quantity = qmt_position.volume
        cost_price = qmt_position.open_price
        current_price = qmt_position.market_price if hasattr(qmt_position, 'market_price') else cost_price
        profit = (current_price - cost_price) * quantity
        profit_rate = ((current_price - cost_price) / cost_price * 100) if cost_price > 0 else 0

        return Position(
            stock_code=qmt_position.stock_code,
            stock_name=qmt_position.stock_name or "",
            quantity=quantity,
            available=qmt_position.can_use_volume if hasattr(qmt_position, 'can_use_volume') else quantity,
            cost_price=cost_price,
            current_price=current_price,
            profit=profit,
            profit_rate=round(profit_rate, 2),
            market_value=current_price * quantity,
            updated_time=now
        )

    def _convert_trade(self, qmt_trade) -> Trade:
        """转换QMT成交对象"""
        return Trade(
            trade_id=str(qmt_trade.order_id),
            order_id=str(qmt_trade.order_id),
            stock_code=qmt_trade.stock_code,
            stock_name=qmt_trade.stock_name or "",
            direction="buy" if qmt_trade.order_type == 23 else "sell",
            price=qmt_trade.traded_price,
            quantity=qmt_trade.traded_volume,
            trade_time=datetime.now(),
            commission=qmt_trade.commission if hasattr(qmt_trade, 'commission') else 0
        )


# 单例
position_service = PositionService()