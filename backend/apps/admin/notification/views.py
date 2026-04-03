# -*- coding: utf-8 -*-
"""通知模块 API 接口"""
from datetime import date
from typing import Optional, List
import json

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from utils.response import SuccessResponse, ErrorResponse
from apps.admin.auth.utils.current import AllUserAuth, Auth
from core.database import get_db
from . import schemas, crud
from .services import NotificationService, NotificationRuleService
from .params import (
    NotificationRuleCreate,
    NotificationRuleUpdate,
    NotificationRuleOut,
    NotificationRuleListOut,
)

router = APIRouter()


# ==================== 通知渠道管理 ====================

@router.get("/channels", summary="获取通知渠道列表")
async def get_channels(
    channel_type: Optional[str] = None,
    auth: Auth = Depends(AllUserAuth())
):
    """获取当前用户的通知渠道列表"""
    dal = crud.NotificationChannelDal(auth.db)
    channels = await dal.get_user_channels(
        user_id=auth.user.id,
        channel_type=channel_type
    )
    datas = [
        schemas.NotificationChannelOut.model_validate(c).model_dump()
        for c in channels
    ]
    return SuccessResponse(datas)


@router.post("/channels", summary="创建通知渠道")
async def create_channel(
    data: schemas.NotificationChannelCreate,
    auth: Auth = Depends(AllUserAuth())
):
    """创建通知渠道"""
    service = NotificationService(auth.db)
    channel = await service.create_channel(
        user_id=auth.user.id,
        channel_type=data.channel_type,
        channel_name=data.channel_name,
        channel_config=data.channel_config,
    )
    return SuccessResponse(
        schemas.NotificationChannelOut.model_validate(channel).model_dump()
    )


@router.put("/channels/{channel_id}", summary="更新通知渠道")
async def update_channel(
    channel_id: int,
    data: schemas.NotificationChannelUpdate,
    auth: Auth = Depends(AllUserAuth())
):
    """更新通知渠道"""
    dal = crud.NotificationChannelDal(auth.db)
    channel = await dal.get_data(channel_id)

    if channel.user_id != auth.user.id:
        return ErrorResponse("无权操作此渠道")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(channel, key, value)

    await auth.db.flush()
    return SuccessResponse(
        schemas.NotificationChannelOut.model_validate(channel).model_dump()
    )


@router.delete("/channels/{channel_id}", summary="删除通知渠道")
async def delete_channel(
    channel_id: int,
    auth: Auth = Depends(AllUserAuth())
):
    """删除通知渠道"""
    dal = crud.NotificationChannelDal(auth.db)
    channel = await dal.get_data(channel_id)

    if channel.user_id != auth.user.id:
        return ErrorResponse("无权操作此渠道")

    await dal.delete_datas([channel_id], v_soft=True)
    return SuccessResponse("删除成功")


@router.post("/channels/{channel_id}/verify", summary="验证通知渠道")
async def verify_channel(
    channel_id: int,
    data: schemas.ChannelVerifyRequest,
    auth: Auth = Depends(AllUserAuth())
):
    """验证通知渠道"""
    dal = crud.NotificationChannelDal(auth.db)
    channel = await dal.get_data(channel_id)

    if channel.user_id != auth.user.id:
        return ErrorResponse("无权操作此渠道")

    service = NotificationService(auth.db)
    success = await service.verify_channel(channel, data.code)

    if success:
        return SuccessResponse("验证成功")
    else:
        return ErrorResponse("验证码错误")


@router.post("/channels/{channel_id}/send-code", summary="发送验证码")
async def send_verify_code(
    channel_id: int,
    auth: Auth = Depends(AllUserAuth())
):
    """发送验证码到渠道"""
    dal = crud.NotificationChannelDal(auth.db)
    channel = await dal.get_data(channel_id)

    if channel.user_id != auth.user.id:
        return ErrorResponse("无权操作此渠道")

    service = NotificationService(auth.db)
    code = await service.generate_verify_code(channel)

    # 如果是邮箱渠道，发送验证码邮件
    if channel.channel_type == "email":
        config = channel.channel_config or {}
        if isinstance(config, str):
            config = json.loads(config)

        from .services.senders import EmailSender
        sender = EmailSender()
        result = await sender.send(
            user_id=auth.user.id,
            title="通知渠道验证码",
            content=f"您的验证码是: {code}，有效期30分钟。",
            config=config,
        )
        if not result.get("success"):
            return ErrorResponse(f"验证码发送失败: {result.get('error_msg')}")

    return SuccessResponse({"message": "验证码已发送"})


@router.post("/channels/{channel_id}/test", summary="测试发送")
async def test_channel(
    channel_id: int,
    data: schemas.ChannelTestRequest,
    auth: Auth = Depends(AllUserAuth())
):
    """测试发送通知"""
    dal = crud.NotificationChannelDal(auth.db)
    channel = await dal.get_data(channel_id)

    if channel.user_id != auth.user.id:
        return ErrorResponse("无权操作此渠道")

    service = NotificationService(auth.db)
    result = await service.test_channel(channel, data.title, data.content)

    if result.get("success"):
        return SuccessResponse("测试发送成功")
    else:
        return ErrorResponse(f"发送失败: {result.get('error_msg')}")


# ==================== 系统通知 ====================

@router.get("/list", summary="获取系统通知列表")
async def get_notifications(
    is_read: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    auth: Auth = Depends(AllUserAuth())
):
    """获取用户的系统通知列表"""
    dal = crud.SystemNotificationDal(auth.db)
    total, items = await dal.get_user_notifications(
        user_id=auth.user.id,
        is_read=is_read,
        page=page,
        page_size=page_size
    )

    unread_count = await dal.get_unread_count(auth.user.id)

    datas = [
        schemas.SystemNotificationOut.model_validate(i).model_dump()
        for i in items
    ]

    return SuccessResponse({
        "total": total,
        "items": datas,
        "unread_count": unread_count,
    })


@router.get("/unread-count", summary="获取未读数量")
async def get_unread_count(auth: Auth = Depends(AllUserAuth())):
    """获取未读通知数量"""
    dal = crud.SystemNotificationDal(auth.db)
    count = await dal.get_unread_count(auth.user.id)
    return SuccessResponse({"unread_count": count})


@router.put("/{notification_id}/read", summary="标记已读")
async def mark_as_read(
    notification_id: int,
    auth: Auth = Depends(AllUserAuth())
):
    """标记通知为已读"""
    dal = crud.SystemNotificationDal(auth.db)
    success = await dal.mark_as_read(notification_id, auth.user.id)

    if success:
        return SuccessResponse("已标记为已读")
    else:
        return ErrorResponse("通知不存在或无权操作")


@router.put("/read-all", summary="全部标记已读")
async def mark_all_as_read(auth: Auth = Depends(AllUserAuth())):
    """标记全部通知为已读"""
    dal = crud.SystemNotificationDal(auth.db)
    count = await dal.mark_all_as_read(auth.user.id)
    return SuccessResponse({"message": f"已标记 {count} 条通知为已读"})


# ==================== 通知发送 ====================

@router.post("/send", summary="发送通知")
async def send_notification(
    data: schemas.NotificationSendRequest,
    auth: Auth = Depends(AllUserAuth())
):
    """发送通知"""
    service = NotificationService(auth.db)
    result = await service.send_notification(
        user_id=data.user_id,
        title=data.title,
        content=data.content,
        channels=data.channels,
        template_code=data.template_code,
        extra_data=data.extra_data,
    )

    if result.get("success"):
        return SuccessResponse(result)
    else:
        return ErrorResponse(result.get("error", "发送失败"), data=result)


# ==================== 通知规则 ====================

@router.get("/rules", summary="获取通知规则列表")
async def get_rules(
    rule_type: Optional[str] = None,
    auth: Auth = Depends(AllUserAuth())
):
    """获取用户的通知规则列表"""
    service = NotificationRuleService(auth.db)
    rules = await service.get_user_rules(
        user_id=auth.user.id,
        rule_type=rule_type,
        enabled_only=False
    )

    # 解析 JSON 字段
    items = []
    for rule in rules:
        rule_dict = {
            "id": rule.id,
            "user_id": rule.user_id,
            "rule_name": rule.rule_name,
            "rule_type": rule.rule_type,
            "event_type_filter": rule.event_type_filter,
            "stock_codes": json.loads(rule.stock_codes) if rule.stock_codes else None,
            "condition_config": json.loads(rule.condition_config) if isinstance(rule.condition_config, str) else rule.condition_config,
            "action_config": json.loads(rule.action_config) if isinstance(rule.action_config, str) else rule.action_config,
            "priority": rule.priority,
            "is_enabled": rule.is_enabled,
            "valid_from": str(rule.valid_from) if rule.valid_from else None,
            "valid_to": str(rule.valid_to) if rule.valid_to else None,
            "last_triggered_at": rule.last_triggered_at,
            "created_at": str(rule.created_at),
            "updated_at": str(rule.updated_at),
        }
        items.append(rule_dict)

    return SuccessResponse({"total": len(items), "items": items})


@router.post("/rules", summary="创建通知规则")
async def create_rule(
    data: NotificationRuleCreate,
    auth: Auth = Depends(AllUserAuth())
):
    """创建通知规则"""
    service = NotificationRuleService(auth.db)

    valid_from = None
    if data.valid_from:
        valid_from = date.fromisoformat(data.valid_from)

    valid_to = None
    if data.valid_to:
        valid_to = date.fromisoformat(data.valid_to)

    rule = await service.create_rule(
        user_id=auth.user.id,
        rule_name=data.rule_name,
        rule_type=data.rule_type,
        condition_config=data.condition_config,
        action_config=data.action_config,
        event_type_filter=data.event_type_filter,
        stock_codes=data.stock_codes,
        priority=data.priority,
        valid_from=valid_from,
        valid_to=valid_to,
    )

    return SuccessResponse({
        "id": rule.id,
        "rule_name": rule.rule_name,
        "rule_type": rule.rule_type,
    })


@router.put("/rules/{rule_id}", summary="更新通知规则")
async def update_rule(
    rule_id: int,
    data: NotificationRuleUpdate,
    auth: Auth = Depends(AllUserAuth())
):
    """更新通知规则"""
    from .models.notification_rule import NotificationRule

    dal = crud.NotificationChannelDal(auth.db)
    dal.model = NotificationRule

    rule = await dal.get_data(rule_id)

    if rule.user_id != auth.user.id:
        return ErrorResponse("无权操作此规则")

    update_data = data.model_dump(exclude_unset=True)

    # 处理日期字段
    if "valid_from" in update_data and update_data["valid_from"]:
        update_data["valid_from"] = date.fromisoformat(update_data["valid_from"])
    if "valid_to" in update_data and update_data["valid_to"]:
        update_data["valid_to"] = date.fromisoformat(update_data["valid_to"])

    # 处理 JSON 字段
    if "stock_codes" in update_data and update_data["stock_codes"]:
        update_data["stock_codes"] = json.dumps(update_data["stock_codes"])

    for key, value in update_data.items():
        setattr(rule, key, value)

    await auth.db.flush()
    return SuccessResponse("更新成功")


@router.delete("/rules/{rule_id}", summary="删除通知规则")
async def delete_rule(
    rule_id: int,
    auth: Auth = Depends(AllUserAuth())
):
    """删除通知规则"""
    from .models.notification_rule import NotificationRule

    dal = crud.NotificationChannelDal(auth.db)
    dal.model = NotificationRule

    rule = await dal.get_data(rule_id)

    if rule.user_id != auth.user.id:
        return ErrorResponse("无权操作此规则")

    await dal.delete_datas([rule_id], v_soft=True)
    return SuccessResponse("删除成功")


@router.post("/rules/check", summary="检查规则并发送通知")
async def check_rules(
    target_date: Optional[str] = None,
    auth: Auth = Depends(AllUserAuth())
):
    """检查通知规则并发送提醒（管理员接口）"""
    service = NotificationRuleService(auth.db)

    check_date = None
    if target_date:
        check_date = date.fromisoformat(target_date)

    result = await service.check_rules_for_date(check_date)
    return SuccessResponse(result)