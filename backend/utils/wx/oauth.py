#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/3/15 20:44 
# @File           : oauth.py
# @IDE            : PyCharm
# @desc           : 简要说明

import requests
from core.logger import logger
from utils.wx.wx_access_token import WxAccessToken


class WXOAuth:

    def __init__(self, appid: str, secret: str):
        """
        初始化微信认证
        :param appid: 微信小程序/公众号的appid
        :param secret: 微信小程序/公众号的secret
        """
        # 重试次数
        self.retry_count = 5
        self.appid = appid
        self.secret = secret

    async def get_code2session(self, code: str) -> dict:
        """
        通过微信用户临时登录凭证 code 进行校验，获取用户openid，与 session 信息

        官方文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
        :param code: 登录时获取的 code
        :return: 正确：{'session_key': 'F8/5LZrdtINYLPEdUJgXXQ==', 'openid': 'okLlC5Kcv7DH2J99dz-Z2FwJeEeU'}
        :return: 报错：{'errcode': 40029, 'errmsg': 'invalid code, rid: 62308e5d-0b0b697e-1db652eb'}
        """
        if not self.appid or not self.secret:
            raise ValueError("微信配置信息不能为空")
            
        api = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": self.appid,
            "secret": self.secret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        response = requests.get(url=api, params=params)
        result = response.json()
        if "openid" not in result:
            logger.error(f"微信校验失败：{result}, code：{code}")
        else:
            logger.info(f"微信校验成功：{result}, code：{code}")
        return result

    async def get_phone_number(self, code: str):
        """
        获取微信用户手机号

        官方文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/phonenumber/phonenumber.getPhoneNumber.html
        :param code: 动态令牌。可通过动态令牌换取用户手机号。
        :return: 成功：{'errcode': 0, 'errmsg': 'ok', 'phone_info': {'phoneNumber': '15093430559'
        , 'purePhoneNumber': '15093430559', 'countryCode': '86', 'watermark': {'timestamp': 1647355468, 'appid': 'wx069c452f9a733df1'}}}
        失败：{'errcode': 40001, 'errmsg': 'invalid credential, access_token is invalid or not latest rid: 62690257-2894b530-58c6fcf3'}
        """
        if not self.appid or not self.secret:
            raise ValueError("微信配置信息不能为空")
            
        api = "https://api.weixin.qq.com/wxa/business/getuserphonenumber"
        at = WxAccessToken(self.appid, self.secret)
        access_token = await at.get()
        if not access_token.get("status", False):
            result = {'errcode': 40001, 'errmsg': '获取微信令牌失败'}
            # print(result)
            logger.error(f"获取微信用户手机号失败：{result}")
            return result
        params = {
            "access_token": access_token.get("token"),
        }
        data = {
            "code": code,
        }
        response = requests.post(url=api, params=params, json=data)
        result = response.json()
        if result.get("errcode", 0) == 0:
            # print("获取微信用户手机号成功", result)
            logger.info(f"获取微信用户手机号成功：{result}, code：{code}")
        else:
            # print("获取微信用户手机号失败", result)
            logger.error(f"获取微信用户手机号失败：{result}, code：{code}")
            if result.get("errcode", 0) == 40001:
                await at.update()
                if self.retry_count > 0:
                    logger.error(f"重试获取微信手机号，重试剩余次数, {self.retry_count}")
                    self.retry_count -= 1
                    return await self.get_phone_number(code)
        return result

    async def parsing_phone_number(self, code: str):
        """
        解析微信用户手机号
        :param code: 动态令牌。可通过动态令牌换取用户手机号。
        :return:
        """
        result = await self.get_phone_number(code)
        if result.get("errcode") == 0:
            phone_info = result["phone_info"]
            assert isinstance(phone_info, dict)
            return phone_info["phoneNumber"]
        return None

    async def parsing_openid(self, code: str):
        """
        解析openid
        :param code: 动态令牌。可通过动态令牌换取用户手机号。
        :return: openid | None
        """
        result = await self.get_code2session(code)
        if "openid" in result:
            return result["openid"]
        return None


# if __name__ == '__main__':
#     WXOAuth().get_code2session("063mPDFa1v16PC0yqhGa1uQ86t4mPDFV")
