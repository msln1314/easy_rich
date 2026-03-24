from datetime import date
from typing import Any, Optional, List
from sqlalchemy.orm.strategy_options import _AbstractLoad
from sqlalchemy import select, func, desc
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from apps.admin.fund import models, schemas


class FundCompanyDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(FundCompanyDal, self).__init__()
        self.db = db
        self.model = models.FundCompany
        self.schema = schemas.FundCompanyOut

    async def get_company_list(
        self,
        page: int = 1,
        limit: int = 20,
        company_name: Optional[str] = None,
    ) -> tuple:
        sql = select(self.model)
        if company_name:
            sql = sql.where(self.model.company_name.like(f"%{company_name}%"))
        sql = sql.order_by(desc(self.model.management_scale))

        count_sql = select(func.count()).select_from(sql.alias())
        count_result = await self.db.scalar(count_sql)
        total = count_result or 0

        sql = sql.offset((page - 1) * limit).limit(limit)
        result = await self.db.scalars(sql)
        datas = [
            schemas.FundCompanyOut.model_validate(i).model_dump() for i in result.all()
        ]
        return datas, total

    async def get_company_by_code(self, company_code: str) -> Optional[dict]:
        sql = select(self.model).where(self.model.company_code == company_code)
        result = await self.db.scalar(sql)
        if result:
            return schemas.FundCompanyOut.model_validate(result).model_dump()
        return None


class FundHoldingDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(FundHoldingDal, self).__init__()
        self.db = db
        self.model = models.FundHolding
        self.schema = schemas.FundHoldingOut

    async def get_stock_holdings(
        self,
        stock_code: str,
        report_date: Optional[date] = None,
        change_type: Optional[str] = None,
        page: int = 1,
        limit: int = 50,
    ) -> tuple:
        sql = select(self.model).where(self.model.stock_code == stock_code)
        if report_date:
            sql = sql.where(self.model.report_date == report_date)
        if change_type:
            sql = sql.where(self.model.change_type == change_type)
        sql = sql.order_by(desc(self.model.holding_value))

        count_sql = select(func.count()).select_from(sql.alias())
        count_result = await self.db.scalar(count_sql)
        total = count_result or 0

        sql = sql.offset((page - 1) * limit).limit(limit)
        result = await self.db.scalars(sql)
        datas = [
            schemas.FundHoldingOut.model_validate(i).model_dump() for i in result.all()
        ]
        return datas, total

    async def get_fund_holdings(
        self,
        fund_code: str,
        report_date: Optional[date] = None,
        page: int = 1,
        limit: int = 50,
    ) -> tuple:
        sql = select(self.model).where(self.model.fund_code == fund_code)
        if report_date:
            sql = sql.where(self.model.report_date == report_date)
        sql = sql.order_by(desc(self.model.holding_value))

        count_sql = select(func.count()).select_from(sql.alias())
        count_result = await self.db.scalar(count_sql)
        total = count_result or 0

        sql = sql.offset((page - 1) * limit).limit(limit)
        result = await self.db.scalars(sql)
        datas = [
            schemas.FundHoldingOut.model_validate(i).model_dump() for i in result.all()
        ]
        return datas, total

    async def get_latest_report_date(self, stock_code: str) -> Optional[date]:
        sql = select(func.max(self.model.report_date)).where(
            self.model.stock_code == stock_code
        )
        result = await self.db.scalar(sql)
        return result


class MainForceDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(MainForceDal, self).__init__()
        self.db = db
        self.model = models.StockMainForceOverview
        self.schema = schemas.MainForceOverviewOut

    async def get_overview(self, stock_code: str) -> Optional[dict]:
        sql = select(self.model).where(self.model.stock_code == stock_code)
        sql = sql.order_by(desc(self.model.report_date)).limit(1)
        result = await self.db.scalar(sql)
        if result:
            return schemas.MainForceOverviewOut.model_validate(result).model_dump()
        return None

    async def get_trend(self, stock_code: str, limit: int = 8) -> List[dict]:
        sql = select(self.model).where(self.model.stock_code == stock_code)
        sql = sql.order_by(desc(self.model.report_date)).limit(limit)
        result = await self.db.scalars(sql)
        return [
            schemas.MainForceOverviewOut.model_validate(i).model_dump()
            for i in result.all()
        ]

    async def get_mainforce_funds(
        self,
        stock_code: str,
        report_date: date,
        change_type: Optional[str] = None,
        page: int = 1,
        limit: int = 50,
    ) -> tuple:
        holding_dal = FundHoldingDal(self.db)
        return await holding_dal.get_stock_holdings(
            stock_code=stock_code,
            report_date=report_date,
            change_type=change_type,
            page=page,
            limit=limit,
        )


class MainForceAlertDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(MainForceAlertDal, self).__init__()
        self.db = db
        self.model = models.MainForceAlert
        self.schema = schemas.MainForceAlertOut

    async def create_alert(
        self,
        user_id: int,
        data: schemas.MainForceAlertCreate,
    ) -> dict:
        obj = self.model(
            user_id=user_id,
            stock_code=data.stock_code,
            stock_name=data.stock_name,
            alert_type=data.alert_type,
            alert_level=data.alert_level,
            alert_content=data.alert_content,
            fund_code=data.fund_code,
            fund_name=data.fund_name,
        )
        await self.flush(obj)
        return schemas.MainForceAlertOut.model_validate(obj).model_dump()

    async def get_user_alerts(
        self,
        user_id: int,
        is_read: Optional[int] = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple:
        sql = select(self.model).where(self.model.user_id == user_id)
        if is_read is not None:
            sql = sql.where(self.model.is_read == is_read)
        sql = sql.order_by(desc(self.model.created_at))

        count_sql = select(func.count()).select_from(sql.alias())
        count_result = await self.db.scalar(count_sql)
        total = count_result or 0

        sql = sql.offset((page - 1) * limit).limit(limit)
        result = await self.db.scalars(sql)
        datas = [
            schemas.MainForceAlertOut.model_validate(i).model_dump()
            for i in result.all()
        ]
        return datas, total

    async def mark_as_read(self, alert_id: int, user_id: int) -> bool:
        sql = select(self.model).where(
            self.model.id == alert_id, self.model.user_id == user_id
        )
        result = await self.db.scalar(sql)
        if result:
            result.is_read = 1
            result.read_time = date.today()
            await self.db.flush()
            return True
        return False
