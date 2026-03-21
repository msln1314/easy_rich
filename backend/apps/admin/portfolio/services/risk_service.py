from datetime import date, datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from apps.admin.portfolio import models, crud


class RiskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.portfolio_dal = crud.PortfolioDal(db)
        self.position_dal = crud.PositionDal(db)

    async def check_position_limit(
        self, portfolio_id: int, stock_code: str, additional_value: float = 0
    ) -> Dict[str, Any]:
        portfolio = await self.portfolio_dal.get_data(portfolio_id)
        positions = await self.position_dal.get_by_portfolio(portfolio_id)

        total_value = sum(pos.market_value or 0 for pos in positions)
        max_single = portfolio.max_single_position

        existing_position = await self.position_dal.get_by_stock(
            portfolio_id, stock_code
        )
        current_value = existing_position.market_value if existing_position else 0
        new_value = current_value + additional_value

        new_ratio = (
            round((new_value / (total_value + additional_value)) * 100, 2)
            if (total_value + additional_value) > 0
            else 0
        )

        violations = []
        if new_ratio > max_single:
            violations.append(
                {
                    "type": "single_position_exceeded",
                    "message": f"单只股票仓位 {new_ratio}% 超过限制 {max_single}%",
                    "current": new_ratio,
                    "limit": max_single,
                }
            )

        return {
            "is_valid": len(violations) == 0,
            "violations": violations,
            "current_ratio": new_ratio,
            "limit": max_single,
        }

    async def check_drawdown(self, portfolio_id: int) -> Dict[str, Any]:
        portfolio = await self.portfolio_dal.get_data(portfolio_id)

        if not portfolio.total_value or not portfolio.total_cost:
            return {"drawdown": 0, "is_alert": False}

        drawdown = 0
        if portfolio.total_cost > 0:
            drawdown = round(
                ((portfolio.total_cost - portfolio.total_value) / portfolio.total_cost)
                * 100,
                2,
            )

        is_alert = drawdown >= portfolio.max_drawdown

        return {
            "drawdown": drawdown,
            "max_drawdown": portfolio.max_drawdown,
            "is_alert": is_alert,
            "total_value": portfolio.total_value,
            "total_cost": portfolio.total_cost,
        }

    async def check_rebalance_needed(self, portfolio_id: int) -> Dict[str, Any]:
        portfolio = await self.portfolio_dal.get_data(portfolio_id)
        positions = await self.position_dal.get_by_portfolio(portfolio_id)

        total_value = sum(pos.market_value or 0 for pos in positions)
        threshold = portfolio.rebalance_threshold

        suggestions = []

        for pos in positions:
            if not pos.market_value or total_value == 0:
                continue

            current_ratio = round((pos.market_value / total_value) * 100, 2)
            target_ratio = pos.target_ratio

            if target_ratio:
                deviation = abs(current_ratio - target_ratio)
                if deviation > threshold:
                    action = "buy" if current_ratio < target_ratio else "sell"
                    suggestions.append(
                        {
                            "stock_code": pos.stock_code,
                            "stock_name": pos.stock_name,
                            "current_ratio": current_ratio,
                            "target_ratio": target_ratio,
                            "deviation": round(deviation, 2),
                            "suggested_action": action,
                        }
                    )

        return {
            "is_needed": len(suggestions) > 0,
            "threshold": threshold,
            "suggestions": suggestions,
        }

    async def generate_risk_alerts(
        self, portfolio_id: int
    ) -> List[models.PortfolioRiskAlert]:
        alerts = []

        drawdown_check = await self.check_drawdown(portfolio_id)
        if drawdown_check["is_alert"]:
            alert = models.PortfolioRiskAlert(
                portfolio_id=portfolio_id,
                alert_type="drawdown",
                alert_level="warning",
                title="回撤预警",
                content=f"当前回撤 {drawdown_check['drawdown']}% 已超过预警线 {drawdown_check['max_drawdown']}%",
                related_value=drawdown_check["drawdown"],
                threshold_value=drawdown_check["max_drawdown"],
            )
            alerts.append(alert)

        rebalance_check = await self.check_rebalance_needed(portfolio_id)
        if rebalance_check["is_needed"]:
            alert = models.PortfolioRiskAlert(
                portfolio_id=portfolio_id,
                alert_type="rebalance",
                alert_level="info",
                title="再平衡提醒",
                content=f"有 {len(rebalance_check['suggestions'])} 只股票偏离目标仓位超过阈值",
            )
            alerts.append(alert)

        for alert in alerts:
            self.db.add(alert)
        await self.db.flush()

        return alerts

    async def get_active_alerts(self, portfolio_id: int) -> List[Dict[str, Any]]:
        sql = (
            select(models.PortfolioRiskAlert)
            .where(
                and_(
                    models.PortfolioRiskAlert.portfolio_id == portfolio_id,
                    models.PortfolioRiskAlert.is_handled == 0,
                    models.PortfolioRiskAlert.is_delete == False,
                )
            )
            .order_by(models.PortfolioRiskAlert.created_at.desc())
        )

        result = await self.db.scalars(sql)
        alerts = result.all()

        return [
            {
                "id": a.id,
                "alert_type": a.alert_type,
                "alert_level": a.alert_level,
                "title": a.title,
                "content": a.content,
                "related_stock_code": a.related_stock_code,
                "related_value": a.related_value,
                "threshold_value": a.threshold_value,
                "is_read": a.is_read,
                "created_at": str(a.created_at),
            }
            for a in alerts
        ]

    async def handle_alert(
        self, alert_id: int, handle_note: Optional[str] = None
    ) -> models.PortfolioRiskAlert:
        sql = select(models.PortfolioRiskAlert).where(
            models.PortfolioRiskAlert.id == alert_id
        )
        result = await self.db.scalars(sql)
        alert = result.first()

        if alert:
            alert.is_handled = 1
            alert.handle_note = handle_note
            alert.handled_at = datetime.now()
            await self.db.flush()

        return alert

    async def pre_trade_risk_check(
        self, portfolio_id: int, stock_code: str, trade_type: str, amount: float
    ) -> Dict[str, Any]:
        checks = []

        if trade_type == "buy":
            position_check = await self.check_position_limit(
                portfolio_id, stock_code, amount
            )
            checks.append(
                {
                    "check_type": "position_limit",
                    "passed": position_check["is_valid"],
                    "details": position_check,
                }
            )

        drawdown_check = await self.check_drawdown(portfolio_id)
        checks.append(
            {
                "check_type": "drawdown",
                "passed": not drawdown_check["is_alert"],
                "details": drawdown_check,
            }
        )

        all_passed = all(c["passed"] for c in checks)

        return {
            "all_passed": all_passed,
            "checks": checks,
            "recommendation": "allow" if all_passed else "review",
        }
