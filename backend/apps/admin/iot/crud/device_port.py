#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据库 增删改查操作

import json
import os
from enum import Enum

from motor.motor_asyncio import AsyncIOMotorDatabase
from application.settings import settings
from core.database import redis_getter
from core.mongo_manage import MongoManage
from utils.file.file_manage import FileManage
from fastapi import Request
from typing import Any
from redis.asyncio import Redis
from fastapi import UploadFile
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.exception import CustomException

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, false,update,func

from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession

from core.validator import vaild_ip

# from utils.file.aliyun_oss import AliyunOSS, BucketConf

from utils.excel.import_manage import ImportManage, FieldType
from utils.excel.write_xlsx import WriteXlsx
from utils.send_email import EmailSender
from utils.sms.reset_passwd import ResetPasswordSMS
from  apps.admin.iot.params import ClientGroupParams,ClientParams,ProductParams
from utils.tools import test_password
from apps.admin.iot import models, schemas
from application.settings import settings
from utils.excel.excel_manage import ExcelManage
from apps.admin.system import crud as sys_crud
from .device import DeviceDal
import copy
from utils import status
from utils.wx.oauth import WXOAuth
from datetime import datetime
class DevicePortDal(DalBase):

    import_headers = [

        {"label": "名称", "field": "name", "required": False},
        {"label": "状态", "field": "status", "required": True},
        {"label": "备注", "field": "remark", "required": False},


        # {"label": "关联角色", "field": "role_ids", "required": True, "type": FieldType.list},
    ]

    def __init__(self, db: AsyncSession):
        super(DevicePortDal, self).__init__()
        self.db = db
        self.model = models.IotDevicePort
        self.schema = schemas.DevicePortSimpleOut

    # async def recursion_get_dept_ids(
    #         self,
    #         user: models.SysUser,
    #         dept: models.SysDept = None,
    #         dept_ids: list[int] = None
    # ) -> list:
    #     """
    #     递归获取所有关联部门 id
    #     :param user:
    #     :param depts: 所有部门实例
    #     :param dept_ids: 父级部门 id 列表
    #     :return:
    #     """
    #     if not dept:
    #         depts = await DeptDal(self.db).get_datas(limit=0, v_return_objs=True)
    #         result = []
    #         for i in user.depts:
    #             result.append(i.id)
    #         result.extend(await self.recursion_get_dept_ids(user, depts, result))
    #         return list(set(result))
    #     # elif dept_ids:
    #     #     result = [i.id for i in filter(lambda item: item.parent_id in dept_ids, depts)]
    #     #     result.extend(await self.recursion_get_dept_ids(user, dept, result))
    #     #     return result
    #     else:
    #         return []

    async def update_port_status(self, port: models.IotDevicePort, status: int) -> None:
        """
        更新当前端口信息
        :param port: port对象
        :param status: 状态
        :return:
        """
        port.status = status
        port.updated_at = datetime.now()
        await self.db.flush()

    async def create_data(
            self,
            data: schemas.ClientIn,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建用户
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        """
        unique = await self.get_data(name=data.name,device_id=data.device_id, v_return_none=True)
        if unique:
            raise CustomException("端口已存在！", code=status.HTTP_ERROR)


        obj = self.model(**data.model_dump())
        # if data.role_ids:
        #     roles = await RoleDal(self.db).get_datas(limit=0, id=("in", data.role_ids), v_return_objs=True)
        #     for role in roles:
        #         obj.roles.add(role)
        # if data.dept_ids:
        #     depts = await DeptDal(self.db).get_datas(limit=0, id=("in", data.dept_ids), v_return_objs=True)
        #     for dept in depts:
        #         obj.depts.add(dept)
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.ClientUpdate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新用户信息
        :param data_id:
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        """

        obj = await self.get_data(data_id)
        data_dict = jsonable_encoder(data)
        for key, value in data_dict.items():
            setattr(obj, key, value)
        await self.flush(obj)
        print(22222222212,obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)


    async def export_query_list(self, header: list, params: ClientParams) -> dict:
        """
        导出用户查询列表为 excel
        :param header:
        :param params:
        :return:
        """

        options = [joinedload(models.IotDevicePort.Device)]
        datas = await self.get_datas(**params.dict(), v_return_objs=True,v_options=options)
        # 获取表头
        row = list(map(lambda i: i.get("label"), header))
        rows = []

        for port in datas:
            data = []
            for item in header:
                field = item.get("field")
                # 通过反射获取对应的属性值
                value = getattr(port, field, "")
                if field == 'device':
                    value = value.name if value else ''

                if field == "status":
                    value = '未使用'
                    if value == '1':
                        value ='接通'
                    if value =='0':
                        value = "断开"


                data.append(value)
            rows.append(data)
        em = ExcelManage()
        em.create_excel("端口列表")
        em.write_list(rows, row)
        file_url = em.save_excel()
        em.close()
        return {"url": file_url, "filename": "端口列表.xlsx"}

    async def get_import_headers_options(self) -> None:
        """
        补全表头数据选项
        :return:
        """
        # 角色选择项
        devices = await DeviceDal(self.db).get_datas(limit=0, v_return_objs=True, status=True)
        device_options = self.import_headers[4]
        assert isinstance(device_options, dict)
        device_options["options"] = [{"label": device.name, "value": device.id} for device in devices]
        #
        # # 性别选择项
        # dict_types = await sys_crud.DictTypeDal(self.db).get_dict_type_dicts(["sys_gender"])
        # gender_options = self.import_headers[3]
        # assert isinstance(gender_options, dict)
        # sys_gender = dict_types.get("sys_gender")
        # gender_options["options"] = [{"label": item["label"], "value": item["value"]} for item in sys_gender]

    async def download_import_template(self) -> dict:
        """
        下载用户最新版导入模板
        :return:
        """
        await self.get_import_headers_options()
        em = WriteXlsx()
        em.create_excel(sheet_name="用户导入模板", save_static=True)

        em.generate_template(copy.deepcopy(self.import_headers))
        em.close()
        return {"url": em.get_file_url(), "filename": "用户导入模板.xlsx"}

    # async def import_users(self, file: UploadFile) -> dict:
    #     """
    #     批量导入用户数据
    #     :param file:
    #     :return:
    #     """
    #     await self.get_import_headers_options()
    #     im = ImportManage(file, copy.deepcopy(self.import_headers))
    #     await im.get_table_data()
    #     im.check_table_data()
    #     for item in im.success:
    #         old_data_list = item.pop("old_data_list")
    #         data = schemas.UserIn(**item)
    #         try:
    #             await self.create_data(data)
    #         except ValueError as e:
    #             old_data_list.append(e.__str__())
    #             im.add_error_data(old_data_list)
    #         except Exception as e:
    #             print(e)
    #             old_data_list.append(f"创建失败，请联系管理员！ 错误信息:{e}")
    #             im.add_error_data(old_data_list)
    #     return {
    #         "success_number": im.success_number,
    #         "error_number": im.error_number,
    #         "error_url": im.generate_error_url()
    #     }

    # async def init_password(self, ids: list[int]) -> list:
    #     """
    #     初始化所选用户密码
    #     将用户密码改为系统默认密码，并将初始化密码状态改为false
    #     :param ids:
    #     :return:
    #     """
    #     users = await self.get_datas(limit=0, id=("in", ids), v_return_objs=True)
    #     result = []
    #     for user in users:
    #         # 重置密码
    #         data = {"id": user.id, "phone": user.phone, "name": user.name, "email": user.email}
    #         password = user.phone[5:12] if settings.DEFAULT_PASSWORD == "0" else settings.DEFAULT_PASSWORD
    #         user.password = self.model.get_password_hash(password)
    #         user.is_reset_password = False
    #         self.db.add(user)
    #         data["reset_password_status"] = True
    #         data["password"] = password
    #         result.append(data)
    #     await self.db.flush()
    #     return result

    # async def init_password_send_sms(self, ids: list[int], rd: Redis) -> list:
    #     """
    #     初始化所选用户密码并发送通知短信
    #     将用户密码改为系统默认密码，并将初始化密码状态改为false
    #     :param ids:
    #     :param rd:
    #     :return:
    #     """
    #     result = await self.init_password(ids)
    #     for user in result:
    #         if not user["reset_password_status"]:
    #             user["send_sms_status"] = False
    #             user["send_sms_msg"] = "重置密码失败"
    #             continue
    #         password = user.pop("password")
    #         sms = ResetPasswordSMS([user.get("phone")], rd)
    #         try:
    #             send_result = (await sms.main_async(password=password))[0]
    #             user["send_sms_status"] = send_result
    #             user["send_sms_msg"] = "" if send_result else "短信发送失败，请联系管理员"
    #         except CustomException as e:
    #             user["send_sms_status"] = False
    #             user["send_sms_msg"] = e.msg
    #     return result

    # async def init_password_send_email(self, ids: list[int]) -> list:
    #     """
    #     初始化所选用户密码并发送通知邮件
    #     将用户密码改为系统默认密码，并将初始化密码状态改为false
    #     :param ids:
    #     :param rd:
    #     :return:
    #     """
    #     result = await self.init_password(ids)
    #     for user in result:
    #         if not user["reset_password_status"]:
    #             user["send_sms_status"] = False
    #             user["send_sms_msg"] = "重置密码失败"
    #             continue
    #         password: str = user.pop("password")
    #         email: str = user.get("email", None)
    #         if email:
    #             subject = "密码已重置"
    #             body = f"您好，您的密码已经重置为{password}，请及时登录并修改密码。"
    #             web_mail = await SettingsDal(self.db).get_tab_values(tab_id=10)
    #             print(web_mail,"web")
    #             es = EmailSender(web_mail)
    #             try:
    #                 send_result = await es.send_email([email], subject, body)
    #                 user["send_sms_status"] = send_result
    #                 user["send_sms_msg"] = "" if send_result else "短信发送失败，请联系管理员"
    #             except CustomException as e:
    #                 user["send_sms_status"] = False
    #                 user["send_sms_msg"] = e.msg
    #         else:
    #             user["send_sms_status"] = False
    #             user["send_sms_msg"] = "未获取到邮箱地址"
    #     return result

    # async def update_current_avatar(self, user: models.SysUser, file: UploadFile) -> str:
    #     """
    #     更新当前用户头像
    #     :param user:
    #     :param file:
    #     :return:
    #     """
    #     # result = await AliyunOSS(BucketConf(**settings.ALIYUN_OSS)).upload_image("avatar", file)
    #     result =''
    #     user.avatar = result
    #     await self.flush(user)
    #     return result
    #
    # async def update_wx_server_openid(self, code: str, user: models.SysUser, redis: Redis) -> bool:
    #     """
    #     更新用户服务端微信平台openid
    #     :param code:
    #     :param user:
    #     :param redis:
    #     :return:
    #     """
    #     wx = WXOAuth(redis, 0)
    #     openid = await wx.parsing_openid(code)
    #     if not openid:
    #         return False
    #     user.is_wx_server_openid = True
    #     user.wx_server_openid = openid
    #     await self.flush(user)
    #     return True

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
        """
        删除多个端口，软删除
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """

        return await super(DevicePortDal, self).delete_datas(ids, v_soft, **kwargs)


