#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:18
# @File           : login_log.py
# @IDE            : PyCharm
# @desc           : 登录日志数据库操作

import random
import json
from sqlalchemy.ext.asyncio import AsyncSession
from .. import models, schemas
from core.crud import DalBase
from fastapi import Request
from starlette.requests import Request as StarletteRequest
from user_agents import parse
from application.settings import settings
from utils.ip_manage import IPManage


class LoginLogDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(LoginLogDal, self).__init__()
        self.db = db
        self.model = models.SysLoginLog
        self.schema = schemas.LoginLogSimpleOut

    async def create_login_record(
            self,
            data,
            status: bool,
            req: Request | StarletteRequest,
            resp: dict
    ):
        """
        创建登录记录
        :return:
        """
        if not settings.LOGIN_LOG_RECORD:
            return None
        header = {}
        for k, v in req.headers.items():
            header[k] = v
        if isinstance(req, StarletteRequest):
            form = (await req.form()).multi_items()
            params = json.dumps({"form": form, "headers": header})
        else:
            body = json.loads((await req.body()).decode())
            params = json.dumps({"body": body, "headers": header})
        user_agent = parse(req.headers.get("user-agent"))
        system = f"{user_agent.os.family} {user_agent.os.version_string}"
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        ip = IPManage(req.client.host)
        location = await ip.parse()
        obj = models.SysLoginLog(
            **location.dict(),
            username=data.username,
            status=status,
            browser=browser,
            system=system,
            response=json.dumps(resp),
            request=params,
            platform=data.platform,
            login_method=data.method
        )
        self.db.add(obj)
        await self.db.flush()

    async def get_user_distribute(self) -> list[dict]:
        """
        获取用户登录分布情况
        高德经纬度查询：https://lbs.amap.com/tools/picker

        {
            name: '北京',
            center: [116.407394, 39.904211],
            total: 20
        }

        :return: List[dict]
        """
        result = [{
                    "name": '北京',
                    "center": [116.407394, 39.904211],
                },
                {
                    "name": '重庆',
                    "center": [106.551643, 29.562849],
                },
                {
                    "name": '郑州',
                    "center": [113.778584, 34.759197],
                },
                {
                    "name": '南京',
                    "center": [118.796624, 32.059344],
                },
                {
                    "name": '武汉',
                    "center": [114.304569, 30.593354],
                },
                {
                    "name": '乌鲁木齐',
                    "center": [87.616824, 43.825377],
                },
                {
                    "name": '新乡',
                    "center": [113.92679, 35.303589],
                }]
        for data in result:
            assert isinstance(data, dict)
            data["total"] = random.randint(2, 80)
        return result