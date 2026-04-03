# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/19 15:47
# @File           : settings.py
# @IDE            : PyCharm
# @desc           : 主配置文件

import os
from fastapi.security import OAuth2PasswordBearer
from pathlib import Path
from functools import lru_cache
from typing import Any, Dict, List, Optional, Literal,ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict
from uvicorn.config import LifespanType
from urllib.parse import quote_plus
from application.config.enums import EnvironmentEnum


class Settings(BaseSettings):

    """
    系统版本
    """

    TITLE: str = "🎉 FastapiAdmin 🎉 -dev"  # 文档标题
    VERSION: str = '0.1.0'        # 版本号
    DESCRIPTION: str = "该项目是一个基于python的web服务框架，基于fastapi和sqlalchemy实现。"  # 文档描述
    SUMMARY: str = "接口汇总"      # 文档概述


    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf-8",
        extra='ignore',
        case_sensitive=True, # 区分大小写
    )

    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEV


    """安全警告: 不要在生产中打开调试运行!"""
    DEBUG: bool = True
    """是否开启演示功能：取消所有POST,DELETE,PUT操作权限"""
    DEMO: bool = False
    """演示功能白名单"""
    DEMO_WHITE_LIST_PATH: List[str] = [
        "/auth/login",
        "/auth/token/refresh",
        "/auth/wx/login",
        "/admin/system/dict/types/details",
        "/admin/system/settings/tabs",
        "/admin/resource/images",
        "/admin/auth/user/export/query/list/to/excel"
    ]

    API_V1_STR: str = "/api"
    
    
    
    # ================================================= #
    # ******************* 服务器配置 ****************** #
    # ================================================= #
    SERVER_HOST: str = '0.0.0.0'        # 允许访问的IP地址
    SERVER_PORT: int = 8001             # 服务端口
    RELOAD: bool = True                 # 是否自动重启
    FACTORY: bool = True                # 是否使用异步模式
    LIFESPAN: LifespanType = 'on'       # 生命周期模式
    WORKERS: int = 1                    # 启动进程数
    LIMIT_CONCURRENCY: int = 1000       # 最大并发连接数
    BACKLOG: int = 2048                 # 等待队列最大连接数
    LIMIT_MAX_REQUESTS: int = 4094      # HTTP最大请求数
    TIMEOUT_KEEP_ALIVE: int = 5         # 保持连接时间(秒)

    # """
    # 引入数据库配置
    # """
    # if DEBUG:
    #     from application.config.development import *
    # else:
    #     from application.config.production import *

    # """项目根目录"""
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    
    # 项目根目录
    BASE_DIR: Path = Path(__file__).parent.parent
    print(BASE_DIR,"base dir")
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URL: str = ""
    REDIS_DB_ENABLE: bool = False
    MONGO_DB_ENABLE: bool = False

    """
    是否开启登录认证
    只适用于简单的接口
    如果是与认证关联性比较强的接口，则无法使用
    """
    OAUTH_ENABLE: bool = True
    """
    配置 OAuth2 密码流认证方式
    官方文档：https://fastapi.tiangolo.com/zh/tutorial/security/first-steps/#fastapi-oauth2passwordbearer
    auto_error:(bool) 可选参数，默认为 True。当验证失败时，如果设置为 True，FastAPI 将自动返回一个 401 未授权的响应，如果设置为 False，你需要自己处理身份验证失败的情况。
    这里的 auto_error 设置为 False 是因为存在 OpenAuth：开放认证，无认证也可以访问，
    如果设置为 True，那么 FastAPI 会自动报错，即无认证时 OpenAuth 会失效，所以不能使用 True。
    """
    oauth2_scheme: Any = OAuth2PasswordBearer(tokenUrl="/auth/api/login", auto_error=False) if OAUTH_ENABLE else lambda: ""
    """安全的随机密钥，该密钥将用于对 JWT 令牌进行签名"""
    SECRET_KEY: str = 'vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=kbvqacjq75vzps$'
    """用于设定 JWT 令牌签名算法"""
    ALGORITHM: str = "HS256"
    """access_token 过期时间，一天"""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    """refresh_token 过期时间，用于刷新token使用，两天"""
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440 * 2
    """access_token 缓存时间，用于刷新token使用，30分钟"""
    ACCESS_TOKEN_CACHE_MINUTES: int = 30

    """
    挂载临时文件目录，并添加路由访问，此路由不会在接口文档中显示
    TEMP_ENABLE：是否启用临时文件目录访问
    TEMP_URL：路由访问
    TEMP_DIR：临时文件目录绝对路径
    官方文档：https://fastapi.tiangolo.com/tutorial/static-files/
    """
    TEMP_ENABLE: bool = True
    TEMP_URL: str = "/temp"
    TEMP_DIR: str = os.path.join(BASE_DIR, "temp")
    WEB_URL: str = "/assets"
    WEB_DIR: str = os.path.join(BASE_DIR, 'static', 'dist-pro', "assets")
    print(WEB_DIR)

    FILE_URL: str = "/files"
    FILE_DIR: str = os.path.join(BASE_DIR, "files")

    # ================================================= #
    # ******************* Gzip压缩配置 ******************* #
    # ================================================= #
    GZIP_ENABLE: bool = True        # 是否启用Gzip
    GZIP_MIN_SIZE: int = 1000       # 最小压缩大小(字节)
    GZIP_COMPRESS_LEVEL: int = 9    # 压缩级别(1-9)

    # ================================================= #
    # ***************** 静态文件配置 ***************** #
    # ================================================= #
    """
    挂载静态目录，并添加路由访问，此路由不会在接口文档中显示
    STATIC_ENABLE：是否启用静态目录访问
    STATIC_URL：路由访问
    STATIC_ROOT：静态文件目录绝对路径
    官方文档：https://fastapi.tiangolo.com/tutorial/static-files/
    """
    STATIC_ENABLE: bool = True
    STATIC_URL: str = "/media"
    STATIC_DIR: str = "static"
    STATIC_ROOT: str = os.path.join(BASE_DIR, STATIC_DIR)


    DOCS_URL: str = "/docs"      # Swagger UI路径
    REDOC_URL: str = "/redoc"    # ReDoc路径

    # ================================================= #
    # ***************** Swagger配置 ***************** #
    # ================================================= #
    SWAGGER_CSS_URL: str = "/media/swagger/swagger-ui/swagger-ui.css"
    SWAGGER_JS_URL: str = "/media/swagger/swagger-ui/swagger-ui-bundle.js"
    REDOC_JS_URL: str = "/media/swagger/redoc/bundles/redoc.standalone.js"
    FAVICON_URL: str = "/media/swagger/favicon.png"


    # 数据库类型
    DATABASE_TYPE: Literal['mysql', 'postgres'] = 'mysql'
    
    # MySQL/PostgreSQL数据库连接
    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = 'root'
    DATABASE_PASSWORD: str = 'ServBay.dev'
    DATABASE_NAME: str = 'fastapi_app'
    

    # ================================================= #
    # ******************** Redis配置 ******************* #
    # ================================================= #
    REDIS_ENABLE: bool = True  # 是否启用Redis
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB_NAME: int = 1
    REDIS_USER: str = ''
    REDIS_PASSWORD: str = ''

    # ================================================= #
    # ***************** 模版文件配置 ***************** #
    # ================================================= #
    TEMPLATE: str = "templates"
    TEMPLATE_DIR: Path = BASE_DIR.joinpath(TEMPLATE)

    # ================================================= #
    # ***************** 动态文件配置 ***************** #
    # ================================================= #
    UPLOAD_FILE_PATH: Path = Path('static/upload')    # 上传目录
    UPLOAD_MACHINE: str = 'A'                         # 上传机器标识
    ALLOWED_EXTENSIONS: list[str] = [                 # 允许的文件类型
        # 图片
        '.bmp', '.gif', '.jpg', '.jpeg', '.png', '.ico', '.svg',
        # 文档
        '.csv', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.html', '.htm', '.txt', '.pdf',
        # 压缩包
        '.rar', '.zip', '.gz', '.bz2',
        # 视频
        '.mp4', '.avi', '.rmvb'
    ]
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 最大文件大小(10MB)


    """
    跨域解决
    详细解释：https://cloud.tencent.com/developer/article/1886114
    官方文档：https://fastapi.tiangolo.com/tutorial/cors/
    """
    # 是否启用跨域
    CORS_ORIGIN_ENABLE: bool = True
    # 只允许访问的域名列表，* 代表所有
    ALLOW_ORIGINS: List[str] = ["*"]
    # 是否支持携带 cookie
    ALLOW_CREDENTIALS: bool = True
    # 设置允许跨域的http方法，比如 get、post、put等。
    ALLOW_METHODS: List[str] = ["*"]
    # 允许携带的headers，可以用来鉴别来源等作用。
    ALLOW_HEADERS: List[str] = ["*"]

    """
    全局事件配置
    """
    
    @property
    def EVENT_LIST(self) -> List[Optional[str]]:
        """获取事件列表"""
        EVENTS: List[Optional[str]] = [
        "core.event.connect_mongo" if self.MONGO_DB_ENABLE else None,
        "core.event.connect_redis" if self.REDIS_DB_ENABLE else None,
        # "core.event.connect_mqtt",
        "core.event.init_ap_scheduler"
        ]
        return EVENTS


    # """
    # 阿里云对象存储OSS配置
    # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # *  [accessKeyId] {String}：通过阿里云控制台创建的AccessKey。
    # *  [accessKeySecret] {String}：通过阿里云控制台创建的AccessSecret。
    # *  [bucket] {String}：通过控制台或PutBucket创建的bucket。
    # *  [endpoint] {String}：bucket所在的区域， 默认oss-cn-hangzhou。
    # """
    ALIYUN_OSS = {
        "accessKeyId": "accessKeyId",
        "accessKeySecret": "accessKeySecret",
        "endpoint": "endpoint",
        "bucket": "bucket",
        "baseUrl": "baseUrl"
    }
    # 阿里云对象存储OSS配置
    ALIYUN_OSS: ClassVar[Dict[str, Any]] = {
    "accessKeyId": "accessKeyId",
    "accessKeySecret": "accessKeySecret",
    "endpoint": "endpoint",
    "bucket": "bucket",
    "baseUrl": "baseUrl"
}

    # ================================================= #
    # ******************** 验证码配置 ******************* #
    # ================================================= #
    CAPTCHA_ENABLE: bool = True                              # 是否启用验证码
    CAPTCHA_EXPIRE_SECONDS: int = 60 * 1                     # 验证码过期时间(秒) 1分钟
    CAPTCHA_FONT_SIZE: int = 40                              # 字体大小
    CAPTCHA_FONT_PATH: str = 'static/assets/font/Arial.ttf'  # 字体路径

    
    #MQTT配置
    MQTT_HOST :str='192.168.4.4'
    MQTT_USER :str ='corxadmin'
    MQTT_PASSWORD:str = '1qaz@WSX'
    MQTT_PORT:int = 1883

    # ================================================= #
    # ******************* GM配置 ********************** #
    # ================================================= #
    # GM（掘金量化）配置
    GM_TOKEN: str = '2d2a05e9ba6eac1de131cea8a509fd3216efd9af'  # GM（掘金量化）API token

    # ================================================= #
    # ******************* Stock Service配置 ********** #
    # ================================================= #
    # Stock Service（股票数据服务）配置
    STOCK_SERVICE_URL: str = 'http://localhost:8008'  # Stock Service 基础URL

    # ================================================= #
    # ******************* 邮件配置 ********************* #
    # ================================================= #
    SMTP_HOST: str = 'smtp.example.com'
    SMTP_PORT: int = 465
    SMTP_USER: str = ''
    SMTP_PASSWORD: str = ''
    SMTP_FROM: str = ''

    # ================================================= #
    # ******************* 微信推送配置 ***************** #
    # ================================================= #
    # 支持 Server酱/WxPusher 等第三方服务
    WECHAT_PUSH_TYPE: str = 'serverchan'  # serverchan / wxpusher / custom
    WECHAT_PUSH_URL: str = ''  # 自定义推送 URL (可选)

    # """
    # 其他项目配置
    # """
    # 默认密码，"0" 默认为手机号后六位
    DEFAULT_PASSWORD: str = "0"
    # 默认头像
    DEFAULT_AVATAR: str = "https://vv-reserve.oss-cn-hangzhou.aliyuncs.com/avatar/2023-01-27/1674820804e81e7631.png"
    # 默认登陆时最大输入密码或验证码错误次数
    DEFAULT_AUTH_ERROR_MAX_NUMBER: int = 5
    # 是否开启保存登录日志
    LOGIN_LOG_RECORD: bool = True
    # 是否开启保存设备操作日志
    ACTION_LOG_RECORD: bool = True
    # 是否开启保存每次请求日志到本地
    REQUEST_LOG_RECORD: bool = True
    # 是否开启每次操作日志记录到MongoDB数据库
    # OPERATION_LOG_RECORD: bool = True
    # 只记录包括的请求方式操作到MongoDB数据库
    # OPERATION_RECORD_METHOD: List[str] = ["POST", "PUT", "DELETE"]
    # 忽略的操作接口函数名称，列表中的函数名称不会被记录到操作日志中
    # IGNORE_OPERATION_FUNCTION: List[str] = ["post_dicts_details"]
    # ================================================= #
    # ********************* 日志配置 ******************* #
    # ================================================= #
    LOGGER_DIR: Path = BASE_DIR.joinpath('logs')
    LOGGER_FORMAT: str = '%(asctime)s - %(levelname)8s - [%(name)s:%(filename)s:%(funcName)s:%(lineno)d] %(message)s' # 日志格式
    LOGGER_LEVEL: str = 'INFO'                                                                      # 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    BACKUPCOUNT: int = 10                                                                           # 日志文件备份数
    WHEN: str = 'MIDNIGHT'                                                                          # 日志分割时间 (MIDNIGHT, H, D, W0-W6)
    INTERVAL: int = 1                                                                               # 日志分割间隔
    ENCODING: str = 'utf-8'                                                                         # 日志编码
    LOG_RETENTION_DAYS: int = 30                                                                    # 日志保留天数，超过此天数的日志文件将被自动清理
    OPERATION_LOG_RECORD: bool = True                                                               # 是否记录操作日志
    IGNORE_OPERATION_FUNCTION: List[str] = ["get_captcha_for_login","post_dicts_details"]                                # 忽略记录的函数
    OPERATION_RECORD_METHOD: List[str] = ["POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]      # 需要记录的请求方法


    # 中间件配置
    MIDDLEWARES: List[Optional[str]] = [
        "core.middleware.register_request_log_middleware" if REQUEST_LOG_RECORD else None,
        "core.middleware.register_operation_record_middleware" if OPERATION_LOG_RECORD else None,
        "core.middleware.register_demo_env_middleware" if DEMO else None,
        "core.middleware.register_jwt_refresh_middleware"
    ]

    # 定时任务配置
    # 发布/订阅通道，与定时任务程序相互关联，请勿随意更改
    SUBSCRIBE: str = 'kinit_queue'


    # """
    # 获取IP地址归属地
    # 文档：https://user.ip138.com/ip/doc
    # """
    IP_PARSE_ENABLE :bool = False
    IP_PARSE_TOKEN :str= "IP_PARSE_TOKEN"

    
    # ================================================= #
    # ******************* 重构配置 ******************* #
    # ================================================= #
    @property
    def MIDDLEWARE_LIST(self) -> List[Optional[str]]:
        """获取项目根目录"""
        # 中间件列表
        MIDDLEWARES: List[Optional[str]] = [
            "app.core.middlewares.CustomCORSMiddleware" if self.CORS_ORIGIN_ENABLE else None,
            "app.core.middlewares.RequestLogMiddleware" if self.OPERATION_LOG_RECORD else None,
            "app.core.middlewares.CustomGZipMiddleware" if self.GZIP_ENABLE else None,
        ]
        return MIDDLEWARES



    @property
    def ASYNC_DB_URI(self) -> str:
        """获取异步数据库连接"""
        if self.DATABASE_TYPE == "mysql":
            return f"mysql+asyncmy://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}?charset=utf8mb4"
        elif self.DATABASE_TYPE == "postgres":
            return f"postgresql+asyncpg://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        else:
            raise ValueError(f"数据库驱动不支持: {self.DATABASE_TYPE}, 请选择 请选择 mysql、postgres")

    @property
    def DB_URI(self) -> str:
        """获取同步数据库连接"""
        if self.DATABASE_TYPE == "mysql":
            return f"mysql+pymysql://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}?charset=utf8mb4"
        elif self.DATABASE_TYPE == "postgres":
            return f"postgresql+psycopg2://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        else:
            raise ValueError(f"数据库驱动不支持: {self.DATABASE_TYPE}, 请选择 mysql、postgres")
    
    @property
    def REDIS_URI(self) -> str:
        """获取Redis连接"""
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_NAME}"
    
    @property
    def FASTAPI_CONFIG(self) -> dict[str, Any]:
        """获取FastAPI应用属性"""
        return {
            "debug": self.DEBUG,
            "title": self.TITLE,
            "version": self.VERSION,
            "description": self.DESCRIPTION,
            "summary": self.SUMMARY,
            "docs_url": None,
            "redoc_url": None,
            "root_path": self.API_V1_STR
        }

    @property
    def UVICORN_CONFIG(self) -> Dict[str, Any]:
        """获取Uvicorn配置"""
        # 确保日志目录存在
        self.LOGGER_DIR.mkdir(parents=True, exist_ok=True)
        
        return {
            "host": self.SERVER_HOST,
            "port": self.SERVER_PORT,
            "reload": self.RELOAD,
            "log_config": None,
            "workers": self.WORKERS,
            "limit_concurrency": self.LIMIT_CONCURRENCY,
            "backlog": self.BACKLOG,
            "limit_max_requests": self.LIMIT_MAX_REQUESTS,
            "timeout_keep_alive": self.TIMEOUT_KEEP_ALIVE,
            "lifespan": self.LIFESPAN,
            "factory": self.FACTORY,
        }

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """获取配置实例"""
    env = os.getenv('ENVIRONMENT', EnvironmentEnum.DEV.value)
    if env not in [e.value for e in EnvironmentEnum]:
        raise ValueError(f"无效的环境配置: {env}")
    
    env_file = Path(__file__).parent.parent / "env" / f".env.{env}"
    if not env_file.exists():
        raise FileNotFoundError(f"环境配置文件不存在: {env_file}")

    return Settings(_env_file=env_file)

settings = get_settings()
