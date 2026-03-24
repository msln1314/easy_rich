from fastapi import APIRouter, Depends, Query, BackgroundTasks
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, Auth
from . import schemas, crud
from .services.data_sync import FundDataSyncService

router = APIRouter()


@router.get("/companies", summary="获取基金公司列表")
async def get_company_list(
    page: int = 1,
    limit: int = 20,
    company_name: str | None = None,
    auth: Auth = Depends(AllUserAuth()),
):
    datas, total = await crud.FundCompanyDal(auth.db).get_company_list(
        page=page,
        limit=limit,
        company_name=company_name,
    )
    return SuccessResponse(datas, count=total)


@router.get("/companies/{company_code}", summary="获取基金公司详情")
async def get_company_detail(
    company_code: str,
    auth: Auth = Depends(AllUserAuth()),
):
    data = await crud.FundCompanyDal(auth.db).get_company_by_code(company_code)
    return SuccessResponse(data)


@router.get("/mainforce/{stock_code}/overview", summary="获取个股主力概览")
async def get_mainforce_overview(
    stock_code: str,
    auth: Auth = Depends(AllUserAuth()),
):
    data = await crud.MainForceDal(auth.db).get_overview(stock_code)
    return SuccessResponse(data)


@router.get("/mainforce/{stock_code}/trend", summary="获取个股主力趋势")
async def get_mainforce_trend(
    stock_code: str,
    limit: int = 8,
    auth: Auth = Depends(AllUserAuth()),
):
    datas = await crud.MainForceDal(auth.db).get_trend(stock_code, limit)
    return SuccessResponse(datas)


@router.get("/mainforce/{stock_code}/funds", summary="获取个股主力基金列表")
async def get_mainforce_funds(
    stock_code: str,
    change_type: str | None = None,
    page: int = 1,
    limit: int = 50,
    auth: Auth = Depends(AllUserAuth()),
):
    holding_dal = crud.FundHoldingDal(auth.db)
    report_date = await holding_dal.get_latest_report_date(stock_code)
    if not report_date:
        return SuccessResponse([], count=0)

    datas, total = await crud.MainForceDal(auth.db).get_mainforce_funds(
        stock_code=stock_code,
        report_date=report_date,
        change_type=change_type,
        page=page,
        limit=limit,
    )
    return SuccessResponse(datas, count=total)


@router.get("/holdings/stock/{stock_code}", summary="获取股票的基金持仓")
async def get_stock_holdings(
    stock_code: str,
    report_date: str | None = None,
    page: int = 1,
    limit: int = 50,
    auth: Auth = Depends(AllUserAuth()),
):
    from datetime import datetime

    rd = datetime.strptime(report_date, "%Y-%m-%d").date() if report_date else None
    datas, total = await crud.FundHoldingDal(auth.db).get_stock_holdings(
        stock_code=stock_code,
        report_date=rd,
        page=page,
        limit=limit,
    )
    return SuccessResponse(datas, count=total)


@router.get("/holdings/fund/{fund_code}", summary="获取基金的持仓明细")
async def get_fund_holdings(
    fund_code: str,
    report_date: str | None = None,
    page: int = 1,
    limit: int = 50,
    auth: Auth = Depends(AllUserAuth()),
):
    from datetime import datetime

    rd = datetime.strptime(report_date, "%Y-%m-%d").date() if report_date else None
    datas, total = await crud.FundHoldingDal(auth.db).get_fund_holdings(
        fund_code=fund_code,
        report_date=rd,
        page=page,
        limit=limit,
    )
    return SuccessResponse(datas, count=total)


@router.get("/alerts", summary="获取主力预警列表")
async def get_alert_list(
    is_read: int | None = None,
    page: int = 1,
    limit: int = 20,
    auth: Auth = Depends(AllUserAuth()),
):
    datas, total = await crud.MainForceAlertDal(auth.db).get_user_alerts(
        user_id=auth.user.id,
        is_read=is_read,
        page=page,
        limit=limit,
    )
    return SuccessResponse(datas, count=total)


@router.post("/alerts", summary="创建主力预警")
async def create_alert(
    data: schemas.MainForceAlertCreate,
    auth: Auth = Depends(AllUserAuth()),
):
    alert = await crud.MainForceAlertDal(auth.db).create_alert(
        user_id=auth.user.id,
        data=data,
    )
    return SuccessResponse(alert)


@router.put("/alerts/{alert_id}/read", summary="标记预警已读")
async def mark_alert_read(
    alert_id: int,
    auth: Auth = Depends(AllUserAuth()),
):
    success = await crud.MainForceAlertDal(auth.db).mark_as_read(
        alert_id=alert_id,
        user_id=auth.user.id,
    )
    return SuccessResponse("已标记已读" if success else "预警不存在")


@router.post("/sync/stock/{stock_code}", summary="同步股票主力数据")
async def sync_stock_mainforce_data(
    stock_code: str,
    auth: Auth = Depends(AllUserAuth()),
):
    service = FundDataSyncService(auth.db)
    result = await service.sync_stock_fund_holders(stock_code)
    return SuccessResponse(result)


@router.post("/sync/fund/{fund_code}", summary="同步基金持仓数据")
async def sync_fund_portfolio_data(
    fund_code: str,
    report_date: str | None = None,
    auth: Auth = Depends(AllUserAuth()),
):
    service = FundDataSyncService(auth.db)
    result = await service.sync_fund_portfolio(fund_code, report_date)
    return SuccessResponse(result)


@router.post("/sync/companies", summary="同步基金公司列表")
async def sync_fund_companies_data(
    auth: Auth = Depends(AllUserAuth()),
):
    service = FundDataSyncService(auth.db)
    result = await service.sync_fund_companies()
    return SuccessResponse(result)
