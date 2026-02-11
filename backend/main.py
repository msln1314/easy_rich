# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/19 15:47
# @File           : main.py
# @IDE            : PyCharm
# @desc           : 主程序入口

"""
FastApi 更新文档：https://github.com/tiangolo/fastapi/releases
FastApi Github：https://github.com/tiangolo/fastapi
Typer 官方文档：https://typer.tiangolo.com/
"""



import typer
shell_app = typer.Typer()
import uvicorn
from scripts.initialize.initialize import InitializeData, Environment
import asyncio
from scripts.create_app.main import CreateApp
print("shell",shell_app)
from core.event import lifespan
from utils.tools import import_modules
from application import urls
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles  # 依赖安装：pip install aiofiles
from application.settings import settings


from main_app import create_app
@shell_app.command()
def run(
        host: str = typer.Option(default='0.0.0.0', help='监听主机IP，默认开放给本网络所有主机'),
        port: int = typer.Option(default=9000, help='监听端口')
):
    """
    启动项目

    factory: 在使用 uvicorn.run() 启动 ASGI 应用程序时，可以通过设置 factory 参数来指定应用程序工厂。
    应用程序工厂是一个返回 ASGI 应用程序实例的可调用对象，它可以在启动时动态创建应用程序实例。
    """


    uvicorn.run(app='main:create_app', host=host, port=port, lifespan="on", factory=True,reload=settings.DEBUG)


# if __name__ == "__main__":
#     uvicorn.run(app='main:create_app', host='127.0.0.1', port=44, lifespan="on", factory=True, reload=True)
@shell_app.command()
def init(env: Environment = Environment.pro):
    print(env)
    """
    初始化数据

    在执行前一定要确认要操作的环境与application/settings.DEBUG 设置的环境是一致的，
    不然会导致创建表和生成数据不在一个数据库中！！！！！！！！！！！！！！！！！！！！！！

    比如要初始化开发环境，那么env参数应该为 dev，并且 application/settings.DEBUG 应该 = True
    比如要初始化生产环境，那么env参数应该为 pro，并且 application/settings.DEBUG 应该 = False

    :param env: 数据库环境
    """
    print("开始初始化数据")
    data = InitializeData()
    asyncio.run(data.run(env))


@shell_app.command()
def migrate(env: Environment = Environment.pro):
    """
    将模型迁移到数据库，更新数据库表结构

    :param env: 数据库环境
    """
    print("开始更新数据库表")
    InitializeData.migrate_model(env)


@shell_app.command()
def init_app(path: str):
    """
    自动创建初始化 APP 结构

    命令例子：python main.py init-app admin/test

    :param path: app 路径，根目录为apps，填写apps后面路径即可，例子：admin/auth
    """
    print(f"开始创建并初始化 {path} APP")
    init_app = CreateApp(path)
    init_app.run()


if __name__ == '__main__':
    print("statr")
    shell_app()
