from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from apps.admin.portfolio import models, schemas


class PortfolioDal(DalBase):
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = models.Portfolio
        self.schema = schemas.PortfolioOut

    async def get_list_by_user(self, user_id: int) -> List[models.Portfolio]:
        sql = (
            select(self.model)
            .where(and_(self.model.user_id == user_id, self.model.is_delete == False))
            .order_by(self.model.is_default.desc(), self.model.created_at.desc())
        )

        result = await self.db.scalars(sql)
        return result.all()

    async def get_default_portfolio(self, user_id: int) -> Optional[models.Portfolio]:
        sql = select(self.model).where(
            and_(
                self.model.user_id == user_id,
                self.model.is_default == 1,
                self.model.is_delete == False,
            )
        )
        result = await self.db.scalars(sql)
        return result.first()

    async def create_portfolio(
        self, data: schemas.PortfolioCreate, user_id: int
    ) -> models.Portfolio:
        obj = self.model(user_id=user_id, **data.model_dump())
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def set_default(self, portfolio_id: int, user_id: int):
        portfolios = await self.get_list_by_user(user_id)
        for p in portfolios:
            p.is_default = 0

        portfolio = await self.get_data(portfolio_id)
        if portfolio:
            portfolio.is_default = 1
        await self.db.flush()
