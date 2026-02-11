from core.event import lifespan
from utils.tools import import_modules
from application import urls
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles  # 依赖安装：pip install aiofiles
from core.docs import custom_api_docs
from core.exception import register_exception
from application.settings import settings
from starlette.responses import FileResponse
def create_app():
    """
    启动项目

    docs_url：配置交互文档的路由地址，如果禁用则为None，默认为 /docs
    redoc_url： 配置 Redoc 文档的路由地址，如果禁用则为None，默认为 /redoc
    openapi_url：配置接口文件json数据文件路由地址，如果禁用则为None，默认为/openapi.json
    """
    app = FastAPI(
        title="admin",
        description="本项目基于Fastapi与Vue3+Typescript+Vite4+element-plus的基础项目 前端基于vue-element-plus-admin框架开发",
        version=settings.VERSION,
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json"
    )
    print("create_app")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"STATIC_ENABLE: {settings.STATIC_ENABLE}")
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"DOCS_URL: {settings.DOCS_URL}")
    print(f"SWAGGER_CSS_URL: {settings.SWAGGER_CSS_URL}")
    print(f"SWAGGER_JS_URL: {settings.SWAGGER_JS_URL}")
    import_modules(settings.MIDDLEWARES, "中间件", app=app)
    # 全局异常捕捉处理
    register_exception(app)
    # 跨域解决
    if settings.CORS_ORIGIN_ENABLE:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_credentials=settings.ALLOW_CREDENTIALS,
            allow_methods=settings.ALLOW_METHODS,
            allow_headers=settings.ALLOW_HEADERS
        )
    # 挂在静态目录
    if settings.STATIC_ENABLE:
        static_url = settings.STATIC_URL
        static_root = settings.STATIC_ROOT
        print(f"Mounting static files: {static_url} -> {static_root}")
        app.mount(static_url, StaticFiles(directory=static_root))
    if settings.TEMP_ENABLE:
        app.mount(settings.TEMP_URL, StaticFiles(directory=settings.TEMP_DIR))
    app.mount(settings.WEB_URL, StaticFiles(directory=settings.WEB_DIR))

    # app.mount("/", StaticFiles(directory="static"), name="static")


    # 引入应用中的路由
    app.include_router(urls.api_router, prefix=settings.API_V1_STR)

    # async def async_startup_event():
    #     # 在启动事件中执行的异步操作
    #     print("Async startup event")
    #
    # # 注册启动事件处理函数
    # @app.on_event("startup")
    # async def startup_event():
    #     print("Starting up the application...")
    #     await async_startup_event()
    #     print("Application startup complete.")


    # 配置接口文档静态资源
    custom_api_docs(app)


    @app.get("/", include_in_schema=False)
    def read_root():
        return FileResponse("static/dist-pro/index.html")

    return app







