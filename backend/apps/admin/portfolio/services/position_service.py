from datetime import date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from apps.admin.portfolio import models, schemas, crud


class PositionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.position_dal = crud.PositionDal(db)
        self.portfolio_dal = crud.PortfolioDal(db)
        self.trade_dal = crud.TradeDal(db)

    async def get_positions_with_calc(self, portfolio_id: int) -> List[dict]:
        positions = await self.position_dal.get_by_portfolio(portfolio_id)
        result = []
        total_value = 0

        for pos in positions:
            if pos.market_value:
                total_value += pos.market_value
            result.append(schemas.PositionOut.model_validate(pos).model_dump())

        for i, pos in enumerate(result):
            if pos.get("market_value") and total_value > 0:
                result[i]["position_ratio"] = round(
                    pos["market_value"] / total_value * 100, 2
                )

        return result

    async def update_position_prices(self, portfolio_id: int, price_data: dict) -> None:
        positions = await self.position_dal.get_by_portfolio(portfolio_id)

        for pos in positions:
            if pos.stock_code in price_data:
                new_price = price_data[pos.stock_code]
                pos.current_price = new_price
                pos.market_value = pos.shares * new_price
                if pos.cost_price > 0:
                    pos.profit = pos.market_value - (pos.shares * pos.cost_price)
                    pos.profit_rate = round(
                        (pos.profit / (pos.shares * pos.cost_price)) * 100, 2
                    )

        await self.db.flush()

    async def recalculate_portfolio_stats(self, portfolio_id: int) -> models.Portfolio:
        positions = await self.position_dal.get_by_portfolio(portfolio_id)

        total_value = 0
        total_cost = 0
        total_profit = 0

        for pos in positions:
            if pos.market_value:
                total_value += pos.market_value
            if pos.cost_price and pos.shares:
                total_cost += pos.cost_price * pos.shares
            if pos.profit:
                total_profit += pos.profit

        portfolio = await self.portfolio_dal.get_data(portfolio_id)
        portfolio.total_value = total_value
        portfolio.total_cost = total_cost
        portfolio.total_profit = total_profit

        if total_cost > 0:
            portfolio.profit_rate = round((total_profit / total_cost) * 100, 2)

        await self.db.flush()
        return portfolio

    async def get_position_summary(self, portfolio_id: int) -> dict:
        positions = await self.position_dal.get_by_portfolio(portfolio_id)

        total_shares = 0
        total_value = 0
        total_cost = 0
        total_profit = 0
        sector_distribution = {}

        for pos in positions:
            total_shares += 1
            if pos.market_value:
                total_value += pos.market_value
            if pos.cost_price and pos.shares:
                total_cost += pos.cost_price * pos.shares
            if pos.profit:
                total_profit += pos.profit

        profit_rate = (
            round((total_profit / total_cost) * 100, 2) if total_cost > 0 else 0
        )

        return {
            "total_positions": total_shares,
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "total_profit": round(total_profit, 2),
            "profit_rate": profit_rate,
            "sector_distribution": sector_distribution,
        }
