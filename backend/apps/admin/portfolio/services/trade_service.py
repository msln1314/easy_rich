from datetime import date
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from apps.admin.portfolio import models, schemas, crud
from apps.admin.portfolio.services.position_service import PositionService


class TradeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.position_dal = crud.PositionDal(db)
        self.trade_dal = crud.TradeDal(db)
        self.portfolio_dal = crud.PortfolioDal(db)
        self.position_service = PositionService(db)

    async def execute_buy(
        self,
        portfolio_id: int,
        stock_code: str,
        stock_name: Optional[str],
        shares: int,
        price: float,
        trade_date: date,
        commission: float = 0,
        remark: Optional[str] = None,
    ) -> models.PortfolioTrade:
        existing_position = await self.position_dal.get_by_stock(
            portfolio_id, stock_code
        )

        position_before = 0
        cost_price_before = 0
        cost_price_after = price
        position_after = shares

        if existing_position:
            position_before = existing_position.shares
            cost_price_before = existing_position.cost_price

            old_total_cost = position_before * cost_price_before
            new_cost = shares * price
            total_shares = position_before + shares

            cost_price_after = (old_total_cost + new_cost) / total_shares
            position_after = total_shares

            existing_position.shares = position_after
            existing_position.cost_price = cost_price_after
            existing_position.available_shares = position_after
            existing_position.last_trade_date = trade_date
            if stock_name:
                existing_position.stock_name = stock_name
        else:
            position_data = schemas.PositionCreate(
                stock_code=stock_code,
                stock_name=stock_name,
                shares=shares,
                cost_price=price,
            )
            new_position = await self.position_dal.add_position(
                portfolio_id, position_data
            )
            new_position.available_shares = shares
            new_position.first_buy_date = trade_date
            new_position.last_trade_date = trade_date

        trade_data = {
            "portfolio_id": portfolio_id,
            "stock_code": stock_code,
            "stock_name": stock_name,
            "trade_type": "buy",
            "trade_date": trade_date,
            "shares": shares,
            "price": price,
            "amount": shares * price,
            "commission": commission,
            "stamp_duty": 0,
            "position_before": position_before,
            "position_after": position_after,
            "cost_price_before": cost_price_before,
            "cost_price_after": cost_price_after,
            "source": "manual",
            "remark": remark,
        }
        trade = await self.trade_dal.create_data(trade_data)

        await self.position_service.recalculate_portfolio_stats(portfolio_id)

        return trade

    async def execute_sell(
        self,
        portfolio_id: int,
        stock_code: str,
        shares: int,
        price: float,
        trade_date: date,
        commission: float = 0,
        stamp_duty: float = 0,
        remark: Optional[str] = None,
    ) -> models.PortfolioTrade:
        existing_position = await self.position_dal.get_by_stock(
            portfolio_id, stock_code
        )

        if not existing_position:
            raise ValueError(f"持仓不存在: {stock_code}")

        if (
            existing_position.available_shares
            and existing_position.available_shares < shares
        ):
            raise ValueError(
                f"可用股数不足: 可用 {existing_position.available_shares}, 请求卖出 {shares}"
            )

        position_before = existing_position.shares
        cost_price_before = existing_position.cost_price
        position_after = position_before - shares

        cost_price_after = cost_price_before if position_after > 0 else 0

        if position_after > 0:
            existing_position.shares = position_after
            if existing_position.available_shares:
                existing_position.available_shares -= shares
            existing_position.last_trade_date = trade_date
        else:
            await self.position_dal.delete_datas([existing_position.id], v_soft=False)

        trade_data = {
            "portfolio_id": portfolio_id,
            "stock_code": stock_code,
            "stock_name": existing_position.stock_name,
            "trade_type": "sell",
            "trade_date": trade_date,
            "shares": shares,
            "price": price,
            "amount": shares * price,
            "commission": commission,
            "stamp_duty": stamp_duty,
            "position_before": position_before,
            "position_after": position_after,
            "cost_price_before": cost_price_before,
            "cost_price_after": cost_price_after,
            "source": "manual",
            "remark": remark,
        }
        trade = await self.trade_dal.create_data(trade_data)

        await self.position_service.recalculate_portfolio_stats(portfolio_id)

        return trade

    async def record_dividend(
        self,
        portfolio_id: int,
        stock_code: str,
        amount: float,
        trade_date: date,
        remark: Optional[str] = None,
    ) -> models.PortfolioTrade:
        existing_position = await self.position_dal.get_by_stock(
            portfolio_id, stock_code
        )

        if not existing_position:
            raise ValueError(f"持仓不存在: {stock_code}")

        existing_position.dividend_received = (
            existing_position.dividend_received or 0
        ) + amount

        trade_data = {
            "portfolio_id": portfolio_id,
            "stock_code": stock_code,
            "stock_name": existing_position.stock_name,
            "trade_type": "dividend",
            "trade_date": trade_date,
            "shares": 0,
            "price": 0,
            "amount": amount,
            "commission": 0,
            "stamp_duty": 0,
            "position_before": existing_position.shares,
            "position_after": existing_position.shares,
            "cost_price_before": existing_position.cost_price,
            "cost_price_after": existing_position.cost_price,
            "source": "manual",
            "remark": remark or "分红入账",
        }
        trade = await self.trade_dal.create_data(trade_data)

        await self.db.flush()
        return trade
