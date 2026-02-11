# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse, ErrorResponse

from apps.admin.auth.utils.current import FullAdminAuth, Auth

from sqlalchemy.orm import joinedload
from . import schemas, crud, models
from core.dependencies import IdList
from .params import RoleParams

router = APIRouter()





###########################################################
#    角色管理
###########################################################
@router.get("", summary="获取角色列表")
async def get_roles(
        params: RoleParams = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.role.list"]))
):
    datas, count = await crud.RoleDal(auth.db).get_datas(**params.dict(), v_return_count=True, v_schema=schemas.RoleSimpleOut)
    return SuccessResponse(datas, count=count)


@router.post("", summary="创建角色信息")
async def create_role(role: schemas.RoleIn, auth: Auth = Depends(FullAdminAuth(permissions=["sys.role.create"]))):
    if role.menu_ids:
        menus = await crud.MenuDal(db=auth.db).get_datas(limit=0, id=("in", role.menu_ids), v_return_objs=True)
    else:
        menus = None
    return SuccessResponse(await crud.RoleDal(auth.db).create_data(data=role, menus=menus))


@router.delete("", summary="批量删除角色", description="硬删除, 如果存在用户关联则无法删除")
async def delete_roles(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth(permissions=["sys.role.delete"]))):
    if 1 in ids.ids:
        return ErrorResponse("不能删除管理员角色")
    await crud.RoleDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新角色信息")
async def put_role(
        data_id: int,
        data: schemas.RoleIn,
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.role.update"]))
):
    if 1 == data_id:
        return ErrorResponse("不能修改管理员角色")
    return SuccessResponse(await crud.RoleDal(auth.db).put_data(data_id, data))


@router.get("/options", summary="获取角色选择项")
async def get_role_options(auth: Auth = Depends(FullAdminAuth(permissions=["sys.user.create", "sys.user.update"]))):
    return SuccessResponse(await crud.RoleDal(auth.db).get_select_datas())


@router.get("/{data_id}", summary="获取角色信息")
async def get_role(
        data_id: int,
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.role.view", "sys.role.update"]))
):
    model = models.SysRole
    options = [joinedload(model.menus)]
    schema = schemas.RoleOut
    return SuccessResponse(await crud.RoleDal(auth.db).get_data(data_id, v_options=options, v_schema=schema))


@router.get("/role/menus/tree/{role_id}", summary="获取菜单列表树信息以及角色菜单权限ID，角色权限使用")
async def get_role_menu_tree(
        role_id: int,
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.role.create", "sys.role.update"]))
):
    tree_data = await crud.MenuDal(auth.db).get_tree_list(mode=3)
    role_menu_tree = await crud.RoleDal(auth.db).get_role_menu_tree(role_id)
    return SuccessResponse({"role_menu_tree": role_menu_tree, "menus": tree_data})
