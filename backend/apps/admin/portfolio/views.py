from datetime import date
from fastapi import APIRouter, Depends, Query
from utils.response import SuccessResponse, ErrorResponse
from apps.admin.auth.utils.current import AllUserAuth, Auth
from . import schemas, crud
from .services import TradeService, PositionService, AnalysisService, RiskService

router = APIRouter()


@router.get("", summary="获取用户组合列表")
async def get_portfolios(auth: Auth = Depends(AllUserAuth())):
    dal = crud.PortfolioDal(auth.db)
    items = await dal.get_list_by_user(auth.user.id)
    datas = [schemas.PortfolioOut.model_validate(i).model_dump() for i in items]
    return SuccessResponse(datas, count=len(datas))


@router.get("/{portfolio_id}", summary="获取组合详情")
async def get_portfolio(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PortfolioDal(auth.db)
    portfolio = await dal.get_data(portfolio_id, v_return_none=True)
    if not portfolio:
        return ErrorResponse("组合不存在")
    return SuccessResponse(schemas.PortfolioOut.model_validate(portfolio).model_dump())


@router.post("", summary="创建组合")
async def create_portfolio(
    data: schemas.PortfolioCreate, auth: Auth = Depends(AllUserAuth())
):
    dal = crud.PortfolioDal(auth.db)
    portfolio = await dal.create_portfolio(data, auth.user.id)
    return SuccessResponse(schemas.PortfolioOut.model_validate(portfolio).model_dump())


@router.put("/{portfolio_id}", summary="更新组合")
async def update_portfolio(
    portfolio_id: int,
    data: schemas.PortfolioUpdate,
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.PortfolioDal(auth.db)
    portfolio = await dal.put_data(portfolio_id, data)
    return SuccessResponse(schemas.PortfolioOut.model_validate(portfolio).model_dump())


@router.delete("/{portfolio_id}", summary="删除组合")
async def delete_portfolio(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PortfolioDal(auth.db)
    await dal.delete_datas([portfolio_id], v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{portfolio_id}/default", summary="设置为默认组合")
async def set_default_portfolio(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PortfolioDal(auth.db)
    await dal.set_default(portfolio_id, auth.user.id)
    return SuccessResponse("设置成功")


@router.get("/position/{portfolio_id}", summary="获取持仓列表")
async def get_positions(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PositionDal(auth.db)
    items = await dal.get_by_portfolio(portfolio_id)
    datas = [schemas.PositionOut.model_validate(i).model_dump() for i in items]
    return SuccessResponse(datas, count=len(datas))


@router.post("/position/{portfolio_id}", summary="添加持仓")
async def add_position(
    portfolio_id: int, data: schemas.PositionCreate, auth: Auth = Depends(AllUserAuth())
):
    dal = crud.PositionDal(auth.db)
    position = await dal.add_position(portfolio_id, data)
    return SuccessResponse(schemas.PositionOut.model_validate(position).model_dump())


@router.delete("/position/{portfolio_id}/{stock_code}", summary="删除持仓")
async def delete_position(
    portfolio_id: int, stock_code: str, auth: Auth = Depends(AllUserAuth())
):
    dal = crud.PositionDal(auth.db)
    position = await dal.get_by_stock(portfolio_id, stock_code)
    if position:
        await dal.delete_datas([position.id], v_soft=False)
    return SuccessResponse("删除成功")


@router.get("/trade/{portfolio_id}", summary="获取交易记录")
async def get_trades(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.TradeDal(auth.db)
    items = await dal.get_by_portfolio(portfolio_id)
    datas = [schemas.TradeOut.model_validate(i).model_dump() for i in items]
    return SuccessResponse(datas, count=len(datas))


@router.post("/trade/{portfolio_id}/buy", summary="记录买入")
async def record_buy(
    portfolio_id: int, data: schemas.TradeBuy, auth: Auth = Depends(AllUserAuth())
):
    service = TradeService(auth.db)
    try:
        trade = await service.execute_buy(
            portfolio_id=portfolio_id,
            stock_code=data.stock_code,
            stock_name=data.stock_name,
            shares=data.shares,
            price=data.price,
            trade_date=data.trade_date,
            commission=data.commission,
            remark=data.remark,
        )
        return SuccessResponse(schemas.TradeOut.model_validate(trade).model_dump())
    except Exception as e:
        return ErrorResponse(str(e))


@router.post("/trade/{portfolio_id}/sell", summary="记录卖出")
async def record_sell(
    portfolio_id: int, data: schemas.TradeSell, auth: Auth = Depends(AllUserAuth())
):
    service = TradeService(auth.db)
    try:
        trade = await service.execute_sell(
            portfolio_id=portfolio_id,
            stock_code=data.stock_code,
            shares=data.shares,
            price=data.price,
            trade_date=data.trade_date,
            commission=data.commission,
            stamp_duty=data.stamp_duty,
            remark=data.remark,
        )
        return SuccessResponse(schemas.TradeOut.model_validate(trade).model_dump())
    except Exception as e:
        return ErrorResponse(str(e))


@router.get("/analysis/{portfolio_id}/performance", summary="获取组合业绩")
async def get_performance(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    service = AnalysisService(auth.db)
    result = await service.get_portfolio_performance(portfolio_id)
    return SuccessResponse(result)


@router.get("/analysis/{portfolio_id}/positions", summary="获取持仓分析")
async def get_position_analysis(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    service = AnalysisService(auth.db)
    result = await service.get_position_analysis(portfolio_id)
    return SuccessResponse(result)


@router.get("/analysis/{portfolio_id}/trades", summary="获取交易统计")
async def get_trade_stats(
    portfolio_id: int,
    days: int = Query(30, ge=1, le=365),
    auth: Auth = Depends(AllUserAuth()),
):
    service = AnalysisService(auth.db)
    result = await service.get_trade_statistics(portfolio_id, days)
    return SuccessResponse(result)


@router.get("/analysis/{portfolio_id}/attribution", summary="获取收益归因")
async def get_profit_attribution(
    portfolio_id: int, auth: Auth = Depends(AllUserAuth())
):
    service = AnalysisService(auth.db)
    result = await service.get_profit_attribution(portfolio_id)
    return SuccessResponse(result)


@router.post("/analysis/{portfolio_id}/snapshot", summary="生成组合快照")
async def create_snapshot(
    portfolio_id: int,
    snapshot_date: date = None,
    auth: Auth = Depends(AllUserAuth()),
):
    service = AnalysisService(auth.db)
    if not snapshot_date:
        snapshot_date = date.today()
    result = await service.generate_snapshot(portfolio_id, snapshot_date)
    return SuccessResponse({"id": result.id, "date": str(result.snapshot_date)})


@router.get("/risk/{portfolio_id}/alerts", summary="获取风控预警")
async def get_risk_alerts(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    service = RiskService(auth.db)
    result = await service.get_active_alerts(portfolio_id)
    return SuccessResponse(result, count=len(result))


@router.post("/risk/{portfolio_id}/check", summary="风控检查")
async def risk_check(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    service = RiskService(auth.db)
    alerts = await service.generate_risk_alerts(portfolio_id)
    return SuccessResponse({"generated_alerts": len(alerts)})


@router.get("/risk/{portfolio_id}/drawdown", summary="回撤检查")
async def check_drawdown(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    service = RiskService(auth.db)
    result = await service.check_drawdown(portfolio_id)
    return SuccessResponse(result)


@router.get("/risk/{portfolio_id}/rebalance", summary="再平衡建议")
async def check_rebalance(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    service = RiskService(auth.db)
    result = await service.check_rebalance_needed(portfolio_id)
    return SuccessResponse(result)


@router.post("/risk/{portfolio_id}/pre_check", summary="交易前风控检查")
async def pre_trade_check(
    portfolio_id: int,
    stock_code: str,
    trade_type: str,
    amount: float,
    auth: Auth = Depends(AllUserAuth()),
):
    service = RiskService(auth.db)
    result = await service.pre_trade_risk_check(
        portfolio_id, stock_code, trade_type, amount
    )
    return SuccessResponse(result)


@router.put("/risk/alert/{alert_id}/handle", summary="处理预警")
async def handle_alert(
    alert_id: int,
    handle_note: str = None,
    auth: Auth = Depends(AllUserAuth()),
):
    service = RiskService(auth.db)
    result = await service.handle_alert(alert_id, handle_note)
    if result:
        return SuccessResponse("处理成功")
    return ErrorResponse("预警不存在")
