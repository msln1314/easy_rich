# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

# from redis.asyncio import Redis
from fastapi import APIRouter, Depends, Body, UploadFile, Request
# from core.database import redis_getter
from utils.response import SuccessResponse, ErrorResponse
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, Auth
from sqlalchemy.orm import joinedload
from . import schemas, crud, models
from apps.admin.iot.crud.client_group import ClientGroupDal
from .schemas import UserOut,UserIn,UserSimpleOut,ResetPwd,UserUpdateBaseInfo,UserUpdate
from core.dependencies import IdList
from .params import UserParams

router = APIRouter()




###########################################################
#    用户管理
###########################################################
@router.get("", summary="获取用户列表")
async def get_users(
        params: UserParams = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.list"]))
):
    model = models.SysUser
    options = [joinedload(model.roles), joinedload(model.dept)]
    schema = UserOut
    datas, count = await crud.UserDal(auth.db).get_datas(
        **params.dict(),
        v_options=options,
        v_schema=schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@router.post("", summary="创建用户")
async def create_user(data: UserIn, auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.create"]))):
    roles = await crud.RoleDal(auth.db).get_datas(limit=0, id=("in", data.role_ids), v_return_objs=True)
    ext_obj = {}
    ext_obj['roles'] = roles
    # if data.iot_group_ids:
    #     iot_groups = await ClientGroupDal(auth.db).get_datas(limit=0, id=("in", data.iot_group_ids), v_return_objs=True)
    #     ext_obj['iot_groups'] = iot_groups
    return SuccessResponse(await crud.UserDal(auth.db).create_data(data=data,ext_obj=ext_obj))


@router.delete("", summary="批量删除用户", description="软删除，删除后清空所关联的角色")
async def delete_users(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.delete"]))):
    if auth.user.id in ids.ids:
        return ErrorResponse("不能删除当前登录用户")
    elif 1 in ids.ids:
        return ErrorResponse("不能删除超级管理员用户")
    await crud.UserDal(auth.db).delete_datas(ids=ids.ids, v_soft=True, is_active=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新用户信息")
async def put_user(
        data_id: int,
        data: UserUpdate,
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.update"]))
):
    ext_obj = {}
    if data.role_ids:
        roles = await crud.RoleDal(auth.db).get_datas(limit=0, id=("in", data.role_ids), v_return_objs=True)
        ext_obj['roles'] = roles
    # if data.iot_group_ids:
    #     iot_groups = await ClientGroupDal(auth.db).get_datas(limit=0, id=("in", data.iot_group_ids), v_return_objs=True)
    #     ext_obj['iot_groups'] = iot_groups
    # print("2222222222222222s",data)
    return SuccessResponse(await crud.UserDal(auth.db).put_data(data_id, data,ext_obj))


@router.get("/{data_id}", summary="获取用户信息")
async def get_user(
        data_id: int,
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.view", "sys.user.update"]))
):
    model = models.SysUser
    options = [joinedload(model.roles), joinedload(model.dept)]
    schema = UserOut
    return SuccessResponse(await crud.UserDal(auth.db).get_data(data_id, v_options=options, v_schema=schema))


@router.post("/current/update/password", summary="修改当前用户密码")
async def user_current_reset_password(data: ResetPwd, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.UserDal(auth.db).reset_current_password(auth.user, data))


@router.post("/current/update/info", summary="更新当前用户基本信息")
async def post_user_current_update_info(data: UserUpdateBaseInfo, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.UserDal(auth.db).update_current_info(auth.user, data))


@router.post("/current/update/avatar", summary="更新当前用户头像")
async def post_user_current_update_avatar(file: UploadFile, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.UserDal(auth.db).update_current_avatar(auth.user, file))


@router.get("/admin/current/info", summary="获取当前管理员信息")
async def get_user_admin_current_info(auth: Auth = Depends(FullAdminAuth())):
    print(auth.user.__dict__)
    result = UserOut.model_validate(auth.user).model_dump()
    result["permissions"] = list(FullAdminAuth.get_user_permissions(auth.user))
    return SuccessResponse(result)


@router.post("/export/query/list/to/excel", summary="导出用户查询列表为excel")
async def post_user_export_query_list(
        header: list = Body(..., title="表头与对应字段"),
        params: UserParams = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.export"]))
):
    return SuccessResponse(await crud.UserDal(auth.db).export_query_list(header, params))


@router.get("/download/import/template", summary="下载最新批量导入用户模板")
async def get_user_download_new_import_template(auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.UserDal(auth.db).download_import_template())


@router.post("/import", summary="批量导入用户")
async def post_import_users(file: UploadFile, auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.import"]))):
    return SuccessResponse(await crud.UserDal(auth.db).import_users(file))


@router.post("/init/password/send/sms", summary="初始化所选用户密码并发送通知短信")
async def post_users_init_password(
        request: Request,
        ids: IdList = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.reset"])),
        # rd: Redis = Depends(redis_getter)
):
    return SuccessResponse(await crud.UserDal(auth.db).init_password_send_sms(ids.ids))

@router.post("/init/password/reset", summary="初始化所选用户密码")
async def post_users_init_password(
        request: Request,
        ids: IdList = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.reset"])),
        # rd: Redis = Depends(redis_getter)
):
    return SuccessResponse(await crud.UserDal(auth.db).init_password_reset(ids.ids))


@router.post("/init/password/send/email", summary="初始化所选用户密码并发送通知邮件")
async def post_users_init_password_send_email(
        request: Request,
        ids: IdList = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.reset"])),
        # rd: Redis = Depends(redis_getter)
):
    web_mail = await crud.SettingsDal(auth.db).get_tab_values(tab_id=10)
    return SuccessResponse(await crud.UserDal(auth.db).init_password_send_email(ids.ids,web_mail))


@router.put("/wx/server/openid", summary="更新当前用户服务端微信平台openid")
async def put_user_wx_server_openid(code: str, auth: Auth = Depends(AllUserAuth())):
    result = await crud.UserDal(auth.db).update_wx_server_openid(code, auth.user)
    return SuccessResponse(result)

