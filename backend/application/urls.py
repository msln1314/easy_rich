# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/19 15:47
# @File           : urls.py
# @IDE            : PyCharm
# @desc           : 路由文件

from fastapi import APIRouter, Depends
from apps.admin.auth.login import app as auth_router
from apps.admin.system.api import router as system_router
from apps.admin.iot.api import router as iot_router
from apps.admin.log.api import router as log_router
from apps.admin.workplace.views import app as workplace_router
from apps.admin.analysis.views import app as analysis_router
from apps.admin.help.views import app as help_router
from apps.admin.resource.views import app as resource_router
from apps.admin.stock.api import router as stock_router
from apps.admin.notification.views import router as notification_router
# 引入应用中的路由
urlpatterns = [
    {"ApiRouter": auth_router, "prefix": "/auth", "tags": ["系统认证"]},
    {"ApiRouter": system_router, "prefix": "/system", "tags": ["系统管理"]},
    {"ApiRouter": iot_router, "prefix": "/iot", "tags": ["IOT管理"]},
    {"ApiRouter": log_router, "prefix": "/logs", "tags": ["日志管理"]},
    {"ApiRouter": workplace_router, "prefix": "/workplace", "tags": ["工作区管理"]},
    {"ApiRouter": analysis_router, "prefix": "/analysis", "tags": ["数据分析管理"]},
    {"ApiRouter": help_router, "prefix": "/help", "tags": ["帮助中心管理"]},
    {"ApiRouter": resource_router, "prefix": "/resource", "tags": ["资源管理"]},
    {"ApiRouter": stock_router, "prefix": "/stock", "tags": ["股票管理"]},
    {"ApiRouter": notification_router, "prefix": "/notification", "tags": ["通知管理"]},
]
api_router = APIRouter()
for url in urlpatterns:
    api_router.include_router(url["ApiRouter"], prefix=url["prefix"], tags=url["tags"])



