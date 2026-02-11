#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/1/28
# @File           : code_manager.py
# @IDE            : PyCharm
# @desc           : 统一的验证码管理（支持短信和邮箱）

import datetime
from core.validator import valid_phone
from core.exception import CustomException
from .code import CodeSMS
from apps.admin.log.crud.code import CodeSendLogDal

class CodeManager:
    """
    统一的验证码管理类，支持短信和邮箱验证码
    """

    def __init__(self, contact: str, web_email=None, user_id=None, ip_address=None, scene="login", db=None):
        """
        :param contact: 联系方式（手机号或邮箱）
        :param web_email: 邮箱配置信息（仅邮箱验证码需要）
        :param user_id: 用户ID（用于记录日志）
        :param ip_address: IP地址（用于记录日志）
        :param scene: 发送场景（用于记录日志）
        :param db: 数据库会话（必须）
        """
        self.contact = contact
        self.web_email = web_email
        self.is_phone = self._check_is_phone(contact)
        self.code = None
        self.valid_time = 300  # 验证码有效时间（秒）
        self.send_interval = 60  # 发送间隔（秒）
        self.user_id = user_id
        self.ip_address = ip_address
        self.scene = scene
        self.db = db
        self.error_message = None

    def _check_is_phone(self, contact: str) -> bool:
        """
        判断是否为手机号
        """
        try:
            return valid_phone(contact) == contact
        except:
            return False

    def get_code(self) -> str:
        """
        生成6位随机验证码
        """
        import random
        return str(random.randint(100000, 999999))

    async def send_code(self) -> bool:
        """
        发送验证码（自动判断是短信还是邮箱）
        """
        if not self.db:
            raise CustomException(msg="数据库会话不能为空", code=500)

        # 检查发送频率
        
        code_log_dal = CodeSendLogDal(self.db)

        can_send = await code_log_dal.check_send_interval(
            self.contact,
            self.send_interval,
            self.scene
        )

        if not can_send:
            raise CustomException(msg="发送过于频繁，请稍后再试", code=400)

        # 生成验证码
        self.code = self.get_code()

        # 计算失效时间
        expire_time = datetime.datetime.now() + datetime.timedelta(seconds=self.valid_time)

        # 发送验证码
        code_type = "sms" if self.is_phone else "email"
        try:
            if self.is_phone:
                # 发送短信验证码
                result = await self._send_sms_code()
            else:
                # 发送邮箱验证码
                result = await self._send_email_code()
        except Exception as e:
            self.error_message = str(e)
            result = False
        else:
            self.error_message = None

        # 记录发送日志
        if result:
            await self._save_code_log(code_type, True, expire_time)
            return True
        else:
            await self._save_code_log(code_type, False, expire_time)
            return False

    async def _send_sms_code(self) -> bool:
        """
        发送短信验证码
        """
        try:
            sms = CodeSMS(self.contact)
            sms.code = self.code
            return await sms._send_async(self.contact)
        except Exception as e:
            print(f"短信发送失败: {e}")
            raise

    async def _send_email_code(self) -> bool:
        """
        发送邮箱验证码
        """
        try:
            from utils.send_email import EmailSender

            if not self.web_email:
                raise CustomException(msg="邮箱服务未配置", code=500)

            es = EmailSender(self.web_email)
            subject = "验证码"
            body = f"您的验证码是：{self.code}，验证码有效时间为5分钟，请勿泄露给他人。"

            result = await es.send_email([self.contact], subject, body)
            return result
        except Exception as e:
            print(f"邮件发送失败: {e}")
            raise

    async def _save_code_log(self, code_type: str, send_status: bool, expire_time) -> None:
        """
        保存验证码发送日志

        :param code_type: 验证码类型
        :param send_status: 发送状态
        :param expire_time: 失效时间
        """
        try:
          

            code_log_dal = CodeSendLogDal(self.db)
            await code_log_dal.create_code_log(
                user_id=self.user_id,
                contact=self.contact,
                code=self.code,
                code_type=code_type,
                send_status=send_status,
                expire_time=expire_time,
                ip_address=self.ip_address,
                scene=self.scene,
                error_message=self.error_message
            )
        except Exception as e:
            print(f"保存验证码日志失败: {e}")

    async def verify_code(self, code: str) -> bool:
        """
        验证验证码是否正确（从数据库查询）
        """
        if not self.db:
            return False

        try:
            from apps.admin.log.crud.code import CodeSendLogDal

            code_log_dal = CodeSendLogDal(self.db)
            return await code_log_dal.verify_code(self.contact, code, self.scene)
        except Exception as e:
            print(f"验证码验证失败: {e}")
            return False
