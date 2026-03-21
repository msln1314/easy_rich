from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from utils.response import SuccessResponse, ErrorResponse
from apps.admin.auth.utils.current import AllUserAuth, Auth
from . import schemas, crud
from .services import CalendarDataSyncService, AIAnalysisService

router = APIRouter()


@router.get("/events", summary="获取事件列表")
async def get_events(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    stock_code: Optional[str] = None,
    event_type: Optional[str] = None,
    is_watchlist: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.StockCalendarEventDal(auth.db)
    total, items = await dal.get_list(
        start_date=start_date,
        end_date=end_date,
        stock_code=stock_code,
        event_type=event_type,
        is_watchlist=is_watchlist,
        page=page,
        page_size=page_size,
    )
    datas = [
        schemas.StockCalendarEventOut.model_validate(i).model_dump() for i in items
    ]
    return SuccessResponse(datas, count=total)


@router.get("/events/{event_id}", summary="获取事件详情")
async def get_event(event_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.StockCalendarEventDal(auth.db)
    event = await dal.get_data(event_id)
    if not event:
        return ErrorResponse("事件不存在")
    return SuccessResponse(
        schemas.StockCalendarEventOut.model_validate(event).model_dump()
    )


@router.get("/events/by_stock/{stock_code}", summary="获取某股票的所有事件")
async def get_events_by_stock(
    stock_code: str,
    days: int = Query(90, ge=1, le=365),
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.StockCalendarEventDal(auth.db)
    items = await dal.get_by_stock(stock_code, days)
    datas = [
        schemas.StockCalendarEventOut.model_validate(i).model_dump() for i in items
    ]
    return SuccessResponse(datas, count=len(datas))


@router.get("/events/by_date/{event_date}", summary="获取某日期的所有事件")
async def get_events_by_date(event_date: date, auth: Auth = Depends(AllUserAuth())):
    dal = crud.StockCalendarEventDal(auth.db)
    items = await dal.get_by_date(event_date)
    datas = [
        schemas.StockCalendarEventOut.model_validate(i).model_dump() for i in items
    ]
    return SuccessResponse(datas, count=len(datas))


@router.post("/events", summary="添加自定义事件")
async def create_event(
    data: schemas.StockCalendarEventCreate, auth: Auth = Depends(AllUserAuth())
):
    dal = crud.StockCalendarEventDal(auth.db)
    event = await dal.create_event(data)
    return SuccessResponse(
        schemas.StockCalendarEventOut.model_validate(event).model_dump()
    )


@router.get("/reminders", summary="获取用户提醒列表")
async def get_reminders(
    user_id: int = Query(..., description="用户ID"),
    is_active: Optional[int] = None,
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.StockEventReminderDal(auth.db)
    items = await dal.get_list_by_user(user_id, is_active)
    datas = [
        schemas.StockEventReminderOut.model_validate(i).model_dump() for i in items
    ]
    return SuccessResponse(datas, count=len(datas))


@router.post("/reminders", summary="创建提醒")
async def create_reminder(
    data: schemas.StockEventReminderCreate, auth: Auth = Depends(AllUserAuth())
):
    dal = crud.StockEventReminderDal(auth.db)
    reminder = await dal.create_reminder(data)
    return SuccessResponse(
        schemas.StockEventReminderOut.model_validate(reminder).model_dump()
    )


@router.put("/reminders/{reminder_id}", summary="更新提醒")
async def update_reminder(
    reminder_id: int,
    data: schemas.StockEventReminderUpdate,
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.StockEventReminderDal(auth.db)
    reminder = await dal.put_data(reminder_id, data)
    return SuccessResponse(
        schemas.StockEventReminderOut.model_validate(reminder).model_dump()
    )


@router.delete("/reminders/{reminder_id}", summary="删除提醒")
async def delete_reminder(reminder_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.StockEventReminderDal(auth.db)
    await dal.delete_datas([reminder_id], v_soft=False)
    return SuccessResponse("删除成功")


@router.post("/sync/earnings", summary="同步财报日历")
async def sync_earnings(auth: Auth = Depends(AllUserAuth())):
    service = CalendarDataSyncService(auth.db)
    count = await service.sync_earnings_calendar()
    return SuccessResponse(
        {"message": f"同步成功，新增 {count} 条记录", "count": count}
    )


@router.post("/sync/dividends", summary="同步分红除权")
async def sync_dividends(auth: Auth = Depends(AllUserAuth())):
    service = CalendarDataSyncService(auth.db)
    count = await service.sync_dividend_calendar()
    return SuccessResponse(
        {"message": f"同步成功，新增 {count} 条记录", "count": count}
    )


@router.post("/sync/unlocks", summary="同步解禁日")
async def sync_unlocks(auth: Auth = Depends(AllUserAuth())):
    service = CalendarDataSyncService(auth.db)
    count = await service.sync_unlock_calendar()
    return SuccessResponse(
        {"message": f"同步成功，新增 {count} 条记录", "count": count}
    )


@router.post("/sync/all", summary="全量同步")
async def sync_all(auth: Auth = Depends(AllUserAuth())):
    service = CalendarDataSyncService(auth.db)
    results = await service.sync_all()
    return SuccessResponse(results)


@router.post("/analysis/event/{event_id}", summary="AI分析单个事件")
async def analyze_event(event_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.StockCalendarEventDal(auth.db)
    event = await dal.get_data(event_id)
    if not event:
        return ErrorResponse("事件不存在")

    service = AIAnalysisService(auth.db)
    result = await service.analyze_event(event)
    return SuccessResponse(result)


@router.post("/analysis/stock/{stock_code}", summary="AI分析股票近期事件")
async def analyze_stock_events(
    stock_code: str,
    days: int = Query(30, ge=1, le=90),
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.StockCalendarEventDal(auth.db)
    items = await dal.get_by_stock(stock_code, days)

    if not items:
        return ErrorResponse(f"未找到股票 {stock_code} 的近期事件")

    service = AIAnalysisService(auth.db)
    results = []
    for event in items[:5]:
        result = await service.analyze_event(event)
        results.append(
            {
                "event_id": event.id,
                "title": event.title,
                "event_date": str(event.event_date),
                "analysis": result,
            }
        )

    return SuccessResponse(results)
