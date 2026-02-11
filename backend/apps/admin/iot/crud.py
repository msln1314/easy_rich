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
from .params import ClientGroupParams,ClientParams,ProductParams
from utils.tools import test_password
from . import models, schemas
from application.settings import settings
from utils.excel.excel_manage import ExcelManage
from apps.admin.system import crud as sys_crud
import copy
from utils import status
from utils.wx.oauth import WXOAuth
from datetime import datetime


class ClientDal(DalBase):

    import_headers = [
        {"label": "充电桩编号", "field": "sn", "required": True},
        {"label": "名称", "field": "name", "required": False},
        {"label": "设备类型", "field": "device_type", "required": True},
        {"label": "IP", "field": "ip", "required": False},
        {"label": "区域", "field": "area", "required": False},
        {"label": "地址", "field": "address", "required": False},

        # {"label": "关联角色", "field": "role_ids", "required": True, "type": FieldType.list},
    ]

    def __init__(self, db: AsyncSession):
        super(ClientDal, self).__init__()
        self.db = db
        self.model = models.IotClient
        self.schema = schemas.ClientSimpleOut

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

    async def update_deal_status(self, client: models.IotClient, status: int) -> None:
        """
        更新当前登录信息
        :param client: client对象
        :param status: 状态
        :return:
        """
        client.deal_status = status
        client.deal_time = datetime.now()
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
        unique = await self.get_data(sn=data.sn, v_return_none=True)
        if unique:
            raise CustomException("编码已存在！", code=status.HTTP_ERROR)

        data.avatar = data.avatar if data.avatar else settings.DEFAULT_AVATAR
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
        obj = await self.get_data(data_id, v_options=[joinedload(self.model.roles)])
        data_dict = jsonable_encoder(data)
        for key, value in data_dict.items():
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def update_bind_info(self, client: models.IotClient, data: schemas.ClientBind) -> Any:
        """
        更新当前客户端绑定信息
        :param user:
        :param data:
        :return:
        """

        client.device_id = data.device_id
        client.port = data.port
        client.connect_type = data.connect_type
        client.bind_time = datetime.now()

        await self.flush(client)
        return await self.out_dict(client)

    async def export_query_list(self, header: list, params: ClientParams) -> dict:
        """
        导出用户查询列表为 excel
        :param header:
        :param params:
        :return:
        """

        options = [joinedload(models.IotClient.Device), joinedload(models.IotClient.group)]
        datas = await self.get_datas(**params.dict(), v_return_objs=True,v_options=options)
        # 获取表头
        row = list(map(lambda i: i.get("label"), header))
        rows = []

        for client in datas:
            data = []
            for item in header:
                field = item.get("field")
                # 通过反射获取对应的属性值
                value = getattr(client, field, "")
                if field == 'device':
                    value = value.name if value else ''

                if field == "is_active":
                    value = "可用" if value else "停用"


                data.append(value)
            rows.append(data)
        em = ExcelManage()
        em.create_excel("客户端列表")
        em.write_list(rows, row)
        file_url = em.save_excel()
        em.close()
        return {"url": file_url, "filename": "客户端列表.xlsx"}

    async def get_import_headers_options(self) -> None:
        """
        补全表头数据选项
        :return:
        """
        # 角色选择项
        device = await DeviceDul(self.db).get_datas(limit=0, v_return_objs=True, status=True)
        role_options = self.import_headers[4]
        assert isinstance(role_options, dict)
        role_options["options"] = [{"label": role.name, "value": role.id} for role in roles]

        # 性别选择项
        dict_types = await sys_crud.DictTypeDal(self.db).get_dict_type_dicts(["sys_gender"])
        gender_options = self.import_headers[3]
        assert isinstance(gender_options, dict)
        sys_gender = dict_types.get("sys_gender")
        gender_options["options"] = [{"label": item["label"], "value": item["value"]} for item in sys_gender]

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

    async def import_users(self, file: UploadFile) -> dict:
        """
        批量导入用户数据
        :param file:
        :return:
        """
        await self.get_import_headers_options()
        im = ImportManage(file, copy.deepcopy(self.import_headers))
        await im.get_table_data()
        im.check_table_data()
        for item in im.success:
            old_data_list = item.pop("old_data_list")
            data = schemas.UserIn(**item)
            try:
                await self.create_data(data)
            except ValueError as e:
                old_data_list.append(e.__str__())
                im.add_error_data(old_data_list)
            except Exception as e:
                print(e)
                old_data_list.append(f"创建失败，请联系管理员！ 错误信息:{e}")
                im.add_error_data(old_data_list)
        return {
            "success_number": im.success_number,
            "error_number": im.error_number,
            "error_url": im.generate_error_url()
        }

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
        删除多个用户，软删除
        删除后清空所关联的角色
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        options = [joinedload(self.model.roles)]
        objs = await self.get_datas(limit=0, id=("in", ids), v_options=options, v_return_objs=True)
        for obj in objs:
            if obj.roles:
                obj.roles.clear()
        return await super(UserDal, self).delete_datas(ids, v_soft, **kwargs)


# class RoleDal(DalBase):
#
#     def __init__(self, db: AsyncSession):
#         super(RoleDal, self).__init__()
#         self.db = db
#         self.model = models.SysRole
#         self.schema = schemas.RoleSimpleOut
#
#     async def create_data(
#             self,
#             data: schemas.RoleIn,
#             v_options: list[_AbstractLoad] = None,
#             v_return_obj: bool = False,
#             v_schema: Any = None
#     ) -> Any:
#         """
#         创建数据
#         :param data:
#         :param v_options:
#         :param v_return_obj:
#         :param v_schema:
#         :return:
#         """
#         obj = self.model(**data.model_dump(exclude={'menu_ids', 'dept_ids'}))
#         if data.menu_ids:
#             menus = await MenuDal(db=self.db).get_datas(limit=0, id=("in", data.menu_ids), v_return_objs=True)
#             for menu in menus:
#                 obj.menus.add(menu)
#         # print(data,"daaaaaaaaaaaaaaaaaaaa")
#         # if data.dept_ids:
#         #     depts = await DeptDal(db=self.db).get_datas(limit=0, id=("in", data.dept_ids), v_return_objs=True)
#         #     for dept in depts:
#         #         obj.depts.add(dept)
#         await self.flush(obj)
#         return await self.out_dict(obj, v_options, v_return_obj, v_schema)
#
#     async def put_data(
#             self,
#             data_id: int,
#             data: schemas.RoleIn,
#             v_options: list[_AbstractLoad] = None,
#             v_return_obj: bool = False,
#             v_schema: Any = None
#     ) -> Any:
#         """
#         更新单个数据
#         :param data_id:
#         :param data:
#         :param v_options:
#         :param v_return_obj:
#         :param v_schema:
#         :return:
#         """
#         obj = await self.get_data(data_id, v_options=[joinedload(self.model.menus)])
#         obj_dict = jsonable_encoder(data)
#         for key, value in obj_dict.items():
#             if key == "menu_ids":
#                 if value:
#                     menus = await MenuDal(db=self.db).get_datas(limit=0, id=("in", value), v_return_objs=True)
#                     if obj.menus:
#                         obj.menus.clear()
#                     for menu in menus:
#                         obj.menus.add(menu)
#                 continue
#             elif key == "user_ids":
#                 if value:
#                     users = await UserDal(db=self.db).get_datas(limit=0, id=("in", value), v_return_objs=True)
#                     if obj.users:
#                         obj.users.clear()
#                     for user in users:
#                         obj.users.add(user)
#                 continue
#             setattr(obj, key, value)
#         await self.flush(obj)
#         return await self.out_dict(obj, None, v_return_obj, v_schema)
#
#     async def get_role_menu_tree(self, role_id: int) -> list:
#         role = await self.get_data(role_id, v_options=[joinedload(self.model.menus)])
#         return [i.id for i in role.menus]
#
#     async def get_select_datas(self) -> list:
#         """
#         获取选择数据，全部数据
#         :return:
#         """
#         sql = select(self.model)
#         queryset = await self.db.scalars(sql)
#         return [schemas.RoleOptionsOut.model_validate(i).model_dump() for i in queryset.all()]
#
#     async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
#         """
#         删除多个角色，硬删除
#         如果存在用户关联则无法删除
#         :param ids: 数据集
#         :param v_soft: 是否执行软删除
#         :param kwargs: 其他更新字段
#         """
#         user_count = await UserDal(self.db).get_count(v_join=[["roles"]], v_where=[models.SysRole.id.in_(ids)])
#         if user_count > 0:
#             raise CustomException("无法删除存在用户关联的角色", code=400)
#         return await super(RoleDal, self).delete_datas(ids, v_soft, **kwargs)
#
#
# class MenuDal(DalBase):
#
#     def __init__(self, db: AsyncSession):
#         super(MenuDal, self).__init__()
#         self.db = db
#         self.model = models.SysMenu
#         self.schema = schemas.MenuSimpleOut
#     async def get_max_order(self):
#         result = await self.db.execute(func.max(self.model.order))
#         max_value = result.scalar()
#         return max_value
#     async def get_tree_list(self, mode: int) -> list:
#         """
#         1：获取菜单树列表
#         2：获取菜单树选择项，添加/修改菜单时使用
#         3：获取菜单树列表，角色添加菜单权限时使用
#         :param mode:
#         :return:
#         """
#         if mode == 3:
#             sql = select(self.model).where(self.model.status == 1, self.model.is_delete == false())
#         if mode == 2:
#             sql = select(self.model).where(self.model.menu_type != 2,self.model.is_delete == false())
#         else:
#             sql = select(self.model).where(self.model.is_delete == false())
#         queryset = await self.db.scalars(sql)
#         datas = list(queryset.all())
#         for data in datas:
#             data.title = data.menu_name
#
#         roots = filter(lambda i: not i.parent_id, datas)
#         if mode == 1:
#             menus = self.generate_tree_list(datas, roots)
#         elif mode == 2 or mode == 3:
#             menus = self.generate_tree_options(datas, roots)
#         else:
#             raise CustomException("获取菜单失败，无可用选项", code=400)
#         return self.menus_order(menus)
#
#     async def get_routers(self, user: models.SysUser) -> list:
#         """
#         获取路由表
#         declare interface AppCustomRouteRecordRaw extends Omit<RouteRecordRaw, 'meta'> {
#             name: string
#             meta: RouteMeta
#             component: string
#             path: string
#             redirect: string
#             children?: AppCustomRouteRecordRaw[]
#         }
#         :param user:
#         :return:
#         """
#         if user.is_staff:
#             sql = select(self.model) \
#                 .where(self.model.status == 1, self.model.menu_type != "2", self.model.is_delete == false())
#             queryset = await self.db.scalars(sql)
#             datas = list(queryset.all())
#         else:
#             options = [joinedload(models.SysUser.roles).subqueryload(models.SysRole.menus)]
#             user = await UserDal(self.db).get_data(user.id, v_options=options)
#             datas = set()
#             for role in user.roles:
#                 for menu in role.menus:
#                     # 该路由没有被禁用，并且菜单不是按钮
#                     if menu.status and menu.menu_type != "2":
#                         datas.add(menu)
#         for data in datas:
#             data.title = data.menu_name
#
#         roots = filter(lambda i: not i.parent_id, datas)
#         menus = self.generate_router_tree(datas, roots)
#         return self.menus_order(menus)
#
#     def generate_router_tree(self, menus: list[models.SysMenu], nodes: filter, name: str = "") -> list:
#         """
#         生成路由树
#         :param menus: 总菜单列表
#         :param nodes: 节点菜单列表
#         :param name: name拼接，切记Name不能重复
#         :return:
#         """
#         data = []
#         for root in nodes:
#             router = schemas.RouterOut.model_validate(root)
#             router.name = name + "".join(name.capitalize() for name in router.path.split("/"))
#             router.meta = schemas.Meta(
#                 title=root.title,
#                 icon=root.icon,
#                 hidden=root.hidden,
#                 alwaysShow=root.alwaysShow,
#                 noCache=root.noCache
#             )
#             if root.menu_type == "0":
#                 sons = filter(lambda i: i.parent_id == root.id, menus)
#                 router.children = self.generate_router_tree(menus, sons, router.name)
#             data.append(router.model_dump())
#         return data
#
#     def generate_tree_list(self, menus: list[models.SysMenu], nodes: filter) -> list:
#         """
#         生成菜单树列表
#         :param menus: 总菜单列表
#         :param nodes: 每层节点菜单列表
#         :return:
#         """
#         data = []
#         for root in nodes:
#             router = schemas.MenuTreeListOut.model_validate(root)
#             if root.menu_type == "0" or root.menu_type == "1":
#                 sons = filter(lambda i: i.parent_id == root.id, menus)
#                 router.children = self.generate_tree_list(menus, sons)
#             data.append(router.model_dump())
#         return data
#
#     def generate_tree_options(self, menus: list[models.SysMenu], nodes: filter) -> list:
#         """
#         生成菜单树选择项
#         :param menus:总菜单列表
#         :param nodes:每层节点菜单列表
#         :return:
#         """
#         data = []
#         for root in nodes:
#             router = {"value": root.id, "label": root.title, "order": root.order}
#             if root.menu_type == "0" or root.menu_type == "1":
#                 sons = filter(lambda i: i.parent_id == root.id, menus)
#                 router["children"] = self.generate_tree_options(menus, sons)
#             data.append(router)
#         return data
#
#     @classmethod
#     def menus_order(cls, datas: list, order: str = "order", children: str = "children") -> list:
#         """
#         菜单排序
#         :param datas:
#         :param order:
#         :param children:
#         :return:
#         """
#         result = sorted(datas, key=lambda menu: menu[order])
#         for item in result:
#             if item[children]:
#                 item[children] = sorted(item[children], key=lambda menu: menu[order])
#         return result
#
#     async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
#         """
#         删除多个菜单
#         如果存在角色关联则无法删除
#         :param ids: 数据集
#         :param v_soft: 是否执行软删除
#         :param kwargs: 其他更新字段
#         :return:
#         """
#         count = await RoleDal(self.db).get_count(v_join=[["menus"]], v_where=[self.model.id.in_(ids)])
#         if count > 0:
#             raise CustomException("无法删除存在角色关联的菜单", code=400)
#         await super(MenuDal, self).delete_datas(ids, v_soft, **kwargs)


class DeviceDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DeviceDal, self).__init__()
        self.db = db
        self.model = models.IotDevice
        self.schema = schemas.DeviceSimpleOut

    async def get_tree_list(self, mode: int) -> list:
        """
        1：获取部门树列表
        2：获取部门树选择项，添加/修改部门时使用
        3：获取部门树列表，用户添加部门权限时使用
        :param mode:
        :return:
        """
        if mode == 3:
            sql = select(self.model).where(self.model.status == 0, self.model.is_delete == false())
        else:
            sql = select(self.model).where(self.model.is_delete == false())
        queryset = await self.db.scalars(sql)
        datas = list(queryset.all())
        for data in datas:
            data.title = data.name
        roots = filter(lambda i: not i.parent_id, datas)
        if mode == 1:
            depts = self.generate_tree_list(datas, roots)
        elif mode == 2 or mode == 3:
            depts = self.generate_tree_options(datas, roots)
        else:
            raise CustomException("获取部门失败，无可用选项", code=400)
        return self.dept_order(depts)

    def generate_tree_list(self, depts: list[models.SysDept], nodes: filter) -> list:
        """
        生成部门树列表
        :param depts: 总部门列表
        :param nodes: 每层节点部门列表
        :return:
        """
        data = []
        for root in nodes:
            router = schemas.DeptTreeListOut.model_validate(root)
            sons = filter(lambda i: i.parent_id == root.id, depts)
            router.children = self.generate_tree_list(depts, sons)
            data.append(router.model_dump())
        return data

    def generate_tree_options(self, depts: list[models.SysDept], nodes: filter) -> list:
        """
        生成部门树选择项
        :param depts: 总部门列表
        :param nodes: 每层节点部门列表
        :return:
        """
        data = []
        for root in nodes:
            router = {"value": root.id, "label": root.name, "order": root.order}
            sons = filter(lambda i: i.parent_id == root.id, depts)
            router["children"] = self.generate_tree_options(depts, sons)
            data.append(router)
        return data

    @classmethod
    def dept_order(cls, datas: list, order: str = "order", children: str = "children") -> list:
        """
        部门排序
        :param datas:
        :param order:
        :param children:
        :return:
        """
        result = sorted(datas, key=lambda dept: dept[order])
        for item in result:
            if item[children]:
                item[children] = sorted(item[children], key=lambda dept: dept[order])
        return result


class TestDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(TestDal, self).__init__(db, models.SysUser, schemas.UserSimpleOut)

    async def test(self):
        # print("-----------------------开始------------------------")
        options = [joinedload(self.model.roles)]
        v_join = [[self.model.roles]]
        v_where = [self.model.id == 1, models.SysRole.id == 1]
        v_start_sql = select(self.model)
        result, count = await self.get_datas(
            v_start_sql=v_start_sql,
            v_join=v_join,
            v_options=options,
            v_where=v_where,
            v_return_count=True
        )
        if result:
            print(result)
            print(count)
        # print("-----------------------结束------------------------")

class DictTypeDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DictTypeDal, self).__init__()
        self.db = db
        self.model = models.SysDictType
        self.schema = schemas.DictTypeSimpleOut

    async def get_dict_type_dicts(self, dict_types: list[str]) -> dict:
        """
        获取多个字典类型下的字典元素列表
        """
        data = {}
        options = [joinedload(self.model.dicts)]
        objs = await DictTypeDal(self.db).get_datas(
            limit=0,
            v_return_objs=True,
            v_options=options,
            dict_type=("in", dict_types)
        )
        for obj in objs:
            if not obj:
                data[obj.dict_type] = []
                continue
            else:
                data[obj.dict_type] = [schemas.DictSimpleOut.model_validate(i).model_dump() for i in obj.dicts]
        return data

    async def get_select_datas(self) -> list:
        """获取选择数据，全部数据"""
        sql = select(self.model)
        queryset = await self.db.execute(sql)
        return [schemas.DictTypeOptionsOut.model_validate(i).model_dump() for i in queryset.scalars().all()]


# class DictDal(DalBase):
#
#     def __init__(self, db: AsyncSession):
#         super(DictDal, self).__init__()
#         self.db = db
#         self.model = models.SysDict
#         self.schema = schemas.DictSimpleOut
#
#
# class SettingsDal(DalBase):
#
#     def __init__(self, db: AsyncSession):
#         super(SettingsDal, self).__init__()
#         self.db = db
#         self.model = models.SysSetting
#         self.schema = schemas.SettingsSimpleOut
#
#     async def get_tab_values(self, tab_id: int) -> dict:
#         """
#         获取系统配置标签下的信息
#         """
#         datas = await self.get_datas(limit=0, tab_id=tab_id, v_return_objs=True)
#         result = {}
#         for data in datas:
#             if not data.disabled:
#                 result[data.config_key] = data.config_value
#         return result
#
#     async def update_datas(self, datas: dict, request: Request) -> None:
#         """
#         更新系统配置信息
#
#         更新ico图标步骤：先将文件上传到本地，然后点击提交后，获取到文件地址，将上传的新文件覆盖原有文件
#         原因：ico图标的路径是在前端的index.html中固定的，所以目前只能改变图片，不改变路径
#         """
#         for key, value in datas.items():
#             if key == "web_ico":
#                 continue
#             elif key == "web_ico_local_path":
#                 if not value:
#                     continue
#                 ico = await self.get_data(config_key="web_ico", tab_id=1)
#                 web_ico = datas.get("web_ico")
#                 if ico.config_value == web_ico:
#                     continue
#                 # 将上传的ico路径替换到static/system/favicon.ico文件
#                 await FileManage.async_copy_file(value, os.path.join(STATIC_ROOT, "system/favicon.ico"))
#                 sql = update(self.model).where(self.model.config_key == "web_ico").values(config_value=web_ico)
#                 await self.db.execute(sql)
#             else:
#                 sql = update(self.model).where(self.model.config_key == str(key)).values(config_value=value)
#                 await self.db.execute(sql)
#         if "wx_server_app_id" in datas and REDIS_DB_ENABLE:
#             rd = redis_getter(request)
#             await rd.client().set("wx_server", json.dumps(datas))
#         elif "sms_access_key" in datas and REDIS_DB_ENABLE:
#             rd = redis_getter(request)
#             await rd.client().set('aliyun_sms', json.dumps(datas))
#
#     async def get_base_config(self) -> dict:
#         """
#         获取系统基本信息
#         """
#         ignore_configs = ["wx_server_app_id", "wx_server_app_secret"]
#         datas = await self.get_datas(limit=0, tab_id=("in", ["1", "9"]), disabled=False, v_return_objs=True)
#         result = {}
#         for config in datas:
#             if config.config_key not in ignore_configs:
#                 result[config.config_key] = config.config_value
#         return result
#
#
# class SettingsTabDal(DalBase):
#
#     def __init__(self, db: AsyncSession):
#         super(SettingsTabDal, self).__init__(db, models.SysSettingTab, schemas.SettingsTabSimpleOut)
#
#     async def get_classify_tab_values(self, classify: list[str], hidden: bool | None = False) -> dict:
#         """
#         获取系统配置分类下的标签信息
#         """
#         model = models.SysSettingTab
#         options = [joinedload(model.settings)]
#         datas = await self.get_datas(
#             limit=0,
#             v_options=options,
#             classify=("in", classify),
#             disabled=False,
#             v_return_objs=True,
#             hidden=hidden
#         )
#         return self.__generate_values(datas)
#
#     async def get_tab_name_values(self, tab_names: list[str], hidden: bool | None = False) -> dict:
#         """
#         获取系统配置标签下的标签信息
#         """
#         model = models.SysSettingsTab
#         options = [joinedload(model.settings)]
#         datas = await self.get_datas(
#             limit=0,
#             v_options=options,
#             tab_name=("in", tab_names),
#             disabled=False,
#             v_return_objs=True,
#             hidden=hidden
#         )
#         return self.__generate_values(datas)
#
#     @classmethod
#     def __generate_values(cls, datas: list[models.SysSettingTab]) -> dict:
#         """
#         生成字典值
#         """
#         return {
#             tab.tab_name: {
#                 item.config_key: item.config_value
#                 for item in tab.settings
#                 if not item.disabled
#             }
#             for tab in datas
#         }
#
#
# class TaskDal(MongoManage):
#
#     class JobOperation(Enum):
#         add = "add_job"
#
#     def __init__(self, db: AsyncIOMotorDatabase):
#         super(TaskDal, self).__init__(db, "vadmin_system_task", schemas.TaskSimpleOut)
#
#     async def get_task(
#             self,
#             _id: str = None,
#             v_return_none: bool = False,
#             v_schema: Any = None,
#             **kwargs
#     ) -> dict | None:
#         """
#         获取单个数据，默认使用 ID 查询，否则使用关键词查询
#
#         包括临时字段 last_run_datetime，is_active
#         is_active: 只有在 scheduler_task_jobs 任务运行表中存在相同 _id 才表示任务添加成功，任务状态才为 True
#         last_run_datetime: 在 scheduler_task_record 中获取该任务最近一次执行完成的时间
#
#         :param _id: 数据 ID
#         :param v_return_none: 是否返回空 None，否则抛出异常，默认抛出异常
#         :param v_schema: 指定使用的序列化对象
#         """
#         if _id:
#             kwargs["_id"] = ("ObjectId", _id)
#
#         params = self.filter_condition(**kwargs)
#         pipeline = [
#             {
#                 '$addFields': {
#                     'str_id': {'$toString': '$_id'}
#                 }
#             },
#             {
#                 '$lookup': {
#                     'from': 'scheduler_task_jobs',
#                     'localField': 'str_id',
#                     'foreignField': '_id',
#                     'as': 'matched_jobs'
#                 }
#             },
#             {
#                 '$lookup': {
#                     'from': 'scheduler_task_record',
#                     'localField': 'str_id',
#                     'foreignField': 'job_id',
#                     'as': 'matched_records'
#                 }
#             },
#             {
#                 '$addFields': {
#                     'is_active': {
#                         '$cond': {
#                             'if': {'$ne': ['$matched_jobs', []]},
#                             'then': True,
#                             'else': False
#                         }
#                     },
#                     'last_run_datetime': {
#                         '$ifNull': [
#                             {'$arrayElemAt': ['$matched_records.created_at', -1]},
#                             None
#                         ]
#                     }
#                 }
#             },
#             {
#                 '$project': {
#                     'matched_records': 0,
#                     'matched_jobs': 0
#                 }
#             },
#             {
#                 '$match': params
#             },
#             {
#                 '$facet': {
#                     'documents': [
#                         {'$limit': 1},
#                     ]
#                 }
#             }
#         ]
#         # 执行聚合查询
#         cursor = self.collection.aggregate(pipeline)
#         result = await cursor.to_list(length=None)
#         data = result[0]['documents']
#         if not data and v_return_none:
#             return None
#         elif not data:
#             raise CustomException("未查找到对应数据", code=status.HTTP_404_NOT_FOUND)
#         data = data[0]
#         if data and v_schema:
#             return jsonable_encoder(v_schema(**data))
#         return data
#
#     async def get_tasks(
#             self,
#             page: int = 1,
#             limit: int = 10,
#             v_schema: Any = None,
#             v_order: str = None,
#             v_order_field: str = None,
#             **kwargs
#     ) -> tuple:
#         """
#         获取任务信息列表
#
#         添加了两个临时字段
#         is_active: 只有在 scheduler_task_jobs 任务运行表中存在相同 _id 才表示任务添加成功，任务状态才为 True
#         last_run_datetime: 在 scheduler_task_record 中获取该任务最近一次执行完成的时间
#         """
#         v_order_field = v_order_field if v_order_field else 'created_at'
#         v_order = -1 if v_order in self.ORDER_FIELD else 1
#         params = self.filter_condition(**kwargs)
#         pipeline = [
#             {
#                 '$addFields': {
#                     'str_id': {'$toString': '$_id'}
#                 }
#             },
#             {
#                 '$lookup': {
#                     'from': 'scheduler_task_jobs',
#                     'localField': 'str_id',
#                     'foreignField': '_id',
#                     'as': 'matched_jobs'
#                 }
#             },
#             {
#                 '$lookup': {
#                     'from': 'scheduler_task_record',
#                     'localField': 'str_id',
#                     'foreignField': 'job_id',
#                     'as': 'matched_records'
#                 }
#             },
#             {
#                 '$addFields': {
#                     'is_active': {
#                         '$cond': {
#                             'if': {'$ne': ['$matched_jobs', []]},
#                             'then': True,
#                             'else': False
#                         }
#                     },
#                     'last_run_datetime': {
#                         '$ifNull': [
#                             {'$arrayElemAt': ['$matched_records.created_at', -1]},
#                             None
#                         ]
#                     }
#                 }
#             },
#             {
#                 '$project': {
#                     'matched_records': 0,
#                     'matched_jobs': 0
#                 }
#             },
#             {
#                 '$match': params
#             },
#             {
#                 '$facet': {
#                     'documents': [
#                         {'$sort': {v_order_field: v_order}},
#                         {'$limit': limit},
#                         {'$skip': (page - 1) * limit}
#                     ],
#                     'count': [{'$count': 'total'}]
#                 }
#             }
#         ]
#
#         # 执行聚合查询
#         cursor = self.collection.aggregate(pipeline)
#         result = await cursor.to_list(length=None)
#         datas = result[0]['documents']
#         count = result[0]['count'][0]['total'] if result[0]['count'] else 0
#         if count == 0:
#             return [], 0
#         elif v_schema:
#             datas = [jsonable_encoder(v_schema(**data)) for data in datas]
#         elif self.schema:
#             datas = [jsonable_encoder(self.schema(**data)) for data in datas]
#         return datas, count
#
#     async def add_task(self, rd: Redis, data: dict) -> int:
#         """
#         添加任务到消息队列
#
#         使用消息无保留策略：无保留是指当发送者向某个频道发送消息时，如果没有订阅该频道的调用方，就直接将该消息丢弃。
#
#         :param rd: redis 对象
#         :param data: 行数据字典
#         :return: 接收到消息的订阅者数量。
#         """
#         exec_strategy = data.get("exec_strategy")
#         job_params = {
#             "name": data.get("_id"),
#             "job_class": data.get("job_class"),
#             "expression": data.get("expression")
#         }
#         if exec_strategy == "interval" or exec_strategy == "cron":
#             job_params["start_date"] = data.get("start_date")
#             job_params["end_date"] = data.get("end_date")
#         message = {
#             "operation": self.JobOperation.add.value,
#             "task": {
#                 "exec_strategy": data.get("exec_strategy"),
#                 "job_params": job_params
#             }
#         }
#         return await rd.publish(SUBSCRIBE, json.dumps(message).encode('utf-8'))
#
#     async def create_task(self, rd: Redis, data: schemas.Task) -> dict:
#         """
#         创建任务
#         """
#         data_dict = data.model_dump()
#         is_active = data_dict.pop('is_active')
#         insert_result = await super().create_data(data_dict)
#         obj = await self.get_task(insert_result.inserted_id, v_schema=schemas.TaskSimpleOut)
#
#         # 如果分组不存在则新增分组
#         group = await TaskGroupDal(self.db).get_data(value=data.group, v_return_none=True)
#         if not group:
#             await TaskGroupDal(self.db).create_data({"value": data.group})
#
#         result = {
#             "subscribe_number": 0,
#             "is_active": is_active
#         }
#
#         if is_active:
#             # 创建任务成功后, 如果任务状态为 True，则向消息队列中发送任务
#             result['subscribe_number'] = await self.add_task(rd, obj)
#         return result
#
#     async def put_task(self, rd: Redis, _id: str, data: schemas.Task) -> dict:
#         """
#         更新任务
#         """
#         data_dict = data.model_dump()
#         is_active = data_dict.pop('is_active')
#         await super(TaskDal, self).put_data(_id, data)
#         obj: dict = await self.get_task(_id, v_schema=schemas.TaskSimpleOut)
#
#         # 如果分组不存在则新增分组
#         group = await TaskGroupDal(self.db).get_data(value=data.group, v_return_none=True)
#         if not group:
#             await TaskGroupDal(self.db).create_data({"value": data.group})
#
#         try:
#             # 删除正在运行中的 Job
#             await SchedulerTaskJobsDal(self.db).delete_data(_id)
#         except CustomException as e:
#             pass
#
#         result = {
#             "subscribe_number": 0,
#             "is_active": is_active
#         }
#
#         if is_active:
#             # 更新任务成功后, 如果任务状态为 True，则向消息队列中发送任务
#             result['subscribe_number'] = await self.add_task(rd, obj)
#         return result
#
#     async def delete_task(self, _id: str) -> bool:
#         """
#         删除任务
#         """
#         result = await super(TaskDal, self).delete_data(_id)
#
#         try:
#             # 删除正在运行中的 Job
#             await SchedulerTaskJobsDal(self.db).delete_data(_id)
#         except CustomException as e:
#             pass
#         return result
#
#     async def run_once_task(self, rd: Redis, _id: str) -> int:
#         """
#         执行一次任务
#         """
#         obj: dict = await self.get_data(_id, v_schema=schemas.TaskSimpleOut)
#         message = {
#             "operation": self.JobOperation.add.value,
#             "task": {
#                 "exec_strategy": "once",
#                 "job_params": {
#                     "name": obj.get("_id"),
#                     "job_class": obj.get("job_class")
#                 }
#             }
#         }
#         return await rd.publish(SUBSCRIBE, json.dumps(message).encode('utf-8'))
#
#
# class TaskGroupDal(MongoManage):
#
#     def __init__(self, db: AsyncIOMotorDatabase):
#         super(TaskGroupDal, self).__init__(db, "vadmin_system_task_group")
#
#
# class TaskRecordDal(MongoManage):
#
#     def __init__(self, db: AsyncIOMotorDatabase):
#         super(TaskRecordDal, self).__init__(db, "scheduler_task_record")
#
#
# class SchedulerTaskJobsDal(MongoManage):
#
#     def __init__(self, db: AsyncIOMotorDatabase):
#         super(SchedulerTaskJobsDal, self).__init__(db, "scheduler_task_jobs", is_object_id=False)
