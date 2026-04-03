# -*- coding: utf-8 -*-
"""通知模块 Schemas"""
from .channel import (
    NotificationChannelCreate,
    NotificationChannelUpdate,
    NotificationChannelOut,
)
from .template import (
    NotificationTemplateCreate,
    NotificationTemplateUpdate,
    NotificationTemplateOut,
)
from .notification import (
    NotificationLogOut,
    SystemNotificationOut,
    SystemNotificationListOut,
    NotificationSendRequest,
    NotificationTestRequest,
)

__all__ = [
    "NotificationChannelCreate",
    "NotificationChannelUpdate",
    "NotificationChannelOut",
    "NotificationTemplateCreate",
    "NotificationTemplateUpdate",
    "NotificationTemplateOut",
    "NotificationLogOut",
    "SystemNotificationOut",
    "SystemNotificationListOut",
    "NotificationSendRequest",
    "NotificationTestRequest",
]