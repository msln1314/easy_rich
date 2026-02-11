#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/14 15:55 
# @File           : code.py
# @IDE            : PyCharm
# @desc           : 发送验证码短信

import datetime
import warnings
# from redis.asyncio import Redis
from .aliyun import AliyunSMS
from core.logger import logger
from core.exception import CustomException


class CodeSMS:

    def __init__(self, phone: str):
        self.phone = phone
        self.sign_conf = "sms_sign_name_1"
        self.template_code_conf = "sms_template_code_1"
        self.code = None

    async def _send_async(self, phone: str) -> bool:
        """
        发送短信验证码（不依赖Redis）
        """
        try:
            # 直接调用阿里云短信发送，不进行Redis频率限制
            from .aliyun import AliyunSMS
            sms = AliyunSMS([phone])
            sms.sign_conf = self.sign_conf
            sms.template_code_conf = self.template_code_conf
            
            # 设置验证码
            if self.code:
                template_param = '{"code":"%s"}' % self.code
            else:
                self.code = self.get_code()
                template_param = '{"code":"%s"}' % self.code
            
            # 发送短信
            await sms._get_settings_async()
            return await sms._send_async(phone, template_param=template_param)
        except Exception as e:
            logger.error(f"短信发送失败: {e}")
            raise CustomException(msg="短信发送失败", code=500)

    def get_code(self) -> str:
        """
        生成6位随机验证码
        """
        import random
        return str(random.randint(100000, 999999))

    def _get_template_param(self, **kwargs) -> str:
        """
        获取模板参数

        可以被子类继承的受保护的私有方法
        """
        self.code = kwargs.get("code", self.get_code())
        template_param = '{"code":"%s"}' % self.code
        return template_param

