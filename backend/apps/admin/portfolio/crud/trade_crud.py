from typing import List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from apps.admin.portfolio import models, schemas


class TradeDal(DalBase):
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = models.PortfolioTrade
        self.schema = schemas.TradeOut

    async def get_by_portfolio(
        self, portfolio_id: int, limit: int = 50
    ) -> List[models.PortfolioTrade]:
        sql = (
            select(self.model)
            .where(
                and_(
                    self.model.portfolio_id == portfolio_id,
                    self.model.is_delete == False,
                )
            )
            .order_by(self.model.trade_date.desc())
            .limit(limit)
        )

        result = await self.db.scalars(sql)
        return result.all()

    async def get_by_stock(
        self, portfolio_id: int, stock_code: str, limit: int = 20
    ) -> List[models.PortfolioTrade]:
        sql = (
            select(self.model)
            .where(
                and_(
                    self.model.portfolio_id == portfolio_id,
                    self.model.stock_code == stock_code,
                    self.model.is_delete == False,
                )
            )
            .order_by(self.model.trade_date.desc())
            .limit(limit)
        )

        result = await self.db.scalars(sql)
        return result.all()
