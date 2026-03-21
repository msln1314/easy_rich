from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from apps.admin.portfolio import models, schemas


class PositionDal(DalBase):
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = models.PortfolioPosition
        self.schema = schemas.PositionOut

    async def get_by_portfolio(
        self, portfolio_id: int
    ) -> List[models.PortfolioPosition]:
        sql = (
            select(self.model)
            .where(
                and_(
                    self.model.portfolio_id == portfolio_id,
                    self.model.is_delete == False,
                )
            )
            .order_by(self.model.market_value.desc())
        )

        result = await self.db.scalars(sql)
        return result.all()

    async def get_by_stock(
        self, portfolio_id: int, stock_code: str
    ) -> Optional[models.PortfolioPosition]:
        sql = select(self.model).where(
            and_(
                self.model.portfolio_id == portfolio_id,
                self.model.stock_code == stock_code,
                self.model.is_delete == False,
            )
        )
        result = await self.db.scalars(sql)
        return result.first()

    async def add_position(
        self, portfolio_id: int, data: schemas.PositionCreate
    ) -> models.PortfolioPosition:
        obj = self.model(portfolio_id=portfolio_id, **data.model_dump())
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update_position(
        self, position: models.PortfolioPosition, shares: int, cost_price: float
    ):
        old_shares = position.shares
        old_cost = position.cost_price

        total_cost = old_shares * old_cost + shares * cost_price
        total_shares = old_shares + shares

        position.shares = total_shares
        position.cost_price = total_cost / total_shares
        await self.db.flush()
