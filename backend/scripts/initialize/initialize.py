#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/11/23 11:21 
# @File           : initialize.py
# @IDE            : PyCharm
# @desc           : 简要说明

from enum import Enum
from sqlalchemy import insert
from core.database import db_getter
from utils.excel.excel_manage import ExcelManage
from application.settings import settings
import os
from apps.admin.system import models as system_models
from apps.admin.help import models as help_models
from apps.admin.iot import models as iot_models
import subprocess


class Environment(str, Enum):
    dev = "dev"
    pro = "pro"


class InitializeData:
    """
    初始化数据

    生成步骤：
        1. 读取数据
        2. 获取数据库
        3. 创建数据
    """

    SCRIPT_DIR = os.path.join(settings.BASE_DIR, 'scripts', 'initialize')

    def __init__(self):
        self.sheet_names = []
        self.datas = {}
        self.ex = None
        self.db = None
        self.__serializer_data()
        self.__get_sheet_data()

    @classmethod
    def migrate_model(cls, env: Environment = Environment.pro):
        print(settings.BASE_DIR)
        """
        模型迁移映射到数据库
        """
        subprocess.check_call(
            ['alembic', '--name', f'{env.value}', 'revision', '--autogenerate', '-m', f'{settings.VERSION}'],
            cwd=settings.BASE_DIR
        )
        subprocess.check_call(['alembic', '--name', f'{env.value}', 'upgrade', 'head'], cwd=settings.BASE_DIR)
        print(f"环境：{env}  {settings.VERSION} 数据库表迁移完成")

    def __serializer_data(self):
        """
        序列化数据，将excel数据转为python对象
        """
        self.ex = ExcelManage()
        self.ex.open_workbook(os.path.join(self.SCRIPT_DIR, 'data', 'init.xlsx'), read_only=True)
        self.sheet_names = self.ex.get_sheets()

    def __get_sheet_data(self):
        """
        获取工作区数据
        """
        for sheet in self.sheet_names:
            sheet_data = []
            self.ex.open_sheet(sheet)
            headers = self.ex.get_header()
            datas = self.ex.readlines(min_row=2, max_col=len(headers))
            for row in datas:
                sheet_data.append(dict(zip(headers, row)))
            self.datas[sheet] = sheet_data

    async def __generate_data(self, table_name: str, model):
        """
        生成数据

        :param table_name: 表名
        :param model: 数据表模型
        """
        async_session = db_getter()
        db = await async_session.__anext__()
        datas = self.datas.get(table_name)
        print(table_name,model,datas,"data")
        print(112555)
        await db.execute(insert(model), datas)
        print(112)
        await db.flush()
        await db.commit()
        print(f"{table_name} 表数据已生成")

    async def generate_menu(self):
        """
        生成菜单数据
        """
        await self.__generate_data("sys_menu", system_models.SysMenu)

    async def generate_role(self):
        """
        生成角色
        """
        await self.__generate_data("sys_role", system_models.SysRole)

    async def generate_user(self):
        """
        生成用户
        """
        await self.__generate_data("sys_user", system_models.SysUser)

    async def generate_user_role(self):
        """
        生成用户
        """
        await self.__generate_data("sys_user_role", system_models.sys_user_role)

    async def generate_system_tab(self):
        """
        生成系统配置分类数据
        """
        await self.__generate_data("sys_settings_tab", system_models.SysSettingTab)

    async def generate_system_config(self):
        """
        生成系统配置数据
        """
        await self.__generate_data("sys_settings", system_models.SysSetting)

    async def generate_dict_type(self):
        """
        生成字典类型数据
        """
        await self.__generate_data("sys_dict_type", system_models.SysDictType)

    async def generate_dict_details(self):
        """
        生成字典详情数据
        """
        await self.__generate_data("sys_dict", system_models.SysDict)

    async def generate_help_issue_category(self):
        """
        生成常见问题类别数据
        """
        await self.__generate_data("sys_help_issue_category", help_models.SysIssueCategory)

    async def generate_help_issue(self):
        """
        生成常见问题详情数据
        """
        await self.__generate_data("sys_help_issue", help_models.SysIssue)

    async def generate_iot_client(self):
        """
        生成iot Client数据
        """
        await self.__generate_data("iot_client", iot_models.IotClient)


    async def run(self, env: Environment = Environment.pro):
        """
        执行初始化工作
        """
        self.migrate_model(env)
        print("开始生成数据")
        await self.generate_menu()
        await self.generate_role()
        await self.generate_user()
        await self.generate_user_role()
        await self.generate_system_tab()
        await self.generate_dict_type()
        await self.generate_system_config()
        await self.generate_dict_details()
        await self.generate_help_issue_category()
        await self.generate_help_issue()

        await self.generate_iot_client()
        print(f"环境：{env} {VERSION} 数据已初始化完成")
