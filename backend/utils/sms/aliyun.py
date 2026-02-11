#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/14 15:26 
# @File           : aliyun.py
# @IDE            : PyCharm
# @desc           : 最新版阿里云短信服务发送程序（Python版本）2022-11-08

"""
短信 API 官方文档：https://help.aliyun.com/document_detail/419298.html?spm=5176.25163407.help.dexternal.6ff2bb6ercg9x3
发送短信 官方文档：https://help.aliyun.com/document_detail/419273.htm?spm=a2c4g.11186623.0.0.36855d7aRBSwtP
Python SDK 官方文档：https://help.aliyun.com/document_detail/215764.html?spm=a2c4g.11186623.0.0.6a0c4198XsBJNW

环境要求
Python 3
安装 SDK 核心库 OpenAPI ，使用pip安装包依赖:
pip install alibabacloud_tea_openapi
pip install alibabacloud_dysmsapi20170525
"""
import random
import re
from typing import List
from core.exception import CustomException
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from core.logger import logger
import datetime
from utils.db_getter import DBGetter
# 从数据库直接查询配置信息
from apps.admin.system.crud.setting import SettingsDal
from core.database import db_getter

class AliyunSMS(DBGetter):
    # 返回错误码对应：
    doc = "https://help.aliyun.com/document_detail/101346.html"

    def __init__(self, phones: List[str]):
        super().__init__()
        self.check_phones_format(phones)
        self.phones = phones

        self.sign_conf = None  # 数据库中 sms_sign_name_* 的配置
        self.template_code_conf = None  # 数据库中 sms_template_code_* 的配置
        # 以上两个配置项的好处在于可以灵活配置短信信息，不需要改代码
        
        # 初始化配置变量
        self.access_key = None
        self.access_key_secret = None
        self.send_interval = None
        self.valid_time = None
        self.sign_name = None
        self.template_code = None

    async def main_async(self, **kwargs) -> List[bool]:
        """
        主程序入口，异步方式

        redis 对象必填
        """
        result = []
        await self._get_settings_async()
        for phone in self.phones:
            result.append(await self._send_async(phone, **kwargs))
        return result

    async def _send_async(self, phone: str, **kwargs) -> bool:
        """
        发送短信
        """
        client = self.create_client(self.access_key, self.access_key_secret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=self._get_template_param(**kwargs)
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = await client.send_sms_with_options_async(send_sms_request, runtime)
            return self._validation(phone, resp)
        except Exception as e:
            print(e.__str__())
            return False

    async def _get_settings_async(self, retry: int = 3):
        """
        获取配置信息（不依赖Redis，直接查询数据库）
        """
        if not self.sign_conf or not self.template_code_conf:
            raise ValueError("缺少短信签名信息和短信模板ID！")
        

        
        async_session = db_getter()
        db = await async_session.__anext__()
        settings_dal = SettingsDal(db)
        
        # 获取所有相关配置
        config_keys = [
            "sms_access_key",
            "sms_access_key_secret", 
            "sms_send_interval",
            "sms_valid_time",
            self.sign_conf,
            self.template_code_conf
        ]
        
        # 查询配置值
        for key in config_keys:
            setting = await settings_dal.get_data(config_key=key, disabled=False, v_return_none=True)
            if not setting:
                raise ValueError(f"配置项 {key} 不存在或已禁用")
            
            if key == "sms_access_key":
                self.access_key = setting.config_value
            elif key == "sms_access_key_secret":
                self.access_key_secret = setting.config_value
            elif key == "sms_send_interval":
                self.send_interval = int(setting.config_value)
            elif key == "sms_valid_time":
                self.valid_time = int(setting.config_value)
            elif key == self.sign_conf:
                self.sign_name = setting.config_value
            elif key == self.template_code_conf:
                self.template_code = setting.config_value

    def main(self, **kwargs) -> List[bool]:
        """
        主程序入口，同步方式
        """
        result = []
        self._get_settings()
        for phone in self.phones:
            result.append(self._send(phone, **kwargs))
        return result

    def _send(self, phone: str, **kwargs) -> bool:
        """
        同步方式发送短信
        """
        client = self.create_client(self.access_key, self.access_key_secret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=self._get_template_param(**kwargs)
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = client.send_sms_with_options(send_sms_request, runtime)
            return self._validation(phone, resp)
        except Exception as e:
            print(e.__str__())
            return False

    def _get_settings(self):
        """
        同步方式获取配置信息（不依赖Redis，直接查询数据库）
        """
        if not self.sign_conf or not self.template_code_conf:
            raise ValueError("缺少短信签名信息和短信模板ID！")
        
        # 从数据库直接查询配置信息
        import asyncio
        
        # 同步方法中调用异步方法
        async def async_get_settings():
            await self._get_settings_async()
        
        try:
            # 获取当前事件循环，如果没有则创建新的事件循环
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果事件循环正在运行，需要在新线程中运行
                import threading
                from concurrent.futures import ThreadPoolExecutor
                
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, async_get_settings())
                    future.result()
            else:
                # 如果事件循环未运行，直接运行
                asyncio.run(async_get_settings())
        except RuntimeError:
            # 如果没有事件循环，创建新的事件循环
            asyncio.run(async_get_settings())

    def _get_template_param(self, **kwargs) -> str:
        """
        获取模板参数

        可以被子类继承的受保护的私有方法
        """
        raise NotImplementedError("该方法应该被重写！")

    def _validation(self, phone: str, resp: dysmsapi_20170525_models.SendSmsResponse) -> bool:
        """
        验证结果并返回
        """
        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if resp.body.code == "OK":
            logger.info(f'{send_time} {phone} 短信发送成功，返回code：{resp.body.code}')
            return True
        else:
            logger.error(f'{send_time} {phone} 短信发送失败，返回code：{resp.body.code}，请参考文档：{self.doc}')
            return False

    @staticmethod
    def get_code(length: int = 6, blend: bool = False) -> str:
        """
        随机获取短信验证码
        短信验证码只支持数字，不支持字母及其他符号

        :param length: 验证码长度
        :param blend: 是否 字母+数字 混合
        """
        code = ""  # 创建字符串变量,存储生成的验证码
        for i in range(length):  # 通过for循环控制验证码位数
            num = random.randint(0, 9)  # 生成随机数字0-9
            if blend:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
                upper_alpha = chr(random.randint(65, 90))
                lower_alpha = chr(random.randint(97, 122))
                # 随机选择其中一位
                num = random.choice([num, upper_alpha, lower_alpha])
            code = code + str(num)
        return code

    @classmethod
    def check_phones_format(cls, phones: List[str]) -> bool:
        """
        同时检查多个手机号格式是否合法

        不合法就会抛出异常
        """
        for phone in phones:
            cls.check_phone_format(phone)
        return True

    @staticmethod
    def check_phone_format(phone: str) -> bool:
        """
        检查手机号格式是否合法

        不合法就会抛出异常
        """
        REGEX_phone = r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$'

        if not phone:
            raise CustomException(msg=f"手机号码（{phone}）不能为空", code=400)
        elif not re.match(REGEX_phone, phone):
            raise CustomException(msg=f"手机号码（{phone}）格式不正确", code=400)
        return True

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        :param access_key_id:
        :param access_key_secret:
        :return: Client
        :throws Exception
        """
        config = open_api_models.Config(
            # 您的 AccessKey ID,
            access_key_id=access_key_id,
            # 您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)
