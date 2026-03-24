# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/03/22
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 复盘功能接口文件

from datetime import date
from fastapi import APIRouter, Depends, Body, Query
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, Auth
from . import schemas, crud
from core.dependencies import IdList


router = APIRouter()


###########################################################
#    复盘记录管理
###########################################################


@router.post("/reviews", summary="创建复盘记录")
async def create_review(
    data: schemas.ReviewCreate, auth: Auth = Depends(AllUserAuth())
):
    review = await crud.ReviewDal(auth.db).create_data(data=data, user_id=auth.user.id)
    return SuccessResponse(review)


@router.get("/reviews", summary="获取复盘记录列表")
async def get_review_list(
    review_type: str | None = None,
    portfolio_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    page: int = 1,
    limit: int = 10,
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.ReviewDal(auth.db)

    if start_date and end_date:
        datas = await dal.get_by_date_range(
            user_id=auth.user.id,
            start_date=start_date,
            end_date=end_date,
            review_type=review_type,
        )
        return SuccessResponse(datas, count=len(datas))
    elif portfolio_id:
        datas = await dal.get_by_portfolio_id(portfolio_id)
        return SuccessResponse(datas, count=len(datas))
    else:
        datas, count = await dal.get_datas(
            page=page,
            limit=limit,
            user_id=auth.user.id,
            review_type=review_type,
            v_schema=schemas.ReviewOut,
            v_return_count=True,
        )
        return SuccessResponse(datas, count=count)


@router.get("/reviews/{review_id}", summary="获取复盘记录详情")
async def get_review_detail(review_id: int, auth: Auth = Depends(AllUserAuth())):
    data = await crud.ReviewDal(auth.db).get_data(review_id)
    if data.user_id != auth.user.id and not auth.user.is_staff:
        return SuccessResponse(None)
    return SuccessResponse(data)


@router.put("/reviews/{review_id}", summary="更新复盘记录")
async def update_review(
    review_id: int, data: schemas.ReviewUpdate, auth: Auth = Depends(AllUserAuth())
):
    existing = await crud.ReviewDal(auth.db).get_data(review_id)
    if existing.user_id != auth.user.id and not auth.user.is_staff:
        return SuccessResponse("无权限操作")
    review = await crud.ReviewDal(auth.db).put_data(review_id, data)
    return SuccessResponse(review)


@router.delete("/reviews", summary="批量删除复盘记录")
async def delete_reviews(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    if not auth.user.is_staff:
        for data_id in ids.ids:
            data = await crud.ReviewDal(auth.db).get_data(data_id)
            if data.user_id != auth.user.id:
                return SuccessResponse("无权限删除其他用户的数据")
    await crud.ReviewDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


###########################################################
#    心得经验管理
###########################################################


@router.post("/experiences", summary="创建心得经验")
async def create_experience(
    data: schemas.ExperienceCreate, auth: Auth = Depends(AllUserAuth())
):
    experience = await crud.ExperienceDal(auth.db).create_data(
        data=data, user_id=auth.user.id
    )
    return SuccessResponse(experience)


@router.get("/experiences", summary="获取心得经验列表")
async def get_experience_list(
    category: str | None = None,
    tags: str | None = Query(None, description="逗号分隔的标签"),
    keyword: str | None = None,
    page: int = 1,
    limit: int = 10,
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.ExperienceDal(auth.db)

    if keyword:
        datas = await dal.search_content(user_id=auth.user.id, keyword=keyword)
        return SuccessResponse(datas, count=len(datas))
    elif category:
        datas = await dal.get_by_category(user_id=auth.user.id, category=category)
        return SuccessResponse(datas, count=len(datas))
    elif tags:
        tag_list = [t.strip() for t in tags.split(",")]
        datas = await dal.get_by_tags(user_id=auth.user.id, tags=tag_list)
        return SuccessResponse(datas, count=len(datas))
    else:
        datas, count = await dal.get_datas(
            page=page,
            limit=limit,
            user_id=auth.user.id,
            v_schema=schemas.ExperienceOut,
            v_return_count=True,
        )
        return SuccessResponse(datas, count=count)


@router.get("/experiences/{experience_id}", summary="获取心得经验详情")
async def get_experience_detail(
    experience_id: int, auth: Auth = Depends(AllUserAuth())
):
    dal = crud.ExperienceDal(auth.db)
    data = await dal.get_data(experience_id)
    if data.user_id != auth.user.id and not auth.user.is_staff:
        return SuccessResponse(None)
    await dal.increment_view_count(experience_id)
    return SuccessResponse(dal._format_output(data))


@router.put("/experiences/{experience_id}", summary="更新心得经验")
async def update_experience(
    experience_id: int,
    data: schemas.ExperienceUpdate,
    auth: Auth = Depends(AllUserAuth()),
):
    existing = await crud.ExperienceDal(auth.db).get_data(experience_id)
    if existing.user_id != auth.user.id and not auth.user.is_staff:
        return SuccessResponse("无权限操作")
    experience = await crud.ExperienceDal(auth.db).put_data(experience_id, data)
    return SuccessResponse(experience)


@router.delete("/experiences", summary="批量删除心得经验")
async def delete_experiences(
    ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())
):
    if not auth.user.is_staff:
        for data_id in ids.ids:
            data = await crud.ExperienceDal(auth.db).get_data(data_id)
            if data.user_id != auth.user.id:
                return SuccessResponse("无权限删除其他用户的数据")
    await crud.ExperienceDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


###########################################################
#    雷区基线规则管理
###########################################################


@router.post("/rules", summary="创建规则")
async def create_rule(data: schemas.RuleCreate, auth: Auth = Depends(AllUserAuth())):
    rule = await crud.RuleDal(auth.db).create_data(data=data, user_id=auth.user.id)
    return SuccessResponse(rule)


@router.get("/rules", summary="获取规则列表")
async def get_rule_list(
    rule_type: str | None = None,
    is_active: int | None = None,
    page: int = 1,
    limit: int = 10,
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.RuleDal(auth.db)

    if is_active == 1:
        datas = await dal.get_active_rules(user_id=auth.user.id, rule_type=rule_type)
        return SuccessResponse(datas, count=len(datas))

    datas, count = await dal.get_datas(
        page=page,
        limit=limit,
        user_id=auth.user.id,
        rule_type=rule_type,
        v_schema=schemas.RuleOut,
        v_return_count=True,
    )
    return SuccessResponse(datas, count=count)


@router.get("/rules/{rule_id}", summary="获取规则详情")
async def get_rule_detail(rule_id: int, auth: Auth = Depends(AllUserAuth())):
    data = await crud.RuleDal(auth.db).get_data(rule_id)
    if data.user_id != auth.user.id and not auth.user.is_staff:
        return SuccessResponse(None)
    return SuccessResponse(data)


@router.put("/rules/{rule_id}", summary="更新规则")
async def update_rule(
    rule_id: int, data: schemas.RuleUpdate, auth: Auth = Depends(AllUserAuth())
):
    existing = await crud.RuleDal(auth.db).get_data(rule_id)
    if existing.user_id != auth.user.id and not auth.user.is_staff:
        return SuccessResponse("无权限操作")
    rule = await crud.RuleDal(auth.db).put_data(rule_id, data)
    return SuccessResponse(rule)


@router.put("/rules/{rule_id}/active", summary="更新规则启用状态")
async def update_rule_active(
    rule_id: int,
    is_active: int = Body(..., embed=True),
    auth: Auth = Depends(AllUserAuth()),
):
    existing = await crud.RuleDal(auth.db).get_data(rule_id)
    if existing.user_id != auth.user.id and not auth.user.is_staff:
        return SuccessResponse("无权限操作")
    await crud.RuleDal(auth.db).update_active_status(rule_id, is_active)
    return SuccessResponse("更新成功")


@router.delete("/rules", summary="批量删除规则")
async def delete_rules(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    if not auth.user.is_staff:
        for data_id in ids.ids:
            data = await crud.RuleDal(auth.db).get_data(data_id)
            if data.user_id != auth.user.id:
                return SuccessResponse("无权限删除其他用户的数据")
    await crud.RuleDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


###########################################################
#    违规记录管理
###########################################################


@router.get("/violations", summary="获取违规记录列表")
async def get_violation_list(
    rule_id: int | None = None,
    days: int | None = None,
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.ViolationDal(auth.db)

    if rule_id:
        datas = await dal.get_by_rule_id(rule_id)
    elif days:
        datas = await dal.get_recent_violations(user_id=auth.user.id, days=days)
    else:
        datas = await dal.get_by_user_id(user_id=auth.user.id)

    return SuccessResponse(datas, count=len(datas))


@router.post("/violations", summary="创建违规记录")
async def create_violation(
    rule_id: int = Body(...),
    violation_context: dict | None = Body(None),
    related_stock_code: str | None = Body(None),
    related_trade_id: int | None = Body(None),
    user_note: str | None = Body(None),
    auth: Auth = Depends(AllUserAuth()),
):
    from datetime import datetime

    violation = await crud.ViolationDal(auth.db).create_violation(
        user_id=auth.user.id,
        rule_id=rule_id,
        violation_time=datetime.now(),
        violation_context=violation_context,
        related_stock_code=related_stock_code,
        related_trade_id=related_trade_id,
        user_note=user_note,
    )
    return SuccessResponse(violation)
