from datetime import date, timedelta
from typing import List, Optional, Tuple
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from apps.admin.stock_calendar import models, schemas


class StockCalendarEventDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(StockCalendarEventDal, self).__init__()
        self.db = db
        self.model = models.StockCalendarEvent
        self.schema = schemas.StockCalendarEventOut

    async def get_list(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        stock_code: Optional[str] = None,
        event_type: Optional[str] = None,
        is_watchlist: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[int, List[models.StockCalendarEvent]]:
        sql = select(self.model).where(self.model.is_delete == False)

        if start_date:
            sql = sql.where(self.model.event_date >= start_date)
        if end_date:
            sql = sql.where(self.model.event_date <= end_date)
        if stock_code:
            sql = sql.where(self.model.stock_code == stock_code)
        if event_type:
            sql = sql.where(self.model.event_type == event_type)
        if is_watchlist:
            sql = sql.where(self.model.is_in_watchlist == 1)

        count_sql = select(self.model.id).where(self.model.is_delete == False)
        if start_date:
            count_sql = count_sql.where(self.model.event_date >= start_date)
        if end_date:
            count_sql = count_sql.where(self.model.event_date <= end_date)
        if stock_code:
            count_sql = count_sql.where(self.model.stock_code == stock_code)
        if event_type:
            count_sql = count_sql.where(self.model.event_type == event_type)
        if is_watchlist:
            count_sql = count_sql.where(self.model.is_in_watchlist == 1)

        total_result = await self.db.execute(count_sql)
        total = len(total_result.all())

        sql = sql.order_by(self.model.event_date.asc())
        sql = sql.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.scalars(sql)
        items = result.all()

        return total, items

    async def get_by_stock(
        self, stock_code: str, days: int = 90
    ) -> List[models.StockCalendarEvent]:
        start = date.today()
        end = start + timedelta(days=days)

        sql = (
            select(self.model)
            .where(
                and_(
                    self.model.stock_code == stock_code,
                    self.model.event_date >= start,
                    self.model.event_date <= end,
                    self.model.is_delete == False,
                )
            )
            .order_by(self.model.event_date.asc())
        )

        result = await self.db.scalars(sql)
        return result.all()

    async def get_by_date(self, event_date: date) -> List[models.StockCalendarEvent]:
        sql = (
            select(self.model)
            .where(
                and_(self.model.event_date == event_date, self.model.is_delete == False)
            )
            .order_by(self.model.event_time.asc())
        )

        result = await self.db.scalars(sql)
        return result.all()

    async def create_event(
        self, data: schemas.StockCalendarEventCreate
    ) -> models.StockCalendarEvent:
        obj = self.model(**data.model_dump())
        self.db.add(obj)
        await self.db.flush()
        return obj


class StockEventReminderDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(StockEventReminderDal, self).__init__()
        self.db = db
        self.model = models.StockEventReminder
        self.schema = schemas.StockEventReminderOut

    async def get_list_by_user(
        self, user_id: int, is_active: Optional[int] = None
    ) -> List[models.StockEventReminder]:
        sql = select(self.model).where(
            and_(self.model.user_id == user_id, self.model.is_delete == False)
        )

        if is_active is not None:
            sql = sql.where(self.model.is_active == is_active)

        sql = sql.order_by(self.model.created_at.desc())

        result = await self.db.scalars(sql)
        return result.all()

    async def get_active_reminders(self) -> List[models.StockEventReminder]:
        sql = select(self.model).where(
            and_(self.model.is_active == 1, self.model.is_delete == False)
        )

        result = await self.db.scalars(sql)
        return result.all()

    async def create_reminder(
        self, data: schemas.StockEventReminderCreate
    ) -> models.StockEventReminder:
        obj = self.model(**data.model_dump())
        self.db.add(obj)
        await self.db.flush()
        return obj
