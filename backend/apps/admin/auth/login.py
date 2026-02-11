# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 安全认证视图

"""
JWT 表示 「JSON Web Tokens」。https://jwt.io/

它是一个将 JSON 对象编码为密集且没有空格的长字符串的标准。

通过这种方式，你可以创建一个有效期为 1 周的令牌。然后当用户第二天使用令牌重新访问时，你知道该用户仍然处于登入状态。
一周后令牌将会过期，用户将不会通过认证，必须再次登录才能获得一个新令牌。

我们需要安装 python-jose 以在 Python 中生成和校验 JWT 令牌：pip install python-jose[cryptography]

PassLib 是一个用于处理哈希密码的很棒的 Python 包。它支持许多安全哈希算法以及配合算法使用的实用程序。
推荐的算法是 「Bcrypt」：pip install passlib[bcrypt]
"""

from datetime import timedelta
import traceback
from fastapi import APIRouter, Depends, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter
from core.exception import CustomException
from sqlalchemy import or_
from core.validator import valid_phone
from utils import status
from utils.response import SuccessResponse, ErrorResponse
from application.settings import settings
from apps.admin.auth.utils.login_manage import LoginManage
from apps.admin.auth.utils.validation import LoginForm, WXLoginForm
from apps.admin.log.crud.login_log import LoginLogDal
from apps.admin.system.crud import MenuDal, UserDal, SettingsDal,SettingsTabDal
from apps.admin.system.models import SysUser
from apps.admin.system.schemas.user import UserIn
from apps.admin.auth.utils.current import FullAdminAuth
from apps.admin.auth.utils.validation.auth import Auth
from utils.wx.oauth import WXOAuth
from utils.sms.code_manager import CodeManager
import jwt
from core.logger import logger
from utils.re_util import is_valid_email,is_valid_phone



app = APIRouter()


class SendCodeRequest(BaseModel):
    username: str  # 手机号或邮箱



class RegisterRequest(BaseModel):
    username: str  # 手机号或邮箱
    code: str  # 验证码
    password: str  # 密码


@app.post("/send/code", summary="发送验证码", description="发送手机短信或邮箱验证码")
async def send_code(
        request: Request,
        data: SendCodeRequest,
        db: AsyncSession = Depends(db_getter)
):
    """
    发送验证码，支持手机短信和邮箱
    """
    # 验证账号是否存在
   

    # 尝试通过手机号或邮箱查询用户
    user = None
    # 首先尝试判断是否是手机号
 
    is_phone = is_valid_phone(data.username)
    is_email = is_valid_email(data.username)
    
    if is_phone:
        user = await UserDal(db).get_data(phone=data.username, v_return_none=True)
    elif is_email:
        user = await UserDal(db).get_data(email=data.username, v_return_none=True)
    print(user,"user11")
    # if not user:
    #     return ErrorResponse(msg="该账号不存在")

    # 根据获取验证码的账户判断发送目标
    # 如果是手机号登录，发送到手机号；如果是邮箱登录，发送到邮箱
    send_to = data.username
    is_email = not is_phone

    # 如果是邮箱验证码，获取邮箱配置
    web_email = None
    if is_email:
  
        web_email_settings_data = await SettingsTabDal(db).get_tab_name_values(tab_names=['web_email'])  # 获取邮箱配置
        settings_data = web_email_settings_data.get('web_email')
        
        if settings_data:
            web_email = {
                "email_access": settings_data.get("email_access"),
                "email_password": settings_data.get("email_password"),
                "email_server": settings_data.get("email_server"),
                "email_port": settings_data.get("email_port")
            }

    # 发送验证码s
    try:
        code_manager = CodeManager(
            send_to,
            web_email=web_email,
            user_id=user.id if user else None, 
            ip_address=request.client.host,
            scene="login",
            db=db
        )
        result = await code_manager.send_code()
        if result:
            return SuccessResponse(msg="验证码已发送")
        else:
            return ErrorResponse(msg="验证码发送失败")
    except CustomException as e:
        logger.error(f"发送验证码失败: {traceback.print_exc()}")
     
        return ErrorResponse(msg=e.msg)
    except Exception as e:
        print(f"发送验证码失败: {e}")
        return ErrorResponse(msg="验证码发送失败")


@app.post("/register", summary="用户注册", description="使用手机号或邮箱注册")
async def register(
        request: Request,
        data: RegisterRequest,
        db: AsyncSession = Depends(db_getter)
):
    """
    用户注册接口
    """
   
    # 判断 username 是手机号还是邮箱


    is_phone = is_valid_phone(data.username)
    is_email = is_valid_email(data.username)


    # 检查用户是否已存在
    if is_phone:
        existing_user = await UserDal(db).get_data(phone=data.username, v_return_none=True)
        if existing_user:
            return ErrorResponse(msg="该手机号已注册")
    elif is_email:
        existing_user = await UserDal(db).get_data(email=data.username, v_return_none=True)
        if existing_user:
            return ErrorResponse(msg="该邮箱已注册")
    else:
        return ErrorResponse(msg="请输入正确的手机号或邮箱")

    # 验证验证码
    code_manager = CodeManager(data.username, db=db)
    is_valid = await code_manager.verify_code(data.code)
    if not is_valid:
        return ErrorResponse(msg="验证码错误或已过期")

    # 创建用户
    user_data = UserIn(
        phone= data.username if is_phone else None,
        email=data.username if not is_phone else None,
        password=data.password,
        name=data.username if is_phone else data.username.split('@')[0],
        nickname=data.username if is_phone else data.username.split('@')[0],
        is_active=True,
        is_staff=True,
        is_admin=False,
        gender="0",
        dept_id=1
    )

    user = await UserDal(db).create_data(data=user_data, ext_obj={})

    return SuccessResponse(msg="注册成功", data={"id": user.get('id'), "username": data.username})


@app.post("/api/login", summary="API 手机号密码登录", description="Swagger API 文档登录认证")
async def api_login_for_access_token(
        request: Request,
        data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(db_getter)
):
    # 尝试通过手机号或邮箱查询用户

    # 先尝试手机号查询
    user = await UserDal(db).get_data(phone=data.username, v_return_none=True)
    if not user:
        # 再尝试邮箱查询
        user = await UserDal(db).get_data(email=data.username, v_return_none=True)

    if not user:
        raise CustomException(status_code=401, code=401, msg="该账号不存在")
    result = SysUser.verify_password(data.password, user.password)
    if not result:
        raise CustomException(status_code=401, code=401, msg="账号或密码错误")
    if not user.is_active:
        raise CustomException(status_code=401, code=401, msg="此账号已被冻结")
    elif not user.is_staff:
        raise CustomException(status_code=401, code=401, msg="此账号无权限")
    access_token = LoginManage.create_token({"sub": user.phone})
    record = LoginForm(platform='2', method='0', username=data.username, password=data.password)
    resp = {"access_token": access_token, "token_type": "bearer"}
    await LoginLogDal(db).create_login_record(record, True, request, resp)
    return resp


@app.post("/login", summary="手机号密码登录", description="员工登录通道，限制最多输错次数，达到最大值后将is_active=False")
async def login_for_access_token(
        request: Request,
        data: LoginForm,
        manage: LoginManage = Depends(),
        db: AsyncSession = Depends(db_getter)
):
    try:
        print(data,"data")
        if data.method == "0":
            result = await manage.password_login(data, db, request)
        elif data.method == "1":
            result = await manage.sms_login(data, db, request)
        else:
            raise ValueError("无效参数")
        print(result)
        if not result.status:
            raise ValueError(result.msg)

        access_token = LoginManage.create_token({"sub": result.user.id, "is_refresh": False})
        expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = LoginManage.create_token({"sub": result.user.id, "is_refresh": True}, expires=expires)
        resp = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "is_reset_password": result.user.is_reset_password,
            "is_wx_server_openid": result.user.is_wx_server_openid
        }
        await LoginLogDal(db).create_login_record(data, True, request, resp)
        return SuccessResponse(resp)
    except ValueError as e:
        await LoginLogDal(db).create_login_record(data, False, request, {"message": str(e)})
        return ErrorResponse(msg=str(e))


@app.post("/wx/login", summary="微信服务端一键登录", description="员工登录通道")
async def wx_login_for_access_token(
        request: Request,
        data: WXLoginForm,
        db: AsyncSession = Depends(db_getter)
  
):
    try:
        if data.platform != "1" or data.method != "2":
            raise ValueError("无效参数")
        
        # 获取微信配置信息
        settings_dal = SettingsDal(db)
        appid_setting = await settings_dal.get_data(config_key="wx_server_app_id", disabled=False, v_return_none=True)
        secret_setting = await settings_dal.get_data(config_key="wx_server_app_secret", disabled=False, v_return_none=True)
        
        if not appid_setting or not secret_setting:
            raise ValueError("微信配置信息不存在或已禁用")
        
        wx = WXOAuth(appid=appid_setting.config_value, secret=secret_setting.config_value)
        phone = await wx.parsing_phone_number(data.code)
        if not phone:
            raise ValueError("无效Code")
        data.phone = phone
        user = await UserDal(db).get_data(phone=phone, v_return_none=True)
        if not user:
            raise ValueError("手机号不存在")
        elif not user.is_active:
            raise ValueError("手机号已被冻结")
    except ValueError as e:
        await LoginLogDal(db).create_login_record(data, False, request, {"message": str(e)})
        return ErrorResponse(msg=str(e))

    # 更新登录时间
    await UserDal(db).update_login_info(user, request.client.host)

    # 登录成功创建 token
    access_token = LoginManage.create_token({"sub": user.phone, "is_refresh": False})
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = LoginManage.create_token({"sub": user.phone, "is_refresh": True}, expires=expires)
    resp = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "is_reset_password": user.is_reset_password,
        "is_wx_server_openid": user.is_wx_server_openid
    }
    await LoginLogDal(db).create_login_record(data, True, request, resp)
    return SuccessResponse(resp)


@app.post("/token/refresh", summary="刷新Token")
async def token_refresh(refresh: str = Body(..., title="刷新Token")):
    error_code = status.HTTP_401_UNAUTHORIZED
    try:
        payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        phone: str = payload.get("sub")
        is_refresh: bool = payload.get("is_refresh")
        if phone is None or not is_refresh:
            return ErrorResponse("未认证，请您重新登录", code=error_code, status=error_code)
    except jwt.exceptions.InvalidSignatureError:
        return ErrorResponse("无效认证，请您重新登录", code=error_code, status=error_code)
    except jwt.exceptions.ExpiredSignatureError:
        return ErrorResponse("登录已超时，请您重新登录", code=error_code, status=error_code)

    access_token = LoginManage.create_token({"sub": phone, "is_refresh": False})
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = LoginManage.create_token({"sub": phone, "is_refresh": True}, expires=expires)
    resp = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    return SuccessResponse(resp)
