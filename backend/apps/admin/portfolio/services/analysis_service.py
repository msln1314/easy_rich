import json
from datetime import date, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from apps.admin.portfolio import models, crud


class AnalysisService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.portfolio_dal = crud.PortfolioDal(db)
        self.position_dal = crud.PositionDal(db)
        self.trade_dal = crud.TradeDal(db)

    async def get_portfolio_performance(self, portfolio_id: int) -> Dict[str, Any]:
        portfolio = await self.portfolio_dal.get_data(portfolio_id)
        positions = await self.position_dal.get_by_portfolio(portfolio_id)

        total_value = 0
        total_cost = 0
        total_profit = 0
        dividend_total = 0

        for pos in positions:
            if pos.market_value:
                total_value += pos.market_value
            if pos.cost_price and pos.shares:
                total_cost += pos.cost_price * pos.shares
            if pos.profit:
                total_profit += pos.profit
            if pos.dividend_received:
                dividend_total += pos.dividend_received

        profit_rate = (
            round((total_profit / total_cost) * 100, 2) if total_cost > 0 else 0
        )

        return {
            "portfolio_id": portfolio_id,
            "portfolio_name": portfolio.name,
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "total_profit": round(total_profit, 2),
            "profit_rate": profit_rate,
            "dividend_received": round(dividend_total, 2),
            "position_count": len(positions),
            "benchmark_index": portfolio.benchmark_index,
        }

    async def get_position_analysis(self, portfolio_id: int) -> Dict[str, Any]:
        positions = await self.position_dal.get_by_portfolio(portfolio_id)

        if not positions:
            return {"positions": [], "sector_allocation": {}, "top_holdings": []}

        total_value = sum(pos.market_value or 0 for pos in positions)

        position_data = []
        sector_allocation = {}

        for pos in positions:
            pos_ratio = 0
            if pos.market_value and total_value > 0:
                pos_ratio = round((pos.market_value / total_value) * 100, 2)

            position_data.append(
                {
                    "stock_code": pos.stock_code,
                    "stock_name": pos.stock_name,
                    "shares": pos.shares,
                    "cost_price": pos.cost_price,
                    "current_price": pos.current_price,
                    "market_value": pos.market_value,
                    "profit": pos.profit,
                    "profit_rate": pos.profit_rate,
                    "position_ratio": pos_ratio,
                    "target_ratio": pos.target_ratio,
                    "dividend_received": pos.dividend_received,
                }
            )

        sorted_positions = sorted(
            position_data, key=lambda x: x.get("market_value", 0) or 0, reverse=True
        )
        top_holdings = sorted_positions[:10]

        return {
            "positions": position_data,
            "sector_allocation": sector_allocation,
            "top_holdings": top_holdings,
        }

    async def get_trade_statistics(
        self, portfolio_id: int, days: int = 30
    ) -> Dict[str, Any]:
        start_date = date.today() - timedelta(days=days)
        trades = await self.trade_dal.get_by_portfolio(portfolio_id, limit=1000)

        recent_trades = [t for t in trades if t.trade_date >= start_date]

        buy_count = 0
        sell_count = 0
        buy_amount = 0
        sell_amount = 0
        total_commission = 0
        total_stamp_duty = 0

        for trade in recent_trades:
            if trade.trade_type == "buy":
                buy_count += 1
                buy_amount += trade.amount
            elif trade.trade_type == "sell":
                sell_count += 1
                sell_amount += trade.amount
            total_commission += trade.commission
            total_stamp_duty += trade.stamp_duty

        return {
            "period_days": days,
            "total_trades": len(recent_trades),
            "buy_count": buy_count,
            "sell_count": sell_count,
            "buy_amount": round(buy_amount, 2),
            "sell_amount": round(sell_amount, 2),
            "total_commission": round(total_commission, 2),
            "total_stamp_duty": round(total_stamp_duty, 2),
            "total_cost": round(total_commission + total_stamp_duty, 2),
        }

    async def get_profit_attribution(self, portfolio_id: int) -> Dict[str, Any]:
        positions = await self.position_dal.get_by_portfolio(portfolio_id)

        total_profit = sum(pos.profit or 0 for pos in positions)

        attribution = []
        for pos in positions:
            if pos.profit:
                contribution = (
                    round((pos.profit / total_profit) * 100, 2)
                    if total_profit != 0
                    else 0
                )
                attribution.append(
                    {
                        "stock_code": pos.stock_code,
                        "stock_name": pos.stock_name,
                        "profit": round(pos.profit, 2),
                        "profit_rate": pos.profit_rate,
                        "contribution": contribution,
                    }
                )

        attribution.sort(key=lambda x: x["profit"], reverse=True)

        return {
            "total_profit": round(total_profit, 2),
            "top_winners": attribution[:5] if attribution else [],
            "top_losers": attribution[-5:][::-1]
            if attribution and len(attribution) > 1
            else [],
        }

    async def generate_snapshot(
        self, portfolio_id: int, snapshot_date: date
    ) -> models.PortfolioSnapshot:
        performance = await self.get_portfolio_performance(portfolio_id)
        position_analysis = await self.get_position_analysis(portfolio_id)

        snapshot = models.PortfolioSnapshot(
            portfolio_id=portfolio_id,
            snapshot_date=snapshot_date,
            total_value=performance["total_value"],
            total_cost=performance["total_cost"],
            profit_rate=performance["profit_rate"],
            sector_allocation=json.dumps(position_analysis["sector_allocation"]),
            top_holdings=json.dumps(position_analysis["top_holdings"]),
        )

        self.db.add(snapshot)
        await self.db.flush()
        return snapshot

    async def get_historical_performance(
        self, portfolio_id: int, days: int = 90
    ) -> List[Dict[str, Any]]:
        start_date = date.today() - timedelta(days=days)

        sql = (
            select(models.PortfolioSnapshot)
            .where(
                and_(
                    models.PortfolioSnapshot.portfolio_id == portfolio_id,
                    models.PortfolioSnapshot.snapshot_date >= start_date,
                    models.PortfolioSnapshot.is_delete == False,
                )
            )
            .order_by(models.PortfolioSnapshot.snapshot_date)
        )

        result = await self.db.scalars(sql)
        snapshots = result.all()

        return [
            {
                "date": str(s.snapshot_date),
                "total_value": s.total_value,
                "profit_rate": s.profit_rate,
            }
            for s in snapshots
        ]
