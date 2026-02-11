#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/11/27 18:37
# @File           : wx_access_token.py
# @IDE            : PyCharm
# @desc           : 获取小程序全局唯一后台接口调用凭据

import requests
from core.logger import logger


class WxAccessToken:
    """
    获取小程序全局唯一后台接口调用凭据（access_token）。调用绝大多数后台接口时都需使用 access_token，开发者需要进行妥善保存。

    官方文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/access-token/auth.getAccessToken.html
    """

    # 类级别的静态变量，所有实例共享
    _current_token = None
    _token_expire_time = None

    def __init__(self, appid: str, secret: str, grant_type: str = "client_credential", *args, **kwargs):
        self.__url = "https://api.weixin.qq.com/cgi-bin/token"
        self.__method = "get"
        self.appid = appid
        self.secret = secret
        self.params = {
            "appid": appid,
            "secret": secret,
            "grant_type": grant_type
        }

    async def get(self) -> dict:
        """
        获取小程序access_token（使用类级别的内存缓存）
        """
        import time
        
        # 检查当前token是否有效（7200秒有效期，提前5分钟更新）
        if WxAccessToken._current_token and WxAccessToken._token_expire_time and time.time() < WxAccessToken._token_expire_time - 300:
            return {"status": True, "token": WxAccessToken._current_token}
        
        # 如果token无效或即将过期，重新获取
        return await self.update()

    async def update(self) -> dict:
        """
        更新小程序access_token（使用类级别的内存缓存）
        """
        import time
        
        print("开始更新 access_token")
        method = getattr(requests, self.__method)
        response = method(url=self.__url, params=self.params)
        result = response.json()

        if result.get("errcode", "0") != "0":
            print("获取access_token失败", result)
            logger.error(f"获取access_token失败：{result}")
            return {"status": False, "token": None}

        print("成功获取到", result)
        
        # 存储到类级别的内存缓存中，设置过期时间（7200秒有效期）
        WxAccessToken._current_token = result.get("access_token")
        WxAccessToken._token_expire_time = time.time() + 7200
        
        logger.info(f"获取access_token成功：{result}")

        return {"status": True, "token": WxAccessToken._current_token}
